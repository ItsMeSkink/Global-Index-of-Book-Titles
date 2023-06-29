from requests import get
from bs4 import BeautifulSoup
import time
import re
import random
import os
import sys

from globalFunctions import HEADERS
sys.path.insert(2, 'C:\\Users\\Wicke\\Desktop\\GIBT Draft 2')


class webProxyFile:
    filename = 'Proxying/Proxy Files/webScrappedProxies.txt'

    @classmethod
    def write(self, content):
        with open(self.filename, 'w') as file:
            file.write(content)

    @classmethod
    def writelines(self, list=list()):
        with open(self.filename, 'w') as file:
            file.writelines(list)

    @classmethod
    def append(self, content):
        with open(self.filename, 'a') as file:
            file.write(content)

    @classmethod
    def appendlines(self, list=list()):
        with open(self.filename, 'a') as file:
            file.writelines(list)

    @classmethod
    def read(self):
        with open(self.filename, 'r') as file:
            return file.read()

    @classmethod
    def readlines(self):
        with open(self.filename, 'r') as file:
            return file.readlines()


class archieveProxyFile(webProxyFile):
    filename = 'Proxying/Proxy Files/archievedProxies.txt'


class Proxying:
    # LOCAL FILES HANDLING
    @classmethod
    def getProxyFiles(self):
        '''simply returns the files in the "Proxy Files" folder'''
        files = os.listdir('Proxying/Proxy Files')
        return files

    @classmethod
    def getLocalProxies(self):
        '''getLocalProxies returns the proxies stored in the local files except for webScrappedProxies.txt'''
        files = self.getProxyFiles()
        files.remove('webScrappedProxies.txt')
        # files.remove('proxyArchieve.txt')
        files.remove('validProxies.txt')
        files.remove('archievedProxies.txt')
        # these files are not to be scanned and listed for proxies
        localProxies = set()

        for proxyFile in files:
            with open(f'Proxying/Proxy Files/{proxyFile}', 'r') as file:
                proxiesList = list(map(lambda proxyString: re.sub(
                    '\n', '', proxyString), file.readlines()))
                localProxies.update(proxiesList)

        return list(localProxies)

    # WEB SCRAPPING AND FILES HANDLING
    @classmethod
    def scrapWebProxies(self):
        '''scrapWebProxies would fundamentally/rawly just scrap the proxies avaiable on "sslproxies.org" and return the array for it. It would not store these proxies'''
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

    @classmethod
    def getWebProxies(self):
        '''getWebProxies() would return an array/list of proxies extracted from "webScrappedProxies.txt"'''

        textLines = webProxyFile.readlines()[2:]
        proxies = list(map(lambda proxystring: re.sub(
            '\n', '', proxystring), textLines))

        return proxies

    @classmethod
    def storeWebProxies(self):
        currentHour = f'Hour: {time.strftime("%H")}\n'
        lastHour = webProxyFile.readlines()[0]

        if (currentHour != lastHour):
            self.updateWebProxies()
            # the same function that was written here was used in the update function this being instead of being re-written, the entire function has been re-used
        else:
            print(
                f'Proxies would be updated at {int(time.strftime("%H")) + 1} o clock')

    @classmethod
    def updateWebProxies(self):
        '''Forcfully updates the proxy list in webScrappedProxies.txt'''
        currentHour = f'Hour: {time.strftime("%H")}\n'

        currentWebProxies = list(
            map(lambda proxyLines: proxyLines + '\n', self.getWebProxies()))
        currentArchieveProxies = archieveProxyFile.readlines()

        toArchieveProxies = set(currentWebProxies + currentArchieveProxies)
        # accounts for pre-existing proxies and new proxies and archieves unique ones
        archieveProxyFile.writelines(toArchieveProxies)

        webProxyFile.write(currentHour + '\n')
        # resets the web proxies file
        webProxyFile.appendlines(
            list(map(lambda proxyString: f'{proxyString}\n', self.scrapWebProxies())))
        # appends all the available proxies

    @classmethod
    def getAllProxies(self):
        return self.getWebProxies() + self.getLocalProxies()

    # RETURNS LOCAL, WEB, ALL PROXIES AS PROPERTY ATTRIBUTE
    @classmethod
    @property
    def web(self):
        return self.getWebProxies()

    @classmethod
    @property
    def local(self):
        return self.getLocalProxies()

    @classmethod
    @property
    def all(self):
        return self.getAllProxies()

    # storeWebProxies()
    # tries to update the proxies each time "Proxying" method is used statically or instancely


allProxies = Proxying.web


class getRequest:
    def __init__(self, url,):
        self.url = url

    @property
    def res(self):
        proxyAddress = random.choice(allProxies)
        allProxies.remove(proxyAddress)
        httpUrl = re.sub('https', 'https', self.url)
        # print(httpUrl)
        try:
            res = get(httpUrl, timeout=5, headers=HEADERS())
            if (res.status_code) == 200:
                return res
            else:
                return self.res
                # this "res" refers to successfull request
        except Exception as e:
            return self.res

    def json(self):
        return self.res.json()

    @property
    def content(self):
        return self.res.content

    @property
    def text(self):
        return self.res.text

    @property
    def headers(self):
        return self.res.headers

    @property
    def status_code(self):
        return self.res.status_code


Proxying.storeWebProxies()