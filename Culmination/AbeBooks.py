import json
import sys
sys.path.insert(1, 'C:\\Users\\Wicke\Desktop\\GIBT Draft 3')
import time

from Scrappers.AbeBooks import AbeBooksBook, AbeBooksSearch
from Scrappers.Google import GoogleSearch
from utilities import concatenate, processMap, threadMap



def AbeBooksData(baseQuery):
    abeBooksSearchResults = GoogleSearch(baseQuery + ' site:abebooks.com')
    print(abeBooksSearchResults.searchURL)

    abeBooksSearchEndpoints = [
        'https://www.abebooks.com/sevlet/SearchResults',
        "https://www.abebooks.com/book-search",
        "https://www.abebooks.com/servlet/BrowseListingsResults"
    ]

    abeBooksUrls = {
        "search": list(),
        "books": list()
    }

    for url in abeBooksSearchResults.hrefs:
        '''sorts the url in "search" and "books"'''
        endpointIndex = 0
        endpointsNumber = len(abeBooksSearchEndpoints)

        for endpoint in abeBooksSearchEndpoints:
            if (url.startswith(endpoint) == True):
                abeBooksUrls['search'].append(url)
            else:
                endpointIndex += 1

        if (endpointIndex == endpointsNumber):
            abeBooksUrls['books'].append(url)

    
    searchResultsData = concatenate(
        list(threadMap(lambda url: AbeBooksSearch(url).expandedData, abeBooksUrls['search'])))

    booksData = list(
        threadMap(lambda url: AbeBooksBook(url).data, abeBooksUrls['books']))

    entireData = searchResultsData + booksData

    with open(f'./AnalysisData/AbeBooks/{baseQuery}.json', 'w') as file:
        file.write(json.dumps(entireData))

    return entireData


