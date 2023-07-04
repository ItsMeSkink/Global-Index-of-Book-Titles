from Scrappers.GoogleBooks import GoogleBooksSearch
from Scrappers.Google import GoogleSearch
from Culmination.Amazon import AmazonData
from Culmination.AbeBooks import AbeBooksData
from Algorithms.ExtractMostCommonPhrase import extractMostCommonPhrase
import time
import json
from concurrent.futures import ThreadPoolExecutor

isbns = [
    9780861542116, 9780753555637, 9781591842804, 9780008386597, 9780553175219, 9780099590088, 9789389053029, 9781422196021, 9789391165482, 9789332585348, 9781473695986, 9780141988511, 9781471409332, 9781471408656, 9781471407277, 9781250836540, 9781250759924, 9781250144553, 9781510105256, 9781250044433, 9781250027436, 9780552574235, 9780552577564, 9780007523528, 9780007523528, 9781250759627
]


# isbnInput = input('Input an ISBN: ')


def isbnTest(isbnInput):
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

    if (__name__ == '__main__'):
        with ThreadPoolExecutor() as executor:
            executor.submit(AmazonData, baseQuery)
            executor.submit(AbeBooksData, baseQuery)

    print(time.time() - initTime)


for isbn in isbns: 
    isbnTest(isbn)
