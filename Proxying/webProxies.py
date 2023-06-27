import re
import time
from bs4 import BeautifulSoup
from requests import get


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


def scrapAndStoreProxies():
    '''this would be structured as such to store proxies in a manner that each day/hour/after a limited time span the proxies would be automatically renewed'''

    with open('Proxying/Proxy Files/webScrappedProxies.txt', 'w'):
        # write statement would reset the entire file each time the functin is run
        with open('webScrappedProxies.txt', 'a') as appendFile:
            appendFile.write('Hour: ' + time.strftime('%H') + '\n\n')
            appendFile.writelines(
                list(map(lambda proxyString: proxyString + '\n', scrapProxies())))


def getScrappedProxies():
    with open('Proxying/Proxy Files/webScrappedProxies.txt', 'r') as file:
        fileProxies = file.readlines()[2:]
        fileProxies = list(map(lambda proxyString: re.sub(
            '\n', '', proxyString), fileProxies))
        return (fileProxies)


def checkScrapStoreProxies():
    with open('Proxying/Proxy Files/webScrappedProxies.txt', 'r') as file:
        fileLines = file.readlines()
        currentHour = f"Hour: {time.strftime('%H')}\n"
        lastHour = (fileLines[0])

        if lastHour != currentHour:
            with open('Proxying/proxyArchieve.txt', 'a') as archieveFile:
                archieveFile.writelines(
                    list(map(lambda proxyString: proxyString + '\n', getScrappedProxies())))
                # this would store all the last proxies in the acrhieve file

            scrapAndStoreProxies()

        else:
            print(
                f'Proxies would be updated at {int(time.strftime("%H")) + 1} \'o\' clock')
