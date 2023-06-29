from bs4 import BeautifulSoup
from termcolor import colored
from bs4.builder import XMLParsedAsHTMLWarning
import warnings
from Proxying.Proxying import getRequest
import sys

from globalFunctions import HEADERS
sys.path.insert(1, 'C:\\Users\\Wicke\\Desktop\\GIBT Draft 2\\')

warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)
# this would filter the warnings even though the code does work


class webpageData:
    @property
    def webpage(self):
        return getRequest(self.url).res

    @property
    def statusCode(self):
        statusCode = self.webpage.status_code
        return colored(statusCode, 'green' if statusCode == 200 else 'red')

    def __str__(self):
        return self.webpage.text

    @property
    def soup(self):
        return BeautifulSoup(self.webpage.text, 'lxml')
