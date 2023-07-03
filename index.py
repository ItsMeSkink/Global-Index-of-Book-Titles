from concurrent.futures import ThreadPoolExecutor
import json
import multiprocessing
import time
from Algorithms.ExtractMostCommonPhrase import extractMostCommonPhrase
from Culmination.AbeBooks import AbeBooksData
from Culmination.Amazon import AmazonData
from Scrappers.Google import GoogleSearch
from Scrappers.GoogleBooks import GoogleBooksSearch

isbnInput = input('Input an ISBN: ')
try:
    book = GoogleBooksSearch(isbnInput)
    extract = book.extractTitleAndAuthor()
except:
    bookTitle = extractMostCommonPhrase(GoogleSearch(isbnInput).titles)
    # extracts the title from Google SERP
    book = GoogleBooksSearch(title=bookTitle)
    # fetches similar books from Google Books
    extract = book.extractTitleAndAuthor()
    # yields the actual useful extract

baseQuery = f"{extract['title']} by {extract['author'].split(' ')[-1]}"
print(baseQuery)

with open(f'AnalysisData/GoogleBooks/{baseQuery}.json', 'w') as file:
    '''stores the data in GoogleBooks Analysis folder'''
    currentBook = list()

    if len(book.data) == 1:
        currentBook = book.data
    else:
        currentBook = [
            {
                "title": extract['title'],
                "author": extract['author'],
                "isbn": int(isbnInput),
            }
        ]

    file.write(str(json.dumps(currentBook + book.similars.data)))

initTime = time.time()

AmazonData(baseQuery)
AbeBooksData(baseQuery)

print(time.time() - initTime)
