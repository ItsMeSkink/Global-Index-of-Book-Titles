import re
from termcolor import colored
from ScrappingClasses.commons import webData
from globalFunctions import extractText, extractURL, threadMap


class amazonWebpage(webData):
    def __init__(self, url):
        self.url = url

        statusCode = self.webpage.status_code

        if (statusCode != 200):
            raise RuntimeError(f'Data not retrieved {statusCode}')

        if (self.checkForCAPTCHA == True):
            raise RuntimeError(
                colored('You have been CAPTCHAd, change header', 'red'))

        if (self.title == None):
            raise ValueError('No Title Deteced')
            # returns that the page is inappropriate

    @property
    def title(self):
        try:
            return extractText(self.soup.select_one('span#productTitle')).strip()
        except:
            pass

    @property
    def description(self):
        try:
            return extractText(self.soup.select_one('div#bookDescription_feature_div div.a-expander-content')).strip()
        except:
            pass

    @property
    def authors(self):
        try:
            authors = (self.soup.select('span.author a'))
            return list(map(extractText, authors))
        except:
            pass

    @property
    def pages(self):
        pages = (extractText(self.soup.select_one('div#rpi-attribute-book_details-fiona_pages')
                             ).replace('Print length', '').replace('pages', '').strip())

        try:
            return int(pages)
        except:
            pass

    @property
    def publisher(self):
        try:
            return extractText(self.soup.select_one('div#rpi-attribute-book_details-publisher')).replace('Publisher', '').strip()
        except:
            pass

    @property
    def aboutAuthors(self):
        try:
            return extractText(self.soup.select_one('div#editorialReviews_feature_div div.a-padding-small')).strip()
        except:
            pass

    @property
    def thumbnail(self):
        try:
            return self.soup.select_one('img#imgBlkFront')['src']
        except:
            pass

    @property
    def data(self):
        return {
            "title": self.title,
            "authors": self.authors,
            "publisher": self.publisher,
            "thumbnail": self.thumbnail,
            "aboutAuthors": self.aboutAuthors,
            "pages": self.pages,
            "description": self.description,
        }

    @property
    def checkForCAPTCHA(self):
        captchaBox = extractText(
            self.soup.select_one('div.a-box-inner h4')).strip()

        if (captchaBox == 'Enter the characters you see below'):
            return True
            # we have gone into captcha
        else:
            return False
