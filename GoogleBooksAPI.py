import json
from typing import Self
from requests import get
from termcolor import colored

from globalFunctions import HEADERS


class googleBooks:
    def __init__(self, isbn=int(), title=str(), author=str()):
        if (isbn != int()):
            self.query = f'isbn:{isbn}'
        elif (title != str() and author != str()):
            self.query = f"intitle:{title} inauthor:{author}"
        elif (title != str()):
            self.query = f'intitle:{title}'
        elif (author != str()):
            self.query = f'inauthor:{author}'
        else:
            raise KeyError(
                'No Query Resolved, Please Enter either an ISBN, Title or Author')

    @property
    def webpage(self):
        return (get(f'https://www.googleapis.com/books/v1/volumes?q={self.query}'))

    @property
    def statusCode(self):
        statusCode = self.webpage.status_code
        return colored(statusCode, 'green' if statusCode == 200 else 'red')

    @property
    def rawItems(self):
        return json.loads(self.webpage.text)['items']

    @property
    def items(self):
        return list(map(lambda item: item['volumeInfo'], self.rawItems))

    @property
    def titles(self):
        return list(map(lambda item: item['title'], self.items))

    @property
    def subtitles(self):
        def checkAndReturnSubtitle(item):
            try:
                return item['subtitle']
            except:
                return ''

        return list(map(checkAndReturnSubtitle, self.items))

    @property
    def authors(self):
        return (list(map(lambda item: item['authors'], self.items)))

    @property
    def descriptions(self):
        def checkAndReturnDescription(item):
            try:
                return item['description']
            except:
                return ''

        return list(map(checkAndReturnDescription, self.items))

    @property
    def publishers(self):
        def checkAndReturnPublisher(item):
            try:
                return item['publisher']
            except:
                return ''

        return list(map(checkAndReturnPublisher, self.items))

    @property
    def pageCounts(self):
        return list(map(lambda item: item['pageCount'], self.items))

    @property
    def isbns(self):
        def checkAndReturnForIndustryIdentifier(item):
            # first check if at all "industyIdentifiers" is available
            try:
                # when available
                isbnObjects = item['industryIdentifiers']
                # "industryIdentifers" list which contains 2 dictionaries, one 13 and one 10

                isbn13Object = list(filter(
                    lambda isbnObject: True if isbnObject['type'] == 'ISBN_13' else False, isbnObjects))
                # takes out the dictionary with "type" == "ISBN_13"
                try:
                    return isbn13Object[0]['identifier']
                    # returns the ISBN13 if available
                except:
                    pass
            except:
                pass

        industrialIdentifiersList = list(
            map(checkAndReturnForIndustryIdentifier, self.items))
        # we get the industrialIdentifersArray which contain the "fucked up" data of ISBN10 and ISBN13

        return industrialIdentifiersList


print(googleBooks(title="Psychology of Money", author="Morgan Housel").isbns)
