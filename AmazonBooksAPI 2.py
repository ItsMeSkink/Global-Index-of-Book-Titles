from ScrappingClasses.amazonWebpage import amazonWebpage
from ScrappingClasses.googleWebpage import googleResults
from globalFunctions import threadMap

isbnInput = 9789380703688
# origin of species
isbnInput = 9789332585348
# python programming

resultsFromISBN = googleResults(f'"{isbnInput}" Book')
# this remains constant, no moving up in the list
# we only "titles" from this


def getFirstAmazonResult(currentIndex=0):
    if (currentIndex > len(resultsFromISBN.titles)):
        raise ValueError('This is the end of the line. No Amazon Results here')

    try:
        resultsFromBuyString = googleResults(
            resultsFromISBN.titles[currentIndex] + ' site:amazon.com').hrefs
        # this would yield the amazon links
        # we need the HREFS from this

        try:
            # this would yield the title if available
            amazonResult = amazonWebpage(resultsFromBuyString[0]).title
            # print(amazonResult)

            print(list(threadMap(lambda href: amazonWebpage(
                href).data, resultsFromBuyString)))

        except:
            # if title unavailable means the data is inappropriate, it would again run the entire function for the next isbn title
            print(
                f'No Amazon result for {resultsFromISBN.titles[currentIndex] + " site:amazon.com"}')
            getFirstAmazonResult(currentIndex + 1)
            # on the basis of the first result, other amazon links would be mapped and data would be retrieved

    except:
        # if there are no hrefs available, run the function again for the next isbn title
        print(
            f'No HREFs for {resultsFromISBN.titles[currentIndex] + " site:amazon.com"}')
        getFirstAmazonResult(currentIndex + 1)


getFirstAmazonResult()