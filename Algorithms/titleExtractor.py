import re


titleList = ['Buy On the origin of species by Charles Darwin online in india',
             'ON THE ORIGIN OF SPECIES - BooksBonanza',
             'On the Origin of Species (Charles Darwin) (Paperback) - BooksTech', 'On the Origin of Species (Charles Darwin) (Paperback)', 'On the Origin of Species - Deen The Bookman', 'Buy On the Origin of Species (Charles Darwin) Book Online at Low']
# titleList = []


def extractTitleFromStrings(titleList):
    largeString = " "
    for title in titleList:
        largeString += title.lower() + ' '

    nonSymbolizedstring = re.sub(r'[^\w+ ]', '', largeString)
    # here we remove all the symbols that are not used in the title

    uniqueWords = set(nonSymbolizedstring.split(' '))
    # here we get all the words that are used in the dataset

    wordTimesDict = {}
    for word in uniqueWords:
        if word != '':
            numberOfTimes = nonSymbolizedstring.count(f' {word} ')
            wordTimesDict[word] = numberOfTimes
    # this returns a dictionary which mentioned how many times a word has been repeated in the dataset

    commonWords = list()
    substractValue = 0
    while commonWords == list():
        for key, value in wordTimesDict.items():
            if value >= len(titleList) - substractValue:
                commonWords.append(key)
        substractValue += 1
    # sometimes there are results all of which doens't mention the book title. So we run a while loop untill we get the most common words used, hence the title

    indexDictionary = dict()
    for term in commonWords:
        termIndex = titleList[0].lower().split(' ').index(term)
        indexDictionary[termIndex] = term
