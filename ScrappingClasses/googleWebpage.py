from mimetypes import init
import re
from requests import get
from termcolor import colored
from ScrappingClasses.commons import webData
from globalFunctions import extractText, extractURL


class GoogleResult:
    def __init__(self, resultElement):
        self.resultElement = resultElement

    @property
    def title(self):
        return (extractText(self.resultElement.select_one('div.BNeawe.vvjwJb')))
        # resultElement is a soup itself

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


class googleWebpage(webData):
    def __init__(self, query):
        self.url = f'https://google.com/search?hl=en&q={query}'

        statusCode = self.webpage.status_code

        if (statusCode != 200):
            raise RuntimeError(f'Data not retrieved {statusCode}')

    @property
    def titles(self):
        titles = list(
            map(extractText, self.soup.select('div.egMi0.kCrYT a h3')))

        if (titles == []):
            raise ValueError('Titles not recieved')
        else:
            return titles

    @property
    def hrefs(self):

        allHrefs = list(map(extractURL, self.soup.select('div.egMi0 a')))
        # extracts a url from the unaccessible hrefs and create a list

        if (allHrefs == []):
            raise ValueError('HREFS not retrieved')

        else:
            return allHrefs

    @property
    def data(self):
        resultElements = self.soup.select('div.egMi0.kCrYT')
        return list(map(lambda element: GoogleResult(element).json(), resultElements))



# MAIN USE IN OTHER ALGORITHMS
class googleResults:
    def __init__(self, query):
        self.query = query
        self.titleExceptCount = 0
        self.hrefsExceptCount = 0
        self.dataExceptCount = 0

        # raise an error when after 5 recurrings it still doesn't yield data (meaning there isn't any data available).

    @property
    def titles(self):
        bookResults = googleWebpage(self.query)
        # if 429 error would be raised here only instaed of titles

        # if(self.titleExceptCount == 0):
            # raise ValueError('no titles found at all')

        try:
            titles = bookResults.titles
            if (titles == [] or titles == None or titles == 'None'):
                # self.titleExceptCount = self.titleExceptCount + 1
                self.titleExceptCount += 1
                return self.titles
            else:
                print(self.titleExceptCount)
                return titles
        except:
            self.titleExceptCount += 1
            return self.titles

    @property
    def hrefs(self):
        bookResults = googleWebpage(self.query)
        try:
            hrefs = bookResults.hrefs
            if (hrefs == [] or hrefs == None or hrefs == 'None'):
                self.hrefsExceptCount += 1
                return self.hrefs
            else:
                print(self.hrefsExceptCount)
                return hrefs
        except:
            self.hrefsExceptCount += 1
            return self.hrefs

    @property
    def data(self):
        bookResults = googleWebpage(self.query)
        try:
            data = bookResults.data
            if (data == [] or data == None or data == 'None'):
                self.dataExceptCount += 1
                return self.data
            else:
                print(self.dataExceptCount)
                return data
        except:
            self.dataExceptCount += 1
            return self.data
