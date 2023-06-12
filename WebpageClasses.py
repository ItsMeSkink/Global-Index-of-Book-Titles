from multiprocessing import AuthenticationError
import os
from bs4 import BeautifulSoup
from colorama import init
from requests import get
from termcolor import colored
from globalFunctions import HEADERS, extractText


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
        allHrefs = list(map(lambda a: a.get('href'),
                        self.soup.select('div#rcnt a')))

        if (self.filterLinks != 'https://www.'):
            return list(filter(lambda link: True if link.startswith(self.filterLinks) else False, allHrefs))
        else:
            return allHrefs


class amazonWebpage:
    def __init__(self, url):
        self.url = url

    @property
    def webpage(self):
        return get(self.url, headers=HEADERS)

    def __str__(self):
        return self.webpage.text

    @property
    def soup(self):
        return BeautifulSoup(self.webpage.text, 'lxml')

    @property
    def title(self):
        return extractText(self.soup.select('span#productTitle')[0]).strip()

    @property
    def description(self):
        return extractText(self.soup.select_one('div#bookDescription_feature_div div.a-expander-content')).strip()
