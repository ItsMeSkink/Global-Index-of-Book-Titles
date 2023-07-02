from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import time
from Culmination.AbeBooks import AbeBooksData
from Culmination.Amazon import AmazonData

from Scrappers.GoogleBooks import GoogleBooksSearch


book = GoogleBooksSearch(input('Input an ISBN: '))
extract = book.extractTitleAndAuthor()

baseQuery = f"{extract['title']} by {extract['author'].split(' ')[-1]}"
print(baseQuery)

initTime = time.time()
if (__name__ == '__main__'):
    executor = ThreadPoolExecutor()
    # executor.submit(AmazonData, baseQuery)
    # executor.submit(AbeBooksData, baseQuery)
    AmazonData(baseQuery)
    AbeBooksData(baseQuery)
    # amazon = multiprocessing.Process(target=AmazonData, args=[baseQuery])
    # abeBooks = multiprocessing.Process(target=AbeBooksData, args=[baseQuery])
    # amazon.start()
    # abeBooks.start()

print(time.time() - initTime)