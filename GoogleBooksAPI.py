import json
from turtle import st
from outcome import Value
from requests import get
from termcolor import colored
from globalFunctions import HEADERS


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


class GoogleBook:
    def __init__(self, item):
        self.item = item
        self.title = item['title']
        self.authors = item['authors']

    @property
    def subtitle(self):
        try:
            return self.item['subtitle']
        except:
            pass

    @property
    def description(self):
        try:
            return self.item['description']
        except:
            pass

    @property
    def isbn(self):
        return checkAndReturnForIndustryIdentifier(self.item)

    @property
    def pages(self):
        try:
            return self.item['pageCount']
        except:
            pass

    @property
    def thumbnail(self):
        abeBooksThumbnailUrl = f"https://pictures.abebooks.com/isbn/{self.isbn}-us.jpg"

        if (get(abeBooksThumbnailUrl).status_code == 200):
            return abeBooksThumbnailUrl
        else:
            try:
                return self.item['imageLinks']['thumbnail']
            except:
                pass

    @property
    def publisher(self):
        try:
            return self.item['publisher']
        except:
            pass

    def json(self):
        return ({
            "title": self.title,
            "authors": self.authors,
            "thumbnail": self.thumbnail,
            "pages": self.pages,
            "publisher": self.publisher,
            "description": self.description,
            "subtitle": self.subtitle,
            "isbn": self.isbn,
        })


class googleBooksSearch:
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

        statusCode = self.webpage.status_code
        if (statusCode == 404 or json.loads(self.webpage.text)['totalItems'] == 0):
            raise ValueError(colored('Book Not Found. Branch Out', 'red'))
        elif (statusCode == 429):
            # print(colored('Try Again Later Network Overload', 'red'))
            raise RuntimeError(
                colored('Try Again Later, Network Overload 429'))
        elif (statusCode == 200):
            print(colored('Successfully Retreived', 'green'))

    @property
    def webpage(self):
        return (get(f'https://www.googleapis.com/books/v1/volumes?q={self.query}'))

    @property
    def statusCode(self):
        statusCode = self.webpage.status_code
        return colored(statusCode, 'green' if statusCode == 200 else 'red')

    @property
    def rawItems(self):
        try:
            return json.loads(self.webpage.text)['items']
        except Exception as ke:
            # print(colored('Not Retrieved. Branch Out', 'red'))
            # here another 3rd function would go which would retreive similar strucuted data from somewhere else
            pass

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
                pass
        return list(map(checkAndReturnSubtitle, self.items))

    @property
    def authors(self):
        def checkAndReturnForAuthors(item):
            try:
                return item['authors']
            except:
                pass

        return (list(map(checkAndReturnForAuthors, self.items)))

    @property
    def descriptions(self):
        def checkAndReturnDescription(item):
            try:
                return item['description']
            except:
                pass
        return list(map(checkAndReturnDescription, self.items))

    @property
    def publishers(self):
        def checkAndReturnPublisher(item):
            try:
                return item['publisher']
            except:
                pass
        return list(map(checkAndReturnPublisher, self.items))

    @property
    def pageCounts(self):
        def checkAndReturnForPageCount(item):
            try:
                return item['pageCount']
            except:
                pass
        return list(map(checkAndReturnForPageCount, self.items))

    @property
    def isbns(self):

        industrialIdentifiersList = list(
            map(checkAndReturnForIndustryIdentifier, self.items))
        # we get the industrialIdentifersArray which contain the "fucked up" data of ISBN10 and ISBN13

        return industrialIdentifiersList
        # it is not necessary that for every result there would be ISBN13 available

    @property
    def thumbnails(self):
        def checkAndReturnGoogleBooksThubnail(item):
            try:
                return item['imageLinks']['thumbnail']
            except:
                pass

        googleBooksThumbnails = list(
            map(checkAndReturnGoogleBooksThubnail, self.items))

        def checkAndReturnAbeBookThumbnail(isbn):
            abeBooksThumbnailUrl = f"https://pictures.abebooks.com/isbn/{isbn}-us.jpg"
            if (get(abeBooksThumbnailUrl).status_code == 200):
                return abeBooksThumbnailUrl

        abeBooksThumbnails = list(
            map(checkAndReturnAbeBookThumbnail, self.isbns))
        allThumbnails = googleBooksThumbnails + abeBooksThumbnails

        return list(filter(lambda url: True if url != None else url, allThumbnails))

    @property
    def data(self):
        return list(map(lambda item: GoogleBook(item).json(), self.items))

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)
        # more methods needed when "book not found"

    def __call__(self):
        statusCode = self.webpage.status_code
        if (statusCode == 404):
            print(colored('Not Retrieved. Branch Out', 'red'))
        elif (statusCode == 429):
            print(colored('Try Again Later Network Overload', 'red'))
        elif (statusCode == 200):
            print(colored('Successfully Retreived'))


book = (googleBooksSearch(title="Python Programming A Modular Approach").titles)
print(book)
