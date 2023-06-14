from mimetypes import init
from bs4 import BeautifulSoup
from outcome import Value
from requests import get
from termcolor import colored
from globalFunctions import HEADERS, extractText
import re


def getGoogleWebpage(userInput):
    return get(
        "https://www.google.com/search?hl=en&q=" + userInput, headers=HEADERS(), )


def printStatusCode(statusCode):
    print(colored(
        statusCode, 'green' if statusCode == 200 else 'red').center(100))


class googleResult:
    pass


class amazonBook:
    # def __init__(self, title, authors, thumbna):

    pass


class webData:
    @property
    def statusCode(self):
        statusCode = self.webpage.status_code
        return colored(statusCode, 'green' if statusCode == 200 else 'red')

    @property
    def webpage(self):
        return get(self.url, headers=HEADERS())

    def __str__(self):
        return self.webpage.text

    @property
    def soup(self):
        return BeautifulSoup(self.webpage.text, 'lxml')


class googleWebpage:
    def __init__(self, query, filterLinks=str()):
        self.query = query
        self.filterLinks = 'https://www.' + filterLinks

        statusCode = self.webpage.status_code

        if (statusCode != 200):
            raise RuntimeError(f'Data not retrieved {statusCode}')

    @property
    def statusCode(self):
        statusCode = self.webpage.status_code
        return colored(statusCode, 'green' if statusCode == 200 else 'red')

    @property
    def webpage(self):
        return get(f"https://google.com/search?hl=en&q={self.query}", headers=HEADERS())

    def __str__(self):
        return self.webpage.text

    @property
    def soup(self):
        return BeautifulSoup(self.webpage.text, 'lxml')

    @property
    def titles(self):
        return list(map(extractText, self.soup.select('div.egMi0.kCrYT a h3')))

    @property
    def hrefs(self):
        def extractURL(a):
            return (re.search(r"https://[\w\W]+&ved", a['href']).group().replace('&ved', ''))
            # .group() returns the matched string

        allHrefs = list(map(extractURL, self.soup.select('div.egMi0 a')))
        # extracts a url from the unaccessible hrefs and create a list

        if (allHrefs == []):
            raise ValueError('HREFS not retrieved')

        if (self.filterLinks != 'https://www.'):
            return list(filter(lambda link: True if link.startswith(self.filterLinks) else False, allHrefs))

        else:
            return allHrefs


class amazonWebpage(webData):
    def __init__(self, url):
        self.url = url

        statusCode = self.webpage.status_code

        if (statusCode != 200):
            raise RuntimeError(f'Data not retrieved {statusCode}')

        if (self.checkForCAPTCHA == True):
            raise RuntimeError(
                colored('You have been CAPTCHAd, change header', 'red'))

        if (self.title == None):
            raise ValueError('No Title Deteced')

    @property
    def title(self):
        return extractText(self.soup.select_one('span#productTitle')).strip()

    @property
    def description(self):
        return extractText(self.soup.select_one('div#bookDescription_feature_div div.a-expander-content')).strip()

    @property
    def authors(self):
        authors = (self.soup.select('span.author a'))
        return list(map(extractText, authors))

    @property
    def pages(self):
        pages = (extractText(self.soup.select_one('div#rpi-attribute-book_details-fiona_pages')
                             ).replace('Print length', '').replace('pages', '').strip())

        try:
            return int(pages)
        except:
            return None

    @property
    def publisher(self):
        return extractText(self.soup.select_one('div#rpi-attribute-book_details-publisher')).replace('Publisher', '').strip()

    @property
    def aboutAuthors(self):
        return extractText(self.soup.select_one('div#editorialReviews_feature_div div.a-padding-small')).strip()

    @property
    def thumbnail(self):
        return self.soup.select_one('img#imgBlkFront')['src']

    @property
    def data(self):
        return {
            "title": self.title,
            "authors": self.authors,
            "publisher": self.publisher,
            "thumbnail": self.thumbnail,
            "aboutAuthors": self.aboutAuthors,
            "pages": self.pages,
            "description": self.description,

        }

    @property
    def checkForCAPTCHA(self):
        captchaBox = extractText(
            self.soup.select_one('div.a-box-inner h4')).strip()

        if (captchaBox == 'Enter the characters you see below'):
            return True
            # we have gone into captcha
        else:
            return False


class abeBooksWebpage(webData):
    def __init__(self, url):
        self.url = url

    # @property
    # def webpage(self):
    #     return get(self.url, headers=HEADERS(), allow_redirects=False)
    #

    # this entire is if the url starts with https://www.abebooks.com/servlet
    @property
    def title(self):
        return extractText(self.soup.select_one('h1#book-title'))

    @property
    def authors(self):
        return (extractText(self.soup.select_one('h2#book-author'))).strip().lower().split(',')

    @property
    def isbn(self):
        isbnTag = (self.soup.select('div#isbn a'))
        isbns10And13 = (
            list(map(lambda item: extractText(item).strip(), isbnTag)))
        isbn13 = list(filter(lambda isbn: True if len(
            isbn) == 13 else False, isbns10And13))[0]
        return isbn13

    @property
    def description(self):
        return extractText(self.soup.select_one('div.synopsis-body')).strip()

    @property
    def publisher(self):
        return extractText(self.soup.select_one('div.publisher span#book-publisher')).strip()

    @property
    def thumbnail(self):
        return self.soup.select_one('div#itemOverview div#imageContainer.pswg img')['src']

    @property
    def data(self):
        return {
            "title": self.title,
            "authors": self.authors,
            "description": self.description,
            "publisher": self.publisher,
            "isbn": self.isbn,
            "thumbnail": self.thumbnail,
        }

    @property
    def isServlet(self):
        if(self.url.startswith('https://www.abebooks.com/servlet')):
            return True
        else:
            return False



# print(amazonWebpage('https://www.amazon.com/Python-Programming-Taneja-Sheetal-Naveen/dp/9332585342').aboutAuthors)
# print(googleWebpage('Buy 9789332585348 Book').titles)
# print(googleWebpage('Buy 9789380703688').titles)
# print(amazonWebpage('https://www.amazon.com/Origin-Species-Penguin-Classics/dp/0140439129/ref=sr_1_1_sspa?keywordsof+species').title)
# print(amazonWebpage('https://www.amazon.com/errors/validateCaptcha'))
abe = (abeBooksWebpage(
    'https://www.abebooks.com/servlet/BookDetailsPL?bi=31450032895&searchurl=ds%3D20%26kn%3Don%2Bof%2Bthe%2Borigin%2Bof%2Bspecies%26sortby%3D17&cm_sp=snippet-_-srp1-_-image1'))

print(abe.data)
