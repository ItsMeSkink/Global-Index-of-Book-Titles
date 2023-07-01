from utilities import extractText, extractURL, tryAndExcept
from functools import reduce
import re
import sys
from requestOrigins import webpageData
sys.path.insert(2, 'C:\\Users\\Wicke\Desktop\\GIBT Draft 3')


addresses = {
    "servletAddresses": {
        "title": 'h1#book-title',
        "authors": 'h2#book-author',
        "isbn": 'div#isbn',
        'description': 'div.synopsis-body',
        'thumbnail': 'img#isbn-image',
        "publisher": 'div.publisher span#book-publisher',
    },
    "isbnAddresses": {
        'title': 'div.plp-title',
        'authors': 'div.plp-author',
        "isbn": 'div.isbns.separator',
        "description": 'div.synopsis-body',
        "thumbnail": 'div#thumbnail img',
        "publisher": 'span#publisher-main',
        'similars': 'div.cf.break-b.m-md-b'
    }
}


class SimilarBook:
    def __init__(self, element):
        self.element = element

    @property
    def entireTitleList(self):
        return extractText(self.element.select_one('h2 a')).split(':')

    @property
    def title(self):
        return self.entireTitleList[0].strip()

    @property
    def subtitle(self):
        return self.entireTitleList[1].strip()

    @property
    def href(self):
        return 'https://www.abebooks.com' + extractURL(self.element.select_one('h2 a'))

    @property
    def data(self):
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "href": self.href
        }


class AbeBooksBook(webpageData):
    def __init__(self, url):
        self.url = url
        if (url.startswith('https://www.abebooks.com/978') or url.startswith('https://www.abebooks.com/products')):
            self.addresses = addresses['isbnAddresses']
            self.addressIndex = 1
        else:
            self.addresses = addresses['servletAddresses']
            self.addressIndex = 0

    @property
    def entireTitleList(self):
        return extractText(self.soup.select_one(self.addresses['title'])).split(':')

    @property
    def title(self):
        return self.entireTitleList[0].strip()

    @property
    def subtitle(self):
        return self.entireTitleList[1].strip()

    @property
    def authors(self):
        authorsList = extractText(self.soup.select_one(
            self.addresses['authors'])).split(',')

        return list(map(lambda author: author.strip(), authorsList))

    @property
    def isbn(self):
        if (self.addressIndex == 1):
            isbnsTagList = (self.soup.select_one(
                self.addresses['isbn']).select('span'))
            isbn13Tag = (list(filter(lambda isbnTag: True if re.search(
                '13', str(isbnTag)) != None else False, isbnsTagList))[0])
            isbn13 = int(extractText(isbn13Tag).split(':')[1])
            return isbn13
        else:
            isbnsTagList = self.soup.select_one(
                self.addresses['isbn']).select('a')

            isbn13 = int(extractText(list(filter(lambda tag: True if len(
                extractText(tag).strip()) == 13 else False, isbnsTagList))[0]))

            return isbn13

    @property
    def description(self):
        return extractText(self.soup.select_one(self.addresses['description']))

    @property
    def thumbnail(self):
        return (self.soup.select_one(self.addresses['thumbnail']).get('src'))

    @property
    def publisher(self):
        return extractText(self.soup.select_one(self.addresses['publisher'])).strip()

    @property
    @tryAndExcept
    def similars(self):
        similarsElementList = self.soup.select(self.addresses['similars'])

        return list(map(lambda element: SimilarBook(element).data, similarsElementList))

    @property
    def data(self):
        return {
            'title': self.title,
            'subtitle': self.subtitle,
            'authors': self.authors,
            'description': self.description,
            'isbn': self.isbn,
            'publisher': self.publisher,
            'thumbnail': self.thumbnail
        }


# -----------------------------------------------------------


class AbeBooksSearchResult:
    def __init__(self, element):
        self.element = element

    @property
    def title(self):
        return extractText(self.element.select_one('h2.title a'))

    @property
    def titleHref(self):
        return 'https://www.abebooks.com' + extractURL(self.element.select_one('h2.title a'))

    @property
    @tryAndExcept
    def isbnHref(self):
        return 'https://www.abebooks.com' + extractURL(self.element.select_one('p.isbn a'))

    @property
    def data(self):
        return {
            'title': self.title,
            'hrefs': [
                self.titleHref,
                self.isbnHref
            ]
        }


class AbeBooksSearch(webpageData):
    def __init__(self, url):
        url = re.sub(r'sortby=\d+&', 'sortby=20&', url)
        url = re.sub(r'bi=s&n=\d+&', '', url)
        self.url = url

    @property
    def titles(self):
        return list(map(lambda item: item['title'], self.data))

    @property
    def hrefs(self):
        hrefsListLists = list(map(lambda item: item['hrefs'], self.data))
        hrefsList = list((reduce(lambda x, y: x + y, hrefsListLists)))
        return hrefsList

    @property
    def data(self):
        searchElements = self.soup.select('li.cf.result-item')
        return list(map(lambda element: AbeBooksSearchResult(element).data, searchElements))
