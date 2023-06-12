import json
import re


def readJSONFile(attribute):
    with open('globalVariables.json', 'r') as jsonFile:
        return json.loads(jsonFile.read())[attribute]


HEADERS = (readJSONFile('headers'))

def extractText(text):
    return re.sub(r'<.*?>', '', str(text))
    # return str(str(text).split('>')[2].split('<')[0])
