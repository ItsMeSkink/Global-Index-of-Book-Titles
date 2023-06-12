from calendar import LocaleHTMLCalendar
from mimetypes import init
from os import terminal_size
import time
from typing import Self
import attr
from requests import get, head
from bs4 import BeautifulSoup
from concurrent.futures import Executor, ThreadPoolExecutor
import re
from globalFunctions import HEADERS, extractText


class BookData:
    def __init__(self, title, author, description):
        self.title = title
        self.author = author
        self.description = description


def extractBookData(link):
    webpage = get(link, headers=HEADERS)

    soup = BeautifulSoup(webpage.content, 'lxml')
    title = soup.find('span', attrs={
        "id": 'productTitle'
    }).text.strip()

    author = extractText(list(soup.find('span', attrs={
        "class": "author"
    }).children)[1])
    # the find orignally returns an html element but extractText extracts the required text

    description = soup.find('div', attrs={
        "class": 'a-expander-content a-expander-partial-collapse-content'
    })
    description = re.sub(r'<.*?>', '', str(description)).strip()

    # thisBook = BookData(title, author, description)
    # print(thisBook.__dict__)
    print(title)
    # return thisBook.__dict__


def searchAmazon(query):

    webpage = get('https://amazon.com/s', params={
        "k": query
    }, headers=HEADERS)
    # try to rewrite headers when error code is 503
    print(str(webpage.status_code).center(100))

    soup = BeautifulSoup(webpage.content, 'lxml')

    links = soup.find_all('a', attrs={
        'class': 'a-link-normal s-no-outline'
    })

    linksList = list(
        map(lambda link: 'https://amazon.com' + link.get('href'), links))
    # print(linksList)

    # print(linksList)
    executor = ThreadPoolExecutor()
    ((executor.map(extractBookData, linksList)))
    # return


initTime = time.time()
(searchAmazon('On the Origin of Species'))
print(time.time() - initTime)
