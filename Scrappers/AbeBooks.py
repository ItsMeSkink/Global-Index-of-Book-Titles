from concurrent.futures import ProcessPoolExecutor
from Scrappers.requestOrigins import webpageData
import re
from functools import reduce
from utilities import concatenate, extractText, extractURL, processMap, returnListWithoutNone, threadMap, tryAndExcept
import sys
sys.path.insert(2, 'C:\\Users\\Wicke\Desktop\\GIBT Draft 3')


addresses = {
    "servletAddresses": {
        "title": 'h1#book-title',
        "authors": 'h2#book-author',
        "isbn": 'div#isbn',
        'description': 'div.synopsis-body',
        'thumbnail': 'div#imageContainer img',
        "publisher": 'div.publisher span#book-publisher',
        "alternate": {
            'description': 'div.cf.detail-section div',
        }
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
    @tryAndExcept
    def subtitle(self):
        return self.entireTitleList[1].strip()

    @property
    @tryAndExcept
    def authors(self):
        authorsList = extractText(self.soup.select_one(
            self.addresses['authors'])).split(',')

        return list(map(lambda author: author.strip(), authorsList))

    @property
    @tryAndExcept
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
    @tryAndExcept
    def description(self):
        defaultDescription = extractText(
            self.soup.select_one(self.addresses['description']))

        if defaultDescription == 'None':
            return extractText(self.soup.select_one(
                self.addresses['alternate']['description']))
        else:
            return defaultDescription

    @property
    @tryAndExcept
    def thumbnail(self):
        return (self.soup.select_one(self.addresses['thumbnail']).get('src'))

    @property
    @tryAndExcept
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
            'thumbnail': self.thumbnail,
            "url": self.url
        }


# -----------------------------------------------------------


searchAddresses = {
    "searchResults": {
        "listingElement": 'li.cf.result-item',
        "titleHref": 'h2.title a',
        'isbnHref': 'p.isbn a'
    },
    "browseListingsResults": {
        "listingElement": 'td.result-details',
        "titleHref": 'b a',
    }

}


class AbeBooksSearchResult:
    def __init__(self, element, addresses):
        self.element = element
        self.addresses = addresses

    @property
    def title(self):
        return extractText(self.element.select_one(self.addresses['titleHref']))

    @property
    def titleHref(self):
        return 'https://www.abebooks.com' + extractURL(self.element.select_one(self.addresses['titleHref']))

    @property
    @tryAndExcept
    def isbnHref(self):
        return 'https://www.abebooks.com' + extractURL(self.element.select_one(self.addresses['isbnHref']))

    @property
    def data(self):
        return {
            'title': self.title,
            'hrefs': returnListWithoutNone([
                self.titleHref,
                self.isbnHref
            ])
        }


class AbeBooksSearch(webpageData):
    def __init__(self, url):
        url = re.sub(r'sortby=\d+&', 'sortby=20&', url)
        url = re.sub(r'bi=s&n=\d+&', '', url)
        self.url = url

        if (url.startswith('https://www.abebooks.com/servlet/BrowseListingsResults') == True):
            self.addresses = searchAddresses['browseListingsResults']
        else:
            self.addresses = searchAddresses['searchResults']

    @property
    def titles(self):
        return list(map(lambda item: item['title'], self.data))

    @property
    def hrefs(self):
        hrefsListLists = list(map(lambda item: item['hrefs'], self.data))
        hrefsList = concatenate(hrefsListLists)
        return returnListWithoutNone(hrefsList)

    @property
    def data(self):
        searchElements = self.soup.select(self.addresses['listingElement'])

        return list(map(lambda element: AbeBooksSearchResult(element, self.addresses).data, searchElements))

    @property
    def expandedData(self):

        # @tryAndExcept
        def extractAbeBooksData(url):
            try:
                data = AbeBooksBook(url)
                return data
            except:
                pass

        return list(threadMap(lambda url: extractAbeBooksData(url).data, self.hrefs))
