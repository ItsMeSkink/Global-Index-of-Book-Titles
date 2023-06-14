from requests import get
from ScrappingClasses.commons import webData
from globalFunctions import HEADERS, extractText


class abeBooksWebpage(webData):
    def __init__(self, url):
        self.url = url

    @property
    def webpage(self):
        return get(self.url, headers=HEADERS(), allow_redirects=False)

    # this entire is if the url starts with https://www.abebooks.com/servlet
    @property
    def title(self):
        return extractText(self.soup.select_one('h1#book-title' if self.isServlet == True else "div.plp-title h1"))

    @property
    def authors(self):
        return (extractText(self.soup.select_one('h2#book-author' if self.isServlet == True else "div.plp-author h2 span"))).strip().lower().split(',')

    @property
    def isbn(self):
        if (self.isServlet == True):
            # returns the ISBN when the URL is a serlvet
            isbnTag = (self.soup.select('div#isbn a'))
            isbns10And13 = (
                list(map(lambda item: extractText(item).strip(), isbnTag)))
            isbn13 = list(filter(lambda isbn: True if len(
                isbn) == 13 else False, isbns10And13))[0]
            return isbn13
        else:
            # returns the ISBN when the URL is not servlet
            isbnTag = self.soup.select('div.isbns span')
            isbns10And13 = list(
                map(lambda item: item.text.split(':')[1].strip(), isbnTag))
            # prints only the isbn10 and isbn 13 (extracted from string)
            isbn13 = list(filter(lambda isbn: True if len(
                isbn) == 13 else False, isbns10And13))[0]
            return isbn13

    @property
    def description(self):
        return extractText(self.soup.select_one('div.synopsis-body')).strip()

    @property
    def publisher(self):
        return extractText(self.soup.select_one('div.publisher span#book-publisher' if self.isServlet == True else 'div.publisher span#publisher-main')).strip()

    @property
    def thumbnail(self):
        return self.soup.select_one('div#itemOverview div#imageContainer.pswg img' if self.isServlet == True else 'div#thumbnail.feature-image img')['src']

    @property
    def data(self):
        return {
            "title": self.title,
            "authors": self.authors,
            "description": self.description,
            "publisher": self.publisher,
            "isbn": self.isbn,
            "thumbnail": self.thumbnail,
        }

    def json(self):
        return self.data

    @property
    def isServlet(self):
        if (self.url.startswith('https://www.abebooks.com/servlet')):
            return True
        else:
            return False
