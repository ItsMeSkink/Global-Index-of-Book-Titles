from bs4 import BeautifulSoup
from requests import get
from termcolor import colored

from globalFunctions import HEADERS


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
