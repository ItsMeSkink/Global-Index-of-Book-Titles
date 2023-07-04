from utilities import returnListWithoutNone, threadMap, tryAndExcept
from Scrappers.Google import GoogleSearch
from Scrappers.Amazon import AmazonProduct
import re
import json
import sys
sys.path.insert(1, 'C:\\Users\\Wicke\Desktop\\GIBT Draft 3')


def AmazonData(baseQuery):
    amazonSearchResults = GoogleSearch(baseQuery + ' site:amazon.com')
    print(amazonSearchResults.searchURL)

    @tryAndExcept
    def extractASIN(url):
        return re.search(r'dp/[\d\w]+', url).group().replace('dp/', '')

    amazonASINS = returnListWithoutNone(list(
        map(lambda url: extractASIN(url), amazonSearchResults.hrefs))
    )

    amazonData = list(
        threadMap(lambda asin: AmazonProduct(asin).data, amazonASINS))

    charactersToRemove = ['\u2605']

    with open(f'./AnalysisData/Amazon/{baseQuery}.json', 'w') as file:
        dataString = str(json.dumps(amazonData))

        for character in charactersToRemove:
            dataString = dataString.replace(character, '')

        dataString.encode('utf-8', 'ignore')
        file.write(dataString)
    # no matter how much time it takes, keep this because of testing purposes

    return amazonData
