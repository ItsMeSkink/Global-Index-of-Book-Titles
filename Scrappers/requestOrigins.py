import sys
sys.path.insert(1, 'C:\\Users\\Wicke\\Desktop\\GIBT Draft 3\\')
from utilities import headers
from requests import post, get
from bs4 import BeautifulSoup
from termcolor import colored
from bs4.builder import XMLParsedAsHTMLWarning
import warnings


url = "https://scrape.smartproxy.com/v1/tasks"
warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)
# this would filter the warnings even though the code does work


class Smartproxy:
    @property
    def response(self):
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": self.authorisationCode
        }
        return post(url, json=self.payload, headers=headers)

    @property
    def res(self):
        # with open('sample.json', 'w') as file:
        #     file.write(self.response.text)
        return self.response

    @property
    def text(self):
        return self.res.text

    @property
    def content(self):
        return self.res.content

    @property
    def headers(self):
        return self.res.headers

    @property
    def statusCode(self):
        return self.res.status_code


class webpageData:
    @property
    def webpage(self):
        return get(self.url, headers=headers())

    @property
    def statusCode(self):
        statusCode = self.webpage.status_code
        return colored(statusCode, 'green' if statusCode == 200 else 'red')

    def __str__(self):
        return self.webpage.text

    @property
    def soup(self):
        soup =  BeautifulSoup(self.webpage.text, 'lxml')
        soup.encode('utf-8')
        return soup
