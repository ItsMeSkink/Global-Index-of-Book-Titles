import re
from bs4 import BeautifulSoup
from requests import get
from termcolor import colored
from ScrappingClasses.commons import webData
from globalFunctions import extractText


class googleWebpage(webData):
    def __init__(self, query, filterLinks=str()):
        self.query = query
        self.url = f'https://google.com/search?hl=en&q={self.query}'
        self.filterLinks = 'https://www.' + filterLinks

        statusCode = self.webpage.status_code

        if (statusCode != 200):
            raise RuntimeError(f'Data not retrieved {statusCode}')

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
