from mimetypes import init
import re
from bs4 import BeautifulSoup
from requests import get
from termcolor import colored
from ScrappingClasses.commons import webData
from globalFunctions import HEADERS, extractText, extractURL, threadMap


class GoogleResult:
    def __init__(self, resultElement):
        self.resultElement = resultElement

        if (self.title == None):
            raise ValueError('No Title Recieved')

    @property
    def title(self):
        soup = BeautifulSoup(get(self.href, headers=HEADERS()).text, 'lxml')
        # this prints the entire title by going inside the webpage and extracting the title
        title = extractText(soup.select_one('title'))
        return (title)

    @property
    def href(self):
        return extractURL(self.resultElement.select_one('a'))

    @property
    def data(self):
        return {
            "title": self.title,
            "href": self.href
        }

    def json(self):
        return self.data

# -------------------------------------------


class googleWebpage(webData):
    def __init__(self, query):
        self.url = f'https://google.com/search?hl=en&q={query}'

        statusCode = self.webpage.status_code

        if (statusCode != 200):
            raise RuntimeError(f'Data not retrieved {statusCode}')

    @property
    def titles(self):
        return list(map(lambda resultObject: resultObject['href'], self.data))

    @property
    def hrefs(self):
        return list(map(lambda resultObject: resultObject['href'], self.data))

    @property
    def data(self):
        resultElements = self.soup.select('div.egMi0.kCrYT')
        return list(threadMap(lambda element: GoogleResult(element).json(), resultElements))

# -------------------------------------------

# MAIN USE IN OTHER ALGORITHMS


class googleResults:
    def __init__(self, query):
        self.query = query
        self.titleExceptCount = 0
        self.hrefsExceptCount = 0
        self.dataExceptCount = 0
        self.data

        # raise an error when after 5 recurrings it still doesn't yield data (meaning there isn't any data available).
    @property
    def titles(self):
        return list(map(lambda result: result["title"], self.data))

    @property
    def hrefs(self):
        return list(map(lambda result: result["href"], self.data))

    @property
    def data(self):
        bookResults = googleWebpage(self.query)

        print(self.dataExceptCount)
        if (self.dataExceptCount > 3):
            raise ValueError(f'No Results for this {self.query}')

        try:
            data = bookResults.data
            if (data == [] or data == None or data == 'None'):
                self.dataExceptCount += 1
                return self.data
            else:
                return data
        except:
            self.dataExceptCount += 1
            return self.data

    def json(self):
        return self.data

# -------------------------------------------
