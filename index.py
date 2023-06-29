import os
import re

from termcolor import colored
from Scrappers.AbeBooksBook import AbeBooksBook, AbeBooksSearchPage
from Scrappers.AmazonProduct import AmazonProduct
from Scrappers.GoogleBooksAPI import GoogleBooksSearch
from Scrappers.GoogleSearch import GoogleSearch
from globalFunctions import threadMap

os.system('start microsoft.windows.camera:')

book = GoogleBooksSearch(input('Enter an ISBN: '))

extract = book.extractTitleAuthor()
baseQuery = f' {extract["title"]} by {extract["author"]}'

print(baseQuery)

amazonSearchResults = GoogleSearch(baseQuery + ' site:amazon.com')
# abebooksSearchResults = googleResults(baseQuery + ' site:abebooks.com')

print(amazonSearchResults.hrefs)
# print(abebooksSearchResults.hrefs)


def scrapAmazonWebpage(href):
    try:
        a = AmazonProduct(href).data
        print(a)
        return a
    except:
        return colored(href, 'red')


def scrapAbeBooksWebpage(href):
    abebooksScrapResults = list()
    try:
        if (href.startswith('https://www.abebooks.com/servlet/SearchResults') == True):
            abebooksScrapResults += AbeBooksSearchPage(href)
        else:
            abebooksScrapResults.join([AbeBooksBook(href).data])

        return abebooksScrapResults
    except:
        return colored(href, 'red')


amazonScraped = list(
    threadMap(lambda href: scrapAmazonWebpage(re.sub('https', 'http', href)), amazonSearchResults.hrefs))

print(amazonScraped)
