from requests import get
from ScrappingClasses.abebooksWebpage import abeBookSearchPage, abeBooksWebpage
from ScrappingClasses.googleWebpage import googleResults


isbnInput = 9789380703688
# origin of species
isbnInput = 9789332585348
# python programming

resultsFromISBN = googleResults(f'"{isbnInput}" Book')


def getFirstAbebookResult(currentIndex=0):
    if (currentIndex > len(resultsFromISBN.titles)):
        raise ValueError('This is the end of the line. No AbeBook Results here')

    try:
        resultsFromBuyString = googleResults(
            resultsFromISBN.titles[currentIndex] + ' site:abebooks.com').hrefs

        try:
            firstHref = resultsFromBuyString[0]
            if (firstHref.startswith('https://www.abebooks.com/servlet/SearchResults' == True)):
                print(abeBookSearchPage(firstHref).booksData)
            else:
                print(abeBooksWebpage(firstHref))

        except:
            print(
                f'No AbeBooks result for {resultsFromISBN.titles[currentIndex] + " site:amazon.com"}')
            getFirstAbebookResult(currentIndex + 1)

    except:
        print(
            f'No HREFs for {resultsFromISBN.titles[currentIndex] + " site:abebooks.com"}')
        getFirstAbebookResult(currentIndex + 1)


getFirstAbebookResult()