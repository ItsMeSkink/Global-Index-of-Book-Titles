from concurrent.futures import ThreadPoolExecutor
import json
from mimetypes import init
from random import choice
import re


def readJSONFile(attribute):
    with open('globalVariables.json', 'r') as jsonFile:
        return json.loads(jsonFile.read())[attribute]

# ------------------------------------------------------------------- #


def extractText(text):
    return re.sub(r'<.*?>', '', str(text))


def extractURL(a, suffix=r"&sa=U&ved"):
    try:
        return (re.search(r"https://[\w\W]+" + suffix, a['href']).group().replace(suffix, ''))
    except:
        return a['href']
    # .group() returns the matched string

# ------------------------------------------------------------------- #

# reference
# "User-Agent":"Mozilla/4.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"

# go not use fake headers


def HEADERS():
    a = choice(range(1, 4))
    b = choice(range(1, 11))
    c = choice(range(500, 537))
    d = choice(range(1, 36))
    e = choice(range(40, 44))
    f = choice(range(2000, 2403))
    g = choice(range(140, 157))

    headersList = [
        f'Mozilla/{a}.0',
        f'X11; Linux x86_64 KHTML/ like Gecko',
        f'AppleWebkit/{c}.{d} Safari/{c}.{d}',
        f'Chrome/{e}.0.{f}.{g}',
    ]

    numberOfHeaders = range(choice(range(1, 4)))
    customHeader = ""
    for _ in numberOfHeaders:
        header = choice(headersList)
        headersList.remove(header)

        customHeader += f"{header} "

    # return readJSONFile('headers')

    return {
        "User-Agent": customHeader.strip(),
        "Accept-Langauge": 'en-US'
    }

# ------------------------------------------------------------------- #


def threadMap(method, list):
    executor = ThreadPoolExecutor()
    return executor.map(method, list)
