from bs4 import BeautifulSoup
from requests import get
from termcolor import colored
from globalFunctions import HEADERS
from bs4.builder import XMLParsedAsHTMLWarning
import warnings

warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)
# this would filter the warnings even though the code does work


class webData:
    @property
    def statusCode(self):
        statusCode = self.webpage.status_code
        return colored(statusCode, 'green' if statusCode == 200 else 'red')

    @property
    def webpage(self):
        self.webHeaders = HEADERS()
        webHeaders = self.webHeaders

        return get(self.url, headers=webHeaders)

    def __str__(self):
        return self.webpage.text

    @property
    def soup(self):
        return BeautifulSoup(self.webpage.text, 'lxml')
