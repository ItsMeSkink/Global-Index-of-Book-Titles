from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import multiprocessing
import os
import random
import re
import time
from bs4 import BeautifulSoup

from requests import Response, get

proxyFiles = os.listdir('Proxy Files')

localProxies = set()
for proxyFile in proxyFiles:
    with open(f'{proxyFile}', 'r') as file:
        proxySet = file.readlines()
        proxySet = list(map(lambda proxyString: re.sub(
            '\n', '', proxyString), proxySet))
        localProxies.update(proxySet)


def scrapProxies():
    res = get('https://www.sslproxies.org/')

    soup = BeautifulSoup(res.text, 'lxml')

    proxyTable = soup.select_one(
        'table.table.table-striped.table-bordered tbody')

    proxyDetails = proxyTable.select('tr')
    # this would select the entire column which contains the details of the proxy address and yield the list of proxies row contents details.
    webScrappedProxies = list()

    for detail in proxyDetails:
        proxyDetailRow = detail.select('td')
        # this yields an list "td"s in a single "tr" for every "tr" (in for loop)

        def getProxyAttribute(attr):
            '''chose from the attribute in the tableContents'''
            tableContents = {
                "IP Address": 0,
                "Port": 1,
                "Code": 2,
                "Country": 3,
                "Anonymity": 4,
                "Google": 5,
                "Https": 6,
                "Last Checked": 7,
            }
            return proxyDetailRow[tableContents[attr]].text

        proxyFormat = f"{getProxyAttribute('IP Address')}:{getProxyAttribute('Port')}"

        if getProxyAttribute('Https') == 'yes':
            webScrappedProxies.append(proxyFormat)

    return webScrappedProxies
    # this would return a list of proxies scraped from the "sslproxies.org" website



class getRequest:
    def __init__(self, url, headers=dict(), proxy=dict()):
        self.url = url
        self.headers = headers
        self.proxy = proxy

    @property
    def res(self):
        proxy = random.choice(localProxies)
        localProxies.remove(proxy)

        try:
            res = get(self.url, proxies={
                      'http': f'http://{proxy}'}, timeout=3)

            if (res.status_code) == 200:
                return res
            else:
                return self.res
                # this "res" refers to successfull request
        except:
            return self.res

    def json(self):
        return self.res.json()

    def content(self):
        return self.res.content

    def text(self):
        return self.res.text

    def headers(self):
        return self.res.headers


# res = getRequest('http://ipinfo.io/json')
# initTime = time.time()
# print(res.json())

# print(time.time() - initTime)
