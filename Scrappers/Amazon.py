from requestOrigins import Smartproxy
import re
import sys
sys.path.insert(1, 'C:\\Users\\Wicke\Desktop\\GIBT Draft 3')
from utilities import tryAndExcept


class AmazonProduct(Smartproxy):
    def __init__(self, asin):
        self.payload = {
            "target": "amazon_product",
            "query": asin,
            "parse": True,
            "domain": "com",
            "device_type": "desktop"
        }
        self.authorisationCode = 'Basic VTAwMDAxMDg4NDM6UCRXMWE0MGNlNjFmNTYzYTMyN2QyN2JhMzZiOThmYTc4N2Rl'

        self.inContent = self.res.json()['results'][0]['content']
        self.entireTitleList = self.inContent['title'].split(':')
        self.authors = list(map(lambda author: author.strip(),
                            self.inContent['manufacturer'].split(',')))
        self.rating = self.inContent['rating']
        self.thumbnail = self.inContent['images'][0]
        self.media = self.inContent['images']

    @property
    def title(self):
        return self.entireTitleList[0].strip()

    @property
    @tryAndExcept
    def subtitle(self):
        return self.entireTitleList[1].strip()

    @property
    def description(self):
        description = self.inContent['description']

        charactersToBeRemoved = ['\n', '\xa0']
        for characterToBeRemoved in charactersToBeRemoved:
            description = description.replace(characterToBeRemoved, ' ')

        return description

    @property
    @tryAndExcept
    def publisher(self):
        return self.inContent['product_details']['publisher']

    @property
    def pages(self):
        bookTypes = ['paperback', 'hardcover', 'print_length',
                     'staple_bound', 'cards', 'flexibound', 'board_book']
        pages = None

        typeIndex = 0
        while pages == None and typeIndex < len(bookTypes):
            try:
                pageString = self.inContent['product_details'][bookTypes[typeIndex]]
                pages = re.sub(' pages', '', pageString)
                pages = int(pages)
            except:
                typeIndex += 1

        return pages

    @property
    @tryAndExcept
    def isbn(self):
        return int(re.sub('-', '', self.inContent['product_details']['isbn_13']))

    @property
    def categories(self):
        categoryLadderCategories = list()
        salesCategories = list()
        try:
            categoryLadder = self.inContent['category'][0]['ladder']
            categoryLadderCategories = list(
                map(lambda item: item['name'], categoryLadder))
        except:
            pass

        try:
            salesRank = self.inContent['sales_rank']
            salesCategories = list(
                map(lambda item: item['ladder'][0]['name'], salesRank))
        except:
            pass

        return list(set(categoryLadderCategories + salesCategories))

    @property
    def data(self):
        data = {
            "title": self.title,
            "subtitle": self.subtitle,
            "authors": self.authors,
            "description": self.description,
            "pages": self.pages,
            "publisher": self.publisher,
            "isbn": self.isbn,
            "thumbnail": self.thumbnail,
            "rating": self.rating,
            "categories": self.categories
        }

        return data

    def json(self):
        return self.data


print(AmazonProduct('B074VF6ZLM').data)
