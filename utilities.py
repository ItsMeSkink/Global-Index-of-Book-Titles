from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import lru_cache, reduce
import json
from random import choice
import re


@lru_cache(maxsize=None)
def readJSONFile(filename):
    with open(filename, 'r') as file:
        content = file.read()
        jsonData = json.loads(content)
        return jsonData


def tryAndExcept(function):
    '''this is a decorator function which will automatically pass the below function in try and except logic'''
    def mod(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except:
            pass

    return mod


def headers():
    '''returns a random header user-agent'''
    a = choice(range(1, 4))
    b = choice(range(1, 11))
    c = choice(range(500, 537))
    d = choice(range(1, 36))
    e = choice(range(40, 44))
    f = choice(range(2000, 2403))
    g = choice(range(140, 157))

    headersList = [
        f'X11; Linux x86_64 KHTML/ like Gecko',
        f'AppleWebkit/{c}.{d} Safari/{c}.{d}',
        f'Chrome/{e}.0.{f}.{g}',
    ]

    numberOfHeaders = range(choice(range(1, 3)))
    customHeader = "Mozilla/5.0"
    for _ in numberOfHeaders:
        header = choice(headersList)
        headersList.remove(header)

        customHeader += f"{header} "

    return {
        "User-Agent": customHeader.strip(),
        "Accept-Langauge": 'en-US'
    }


def threadMap(method, list):
    executor = ThreadPoolExecutor()
    return executor.map(method, list)


def processMap(method, list):
    executor = ProcessPoolExecutor()
    return executor.map(method, list)


def extractText(text):
    return re.sub(r'<.*?>', '', str(text)).strip()


def extractURL(a, suffix=r"&sa=U&ved"):
    try:
        return (re.search(r"https://[\w\W]+" + suffix, a['href']).group().replace(suffix, ''))
    except:
        return a['href']
    # .group() returns the matched string


def returnListWithoutNone(array):
    return list(filter(lambda item: True if item != None else False, array))


def concatenate(array):
    return list(reduce(lambda x, y: x + y, array))
