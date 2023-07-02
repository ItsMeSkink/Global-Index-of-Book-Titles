import sys
sys.path.insert(1, 'C:\\Users\\Wicke\Desktop\\GIBT Draft 3')
from Scrappers.requestOrigins import Smartproxy
from utilities import readJSONFile, tryAndExcept

url = "https://scrape.smartproxy.com/v1/tasks"


class GoogleSearch(Smartproxy):
    def __init__(self, query):
        self.payload = {
            "target": "google_search",
            "query": query,
            "parse": True,
            "domain": "com",
            "locale": "en",
            "google_results_language": "en",
            "geo": "India",
            "device_type": "desktop",
            "page_from": "1",
            "num_pages": "100",
            "google_nfpr": True,
            "google_safe_search": True
        }
        self.authorisationCode = readJSONFile('codes.json')['SERP']
        self.inContent = self.res.json()['results'][0]['content']
        self.results = self.inContent['results']

    @property
    def imagesData(self):
        imageResults = self.results['images']['items']

        structuredResults = list(map(lambda item: {
            "title": item['alt'],
            "href": item['source']
        }, imageResults))

        return structuredResults

    @property
    def organicData(self):
        organicResults = self.results['organic']

        structuredResults = list(map(
            lambda item: {
                "title": item['title'],
                "href": item['url']
            }, organicResults
        ))

        return structuredResults

    @property
    def titles(self):
        return list(map(lambda item: item['title'], self.data))

    @property
    def hrefs(self):
        return (list(map(lambda item: item['href'], self.data)))

    @property
    def data(self):
        return self.imagesData + self.organicData

    @property
    @tryAndExcept
    def searchURL(self):
        return self.res.json()['results'][0]['url']

    def json(self):
        return self.data
