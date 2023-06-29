from functools import reduce
import json
import re
from turtle import color
from requests import get
from termcolor import colored
from Algorithms.ExtractMostCommonPhrase import extractMostCommonPhrase
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
        # self.title = re.sub(r'[^\w\s]', '', item['title'])

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
    
    @property
    def data(self):
        return self.json()


def returnListWithoutNone(array):
    return list(filter(lambda item: True if item != None else False, array))


class GoogleBooksSearch:
    """
    This method takes in 3 types of inputs
    1) ISBN
    2) Title
    3) Author

    Two types of inputs are frequently given -> 1) ISBN, 2) Title + Author

    The yield is always a list (1 item list in ISBN input and multiple items list in Title + Author input)
    Due to the list nature or all output, to get the title, we always write titles[0] in case of ISBN
    In input of Title + Author, titles of all objects are yielded
    """

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
            
    @property
    def webpage(self):
        return (get(f'https://www.googleapis.com/books/v1/volumes?q={self.query}', headers=HEADERS()))
        # proxies not required

    @property
    def statusCode(self):
        statusCode = self.webpage.status_code
        return colored(statusCode, 'green' if statusCode == 200 else 'red')


    @property
    def titles(self):
        titlesList = list(
            map(lambda bookObject: (bookObject)['title'], self.data))

        return returnListWithoutNone(titlesList)

    @property
    def subtitles(self):
        subtitlesList = list(
            map(lambda bookObject: (bookObject)["subtitle"], self.data))

        return list(filter(lambda subtitle: True if subtitle != None else False, subtitlesList))
        # fitlers and return subtitlesList

    @property
    def authors(self):
        authorsListsList = list(
            map(lambda bookObject: bookObject['authors'], self.data))

        if (authorsListsList != [None] or authorsListsList != None):
            return reduce(lambda x, y: x + y, (authorsListsList))
        else:
            return [str()]

    @property
    def descriptions(self):
        descriptionsList = list(
            map(lambda bookObject: (bookObject)['description'], self.data))

        return returnListWithoutNone(descriptionsList)

    @property
    def publishers(self):
        publishersList = list(
            map(lambda bookObject: (bookObject)['publisher'], self.data))

        return returnListWithoutNone(publishersList)

    @property
    def pageCounts(self):
        pageCountsList = list(
            map(lambda bookObject: (bookObject)['pages'], self.data))

        return returnListWithoutNone(pageCountsList)

    @property
    def isbns(self):
        isbnsList = list(
            map(lambda bookObject: (bookObject)['isbn'], self.data))

        return returnListWithoutNone(isbnsList)

    @property
    def thumbnails(self):
        thumbnailList = list(
            map(lambda bookObject: (bookObject)['thumbnail'], self.data))

        return returnListWithoutNone(thumbnailList)

    @property
    def rawItems(self):
        try:
            return json.loads(self.webpage.text)['items']
        except Exception as ke:
            pass

    @property
    def items(self):
        return list(map(lambda item: item['volumeInfo'], self.rawItems))

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
        book = GoogleBooksSearch(self.isbn)
        bookAgain = GoogleBooksSearch(
            title=book.titles[0], author=book.authors[0].split(' ')[-1])
        # use the author's last name for search

        return bookAgain.data

    def extractTitleAuthor(self):
        try:
            titles = list(
                map(lambda bookObject: re.sub(r'[^\w\s]', '', bookObject['title']), self.similars))

            authors = list(
                map(lambda bookObject: re.sub(r'[^\w\s]', '', bookObject['authors'][0]), self.similars))

            extractedTitle = extractMostCommonPhrase(titles).strip()
            extractedAuthor = extractMostCommonPhrase(authors).strip()

            return {
                "title": extractedTitle,
                "author": extractedAuthor
            }

        except Exception as e:
            print(colored(e, 'red'))

            if (self.authors == [None]):
                titles = list(map(lambda bookObject: bookObject['title'] + ' ' + (
                    bookObject['subtitle'] if bookObject['subtitle'] != None else ''), self.data))

                return {"title":  extractMostCommonPhrase(titles).strip(),
                        'author': ''}

            else:
                raise ReferenceError('Error in Titles')
