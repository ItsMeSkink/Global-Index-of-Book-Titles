from functools import reduce
import json
from requests import get
from termcolor import colored
from ExtractMostCommonPhrase import extractMostCommonPhrase
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

    @property
    def authors(self):
        try:
            return self.item['authors']
        except:
            pass

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

        if (get(abeBooksThumbnailUrl, headers=HEADERS()).status_code == 200):
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


def returnListWithoutNone(array):
    return list(filter(lambda item: True if item != None else False, array))


class googleBooksSearch:
    def __init__(self, isbn=int(), title=str(), author=str()):
        if (isbn != int()):
            self.isbn = isbn
            self.query = f'isbn:{isbn}'
        elif (title != str() and author != str()):
            self.title = title
            self.author = author
            self.query = f"intitle:{title} inauthor:{author}"
        elif (title != str()):
            self.title = title
            self.query = f'intitle:{title}'
        elif (author != str()):
            self.author = author
            self.query = f'inauthor:{author}'
        else:
            raise KeyError(
                'No Query Resolved, Please Enter either an ISBN, Title or Author')

        statusCode = self.webpage.status_code
        if (statusCode == 404 or json.loads(self.webpage.text)['totalItems'] == 0):
            raise ValueError(colored('Book Not Found. Branch Out', 'red'))
        elif (statusCode == 429):
            raise RuntimeError(
                colored('Try Again Later, Network Overload 429'))
        elif (statusCode == 200):
            print(colored('Successfully Retreived', 'green'))

    @property
    def webpage(self):
        return (get(f'https://www.googleapis.com/books/v1/volumes?q={self.query}', headers=HEADERS()))

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
        titlesList = list(
            map(lambda bookObject: GoogleBook(bookObject).title, self.items))

        return returnListWithoutNone(titlesList)

    @property
    def subtitles(self):
        subtitlesList = list(
            map(lambda bookObject: GoogleBook(bookObject).subtitle, self.items))

        return list(filter(lambda subtitle: True if subtitle != None else False, subtitlesList))
        # return subtitlesList

    @property
    def authors(self):
        authorsListsList = list(
            map(lambda bookObject: GoogleBook(bookObject).authors, self.items))

        return reduce(lambda x, y: x + y, list(authorsListsList))

    @property
    def descriptions(self):
        descriptionsList = list(
            map(lambda bookObject: GoogleBook(bookObject).description, self.items))

        return returnListWithoutNone(descriptionsList)

    @property
    def publishers(self):
        publishersList = list(
            map(lambda bookObject: GoogleBook(bookObject).publisher, self.items))

        return returnListWithoutNone(publishersList)

    @property
    def pageCounts(self):
        pageCountsList = list(
            map(lambda bookObject: GoogleBook(bookObject).pages, self.items))

        return returnListWithoutNone(pageCountsList)

    @property
    def isbns(self):
        isbnsList = list(
            map(lambda bookObject: GoogleBook(bookObject).isbn, self.items))

        return returnListWithoutNone(isbnsList)

    @property
    def thumbnails(self):
        thumbnailList = list(
            map(lambda bookObject: GoogleBook(bookObject).thumbnail, self.items))

        return returnListWithoutNone(thumbnailList)

    @property
    def data(self):
        return list(map(lambda item: GoogleBook(item).json(), self.items))

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)
        # more methods needed when "book not found"

    # --------------------------------------------------------------------------------------------

    @property
    def similars(self):
        book = googleBooksSearch(self.isbn)
        bookAgain = googleBooksSearch(
            title=book.titles[0], author=book.authors[0])

        return bookAgain.data

    def extractTitleAuthor(self):
        titles = list(
            map(lambda bookObject: bookObject['title'] + ' ' + (bookObject['subtitle'] if bookObject['subtitle'] != None else ''), self.similars))
        authors = list(
            map(lambda bookObject: bookObject['authors'][0], self.similars))

        extractedTitle = extractMostCommonPhrase(titles)
        extractedAuthor = extractMostCommonPhrase(authors)

        return {
            "title": extractedTitle,
            "author": extractedAuthor
        }
