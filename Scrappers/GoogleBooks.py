from utilities import concatenate, headers, returnListWithoutNone, tryAndExcept
from Algorithms.ExtractMostCommonPhrase import extractMostCommonPhrase
import re
from termcolor import colored
from requests import get
from cv2 import reduce
import json
import sys
sys.path.insert(2, 'C:\\Users\\Wicke\Desktop\\GIBT Draft 3')


@tryAndExcept
def checkAndReturnForIndustryIdentifier(item):
    # first check if at all "industyIdentifiers" is available
    # when available
    isbn13Object = list(filter(
        lambda isbnObject: True if isbnObject['type'] == 'ISBN_13' else False, item))
    # takes out the dictionary with "type" == "ISBN_13"
    return isbn13Object[0]['identifier']
    # returns the ISBN13 if available


class GoogleBook:
    def __init__(self, volumeInfo):
        self.volumeInfo = volumeInfo

    @property
    def title(self):
        return self.volumeInfo['title']

    @property
    @tryAndExcept
    def subtitle(self):
        return self.volumeInfo['subtitle']

    @property
    @tryAndExcept
    def authors(self):
        return self.volumeInfo['authors']

    @property
    @tryAndExcept
    def description(self):
        return self.volumeInfo['description']

    @property
    @tryAndExcept
    def publisher(self):
        return self.volumeInfo['publisher']

    @property
    @tryAndExcept
    def isbn(self):
        return int(checkAndReturnForIndustryIdentifier(self.volumeInfo['industryIdentifiers']))

    @property
    @tryAndExcept
    def pages(self):
        return self.volumeInfo['pageCount']

    @property
    @tryAndExcept
    def categories(self):
        return self.volumeInfo['categories']

    @property
    @tryAndExcept
    def rating(self):
        return self.volumeInfo['averageRating']

    @property
    @tryAndExcept
    def thumbnails(self):
        googleBooksThumbnail = self.volumeInfo['imageLinks']['thumbnail']
        abeBooksThumbnailUrl = f"https://pictures.abebooks.com/isbn/{self.isbn}-us.jpg"

        if (get(abeBooksThumbnailUrl, headers=headers()).status_code) == 200:
            abeBooksThumbnail = abeBooksThumbnailUrl

        return [
            googleBooksThumbnail,
            abeBooksThumbnail
        ]

    @property
    def data(self):
        return {
            'title': self.title,
            'subtitle': self.subtitle,
            'authors': self.authors,
            'description': self.description,
            'pages': self.pages,
            'isbn': self.isbn,
            'publisher': self.publisher,
            'categories': self.categories,
            'rating': self.rating,
            'thumbnails': self.thumbnails
        }


# ----------------------------------------------

class GoogleBooksSearch:
    def __init__(self, isbn=int(), title=str(), author=str()):
        # sets the default values for these attributes
        if (isbn != int()):
            self.isbn = isbn
            self.title = None
            self.author = None
            self.query = f'isbn:{isbn}'
        elif (title != str() and author != str()):
            self.title = title
            self.author = author
            self.isbn = None
            self.query = f"intitle:{title} inauthor:{author}"
        elif (title != str()):
            self.title = title
            self.author = None
            self.isbn = None
            self.query = f'intitle:{title}'
        elif (author != str()):
            self.author = author
            self.title = None
            self.isbn = None
            self.query = f'inauthor:{author}'
        else:
            raise KeyError(
                'No Query Resolved, Please Enter either an ISBN, Title or Author')
        statusCode = self.statusCode
        if (self.webpage.json()['totalItems'] == 0):
            statusCode = 404

        match statusCode:
            case 404:
                raise ValueError(colored('Book Not Found. Branch Out', 'red'))
            case 429:
                raise RuntimeError(
                    colored('Try Again Later, Network Overload 429'))

    @property
    def webpage(self):
        return (get(f'https://www.googleapis.com/books/v1/volumes?q={self.query}', headers=headers()))

    @property
    def statusCode(self):
        return self.webpage.status_code

    @property
    def titles(self):
        return list(map(lambda item: item['title'], self.data))

    @property
    def subtitles(self):
        return returnListWithoutNone(list(map(lambda item: item['subtitle'], self.data)))

    @property
    def authors(self):
        return returnListWithoutNone(list(map(lambda item: item['authors'], self.data)))

    @property
    def descriptions(self):
        return returnListWithoutNone(list(map(lambda item: item['description'], self.data)))

    @property
    def isbns(self):
        return returnListWithoutNone(list(map(lambda item: (item['isbn']), self.data)))

    @property
    def publishers(self):
        return returnListWithoutNone(list(map(lambda item: item['publisher'], self.data)))

    @property
    def pagesCounts(self):
        return returnListWithoutNone(list(map(lambda item: item['pages'], self.data)))

    @property
    def thumbnails(self):
        thumbnailsList = concatenate(list(
            map(lambda item: item['thumbnails'], self.data)))

        return returnListWithoutNone(thumbnailsList)

    @property
    def data(self):
        return list(map(lambda item: GoogleBook(item['volumeInfo']).data, self.webpage.json()['items']))

    def json(self):
        return self.data

    @property
    def similars(self):
        if self.isbn != None:
            book = GoogleBooksSearch(self.isbn).data[0]
            author = book['authors'][0].split(
                ' ')[-1] if book['authors'] != None else None
            # use the author's last name for search

            bookAgain = GoogleBooksSearch(
                title=book['title'], author=author)
        else:
            bookAgain = self
            # isbn directs to a single particular book. Another type of query would yield multiple results (which we require as similars results)

        return bookAgain
        # this would not only return the dictionary data but the entire class to be utilized

    def extractTitleAndAuthor(self):
        def removeNonAlphaSpace(item):
            return re.sub(r'[^\w\s]', '', item)

        titles = list(map(removeNonAlphaSpace, self.similars.titles))
        authors = list(
            map(removeNonAlphaSpace, concatenate(self.similars.authors)))

        extractedTitle = extractMostCommonPhrase(titles)
        extractedAuthors = extractMostCommonPhrase(authors)

        return {
            'title': extractedTitle,
            'author': extractedAuthors
        }
