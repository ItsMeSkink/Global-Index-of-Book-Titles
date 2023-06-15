from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from csv import list_dialects
from mimetypes import init
import re
from requests import get
import soupsieve
from ScrappingClasses.commons import webData
from globalFunctions import HEADERS, extractText, threadMap


# web process of abebooks for www.abebooks.com/servlet/search

class abeBooksWebpage(webData):
    def __init__(self, url):
        self.url = url

        if (self.title == 'None'):
            raise ValueError('No title returned')

        try:
            pass
        except Exception as e:
            print(url)
            print(e)

    @property
    def webpage(self):
        return get(self.url, headers=HEADERS(), allow_redirects=False)

    # this entire is if the url starts with https://www.abebooks.com/servlet
    @property
    def title(self):
        return extractText(self.soup.select_one('h1#book-title span' if self.isServlet == True else "div.plp-title h1"))

    @property
    def authors(self):
        return (extractText(self.soup.select_one('h2#book-author' if self.isServlet == True else "div.plp-author h2 span"))).strip().lower().split(',')

    @property
    def isbn(self):
        isbns10And13 = list()
        if (self.isServlet == True):
            # returns the ISBN when the URL is a serlvet
            isbnTag = (self.soup.select('div#isbn a'))
            isbns10And13 = (
                list(map(lambda item: extractText(item).strip(), isbnTag)))
        else:
            # returns the ISBN when the URL is not servlet
            isbnTag = self.soup.select('div.isbns span')
            isbns10And13 = list(
                map(lambda item: item.text.split(':')[1].strip(), isbnTag))
            # prints only the isbn10 and isbn 13 (extracted from string)

        isbn13 = list(filter(lambda isbn: True if len(
            isbn) == 13 else False, isbns10And13))

        try:
            return isbn13[0]
            # in case when there is no ISBN available
        except:
            pass

    @property
    def description(self):
        description = extractText(
            self.soup.select_one('div.synopsis-body')).strip()

        if (description.startswith('Please Read Notes')):
            # in case when the dsecription start with "Please Read Notes" because it isn't an actual description
            pass
        else:
            return description

    @property
    def publisher(self):
        return extractText(self.soup.select_one('div.publisher span#book-publisher' if self.isServlet == True else 'div.publisher span#publisher-main')).strip()

    @property
    def thumbnail(self):
        thumbnail = self.soup.select_one(
            'div#itemOverview div#imageContainer.pswg img' if self.isServlet == True else 'div#thumbnail.feature-image img')

        try:
            # in case thumbnail is not available
            return thumbnail['src']
        except:
            pass

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

# replace "sortby=17 with sortby=20"
# remove "&bi=s&n=100121501"


class abeBookSearchPage(webData):
    def __init__(self, url):
        url = re.sub(r'sortby=\d+&', 'sortby=20&', url)
        url = re.sub(r'bi=s&n=\d+&', '', url)

        self.url = url

    @property
    def titleHrefs(self):
        hrefs = self.soup.select('div.result-detail.col-xs-8 h2.title a')

        return list(map(lambda a: 'https://www.abebooks.com' + re.sub(r'&searchurl=[\w\W]+', '', a['href']), hrefs))

    @property
    def isbnHrefs(self):
        hrefs = self.soup.select(
            'div.result-detail.col-xs-8 p.isbn.pub-data a')

        return list(map(lambda a: 'https://www.abebooks.com' + re.sub(r'&searchurl=[\w\W]+', '', a['href']), hrefs))

    @property
    def booksData(self):
        return (list(threadMap(lambda href: abeBooksWebpage(href).data, (self.titleHrefs + self.isbnHrefs))))
