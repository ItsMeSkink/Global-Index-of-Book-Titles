from concurrent.futures import ThreadPoolExecutor
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

# initTime = time.time()
    # executor = ThreadPoolExecutor()
    # executor.submit(AmazonData, baseQuery)
    # executor.submit(AbeBooksData, baseQuery)
    # AmazonData(baseQuery)
# AbeBooksData(baseQuery)
    # amazon = multiprocessing.Process(target=AmazonData, args=[baseQuery])
    # abeBooks = multiprocessing.Process(target=AbeBooksData, args=[baseQuery])
    # amazon.start()
    # abeBooks.start()

# print(time.time() - initTime)