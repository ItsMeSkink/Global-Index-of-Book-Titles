import json
from mimetypes import init
from random import choice
import re


def readJSONFile(attribute):
    with open('globalVariables.json', 'r') as jsonFile:
        return json.loads(jsonFile.read())[attribute]


# HEADERS = (readJSONFile('headers'))


def extractText(text):
    return re.sub(r'<.*?>', '', str(text))
    # return str(str(text).split('>')[2].split('<')[0])

# "User-Agent":"Mozilla/4.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"


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
        f'X{b}; Linux x86_64 KHTML/ like Gecko',
        f'AppleWebkit/{c}.{d} Safari/{c}.{d}',
        f'Chrome/{e}.0.{f}.{g}',
    ]

    numberOfHeaders = range(choice(range(1, 4)))
    customHeader = ""
    for _ in numberOfHeaders:
        header = choice(headersList)
        headersList.remove(header)

        customHeader += f"{header} "

    return readJSONFile('headers')

    return {
        "User-Agent": customHeader.strip(),
        "Accept-Langauge": 'en-US'
    }

# print(HEADERS())