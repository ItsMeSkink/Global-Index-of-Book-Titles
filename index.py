import os

from termcolor import colored
from GoogleBooksAPI import GoogleBooksSearch
from ScrappingClasses.abebooksWebpage import abeBookSearchPage, abeBooksWebpage
from ScrappingClasses.amazonWebpage import amazonWebpage
from ScrappingClasses.googleWebpage import googleResults
from globalFunctions import threadMap

os.system('start microsoft.windows.camera:')

book = GoogleBooksSearch(input('Enter an ISBN: '))

extract = book.extractTitleAuthor()
baseQuery = f' {extract["title"]} by {extract["author"]}'

print(baseQuery)

amazonSearchResults = googleResults(baseQuery + ' site:amazon.com')
abebooksSearchResults = googleResults(baseQuery + ' site:abebooks.com')

print(amazonSearchResults.hrefs)
print(abebooksSearchResults.hrefs)

# a = ['https://www.amazon.com/Cant-Hurt-Me-Master-Your/dp/1544512287', 'https://www.amazon.com/Cant-Hurt-Me-Master-Clean/dp/1544507852', 'https://www.amazon.com/Cant-Hurt-Me-Master-Your/dp/1544512279', 'https://www.amazon.com/Cant-Hurt-Me-Master-Clean/dp/1544507879', 'https://www.amazon.com/Cant-Hurt-Me-Master-Your-ebook/dp/B07H453KGH', 'https://www.amazon.com/Cant-Hurt-Me-David-Goggins-audiobook/dp/B07KKP62FW', 'https://www.amazon.com/cant-hurt-me-david-goggins-book/s%3Fk%3Dcan%2527t%2Bhurt%2Bme%2Bdavid%2Bgoggins%2Bbook', 'https://www.amazon.com/Cant-Hurt-Me-Master-Clean-ebook/dp/B085TCV73F', 'https://www.amazon.com/Cant-Hurt-Me-Master-Goggins/dp/B09SGFDBFD']


def scrapAmazonWebpage(href):
    try:
        return amazonWebpage(href).data
    except:
        return colored(href, 'red')


amazonScraped = list(
    threadMap(lambda href: scrapAmazonWebpage(href), amazonSearchResults))


def scrapAbeBooksWebpage(href):
    abebooksScrapResults = []
    try:
        if (href.startswith('https://www.abebooks.com/servlet/SearchResults') == True):
            abebooksScrapResults += abeBookSearchPage(href)
        else:
            abebooksScrapResults.join([abeBooksWebpage(href).data])

        return abebooksScrapResults
    except:
        return colored(href, 'red')


abebooksScraped = list(
    threadMap(lambda href: scrapAbeBooksWebpage(href), abebooksSearchResults))
