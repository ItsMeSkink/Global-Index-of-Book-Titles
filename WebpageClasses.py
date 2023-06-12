from bs4 import BeautifulSoup
from requests import get
from termcolor import colored
from globalFunctions import HEADERS, extractText
import re


def getGoogleWebpage(userInput):
    return get(
        "https://www.google.com/search?hl=en&q=" + userInput, headers=HEADERS)


def printStatusCode(statusCode):
    print(colored(
        statusCode, 'green' if statusCode == 200 else 'red').center(100))


def getAmazonLinks(userInput):

    webpage = getGoogleWebpage(userInput)

    statusCode = webpage.status_code

    printStatusCode(statusCode)
    soup = BeautifulSoup(webpage.text, 'lxml')

    hrefs = list(map(lambda a: a.get('href'), soup.select('div#rcnt a')))

    def filterAmazonLinks(link):
        if link.startswith('https://www.amazon.'):
            return True

    amazonLinks = list(filter(filterAmazonLinks, hrefs))
    return amazonLinks


class webData:
    @property
    def statusCode(self):
        statusCode = self.webpage.status_code
        return colored(statusCode, 'green' if statusCode == 200 else 'red')

    @property
    def webpage(self):
        return get(self.url, headers=HEADERS)

    def __str__(self):
        return self.webpage.text

    @property
    def soup(self):
        return BeautifulSoup(self.webpage.text, 'lxml')


class googleWebpage:
    def __init__(self, query, filterLinks=str()):
        self.query = query
        self.filterLinks = 'https://www.' + filterLinks

    @property
    def statusCode(self):
        statusCode = self.webpage.status_code
        return colored(statusCode, 'green' if statusCode == 200 else 'red')

    @property
    def webpage(self):
        return get(f"https://google.com/search?hl=en&q={self.query}", headers=HEADERS)

    def __str__(self):
        return self.webpage.text

    @property
    def soup(self):
        return BeautifulSoup(self.webpage.text, 'lxml')

    @property
    def titles(self):
        return list(map(extractText, self.soup.select('h3')))

    @property
    def hrefs(self):
        def extractURL(a):
            return (re.search(r"https://[\w\W]+&ved", a['href']).group().replace('&ved', ''))
            # .group() returns the matched string

        allHrefs = list(map(extractURL, self.soup.select('div.egMi0 a')))
        # extracts a url from the unaccessible hrefs and create a list

        if (self.filterLinks != 'https://www.'):
            return list(filter(lambda link: True if link.startswith(self.filterLinks) else False, allHrefs))

        else:
            return allHrefs


class amazonWebpage(webData):
    def __init__(self, url):
        self.url = url

    @property
    def title(self):
        return extractText(self.soup.select('span#productTitle')[0]).strip()

    @property
    def description(self):
        return (self.soup.select_one('div#bookDescription_feature_div div.a-expander-content')).strip()

    @property
    def authors(self):
        authors = (self.soup.select('span.author a'))
        return list(map(extractText, authors))

    @property
    def pages(self):
        return int(extractText(self.soup.select_one('div#rpi-attribute-book_details-fiona_pages')).replace('Print length', '').replace('pages', '').strip())

    @property
    def publisher(self):
        return extractText(self.soup.select_one('div#rpi-attribute-book_details-publisher')).replace('Publisher', '').strip()

    @property
    def aboutAuthors(self):
        return extractText(self.soup.select_one('div#editorialReviews_feature_div div.a-padding-small')).strip()


class abeBooksWebpage(webData):
    def __init__(self, url):
        self.url = url

    @property
    def title(self):
        return extractText(self.soup.select_one('h1#book-title'))


print(abeBooksWebpage('https://www.abebooks.com/servlet/BookDetailsPL?bi=31293596369&searchurl=n%3D100121501%26bi%3Ds%26sortby%3D17%26tn%3Dpython%2Bprogramming%2Bmodular%2Bapproach%26an%3Dnaveen%2Bkumar&cm_sp=snippet-_-srp1-_-image1').title)
