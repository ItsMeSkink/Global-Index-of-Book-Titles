import json


filename = 'AnalysisData\AbeBooks\Wings of Fire by Kalam.json'
with open(filename, 'r') as readFile:
    jsonData = json.loads(readFile.read())
    settedData = list(set(jsonData))
    with open(filename, 'w') as writeFile:
        writeFile.write(str(json.dumps(settedData)))
