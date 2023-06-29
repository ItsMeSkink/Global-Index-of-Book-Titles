import re
from Scrappers.AbeBooksBook import AbeBooksBook, AbeBooksSearchPage
from Scrappers.AmazonProduct import AmazonProduct
from Scrappers.GoogleBooksAPI import GoogleBooksSearch
from Scrappers.GoogleSearch import GoogleSearch
from globalFunctions import mapping


googleBooks = GoogleBooksSearch(9781591842804)
titleAuthor = googleBooks.extractTitleAuthor()
baseQuery = f"{titleAuthor['title']} by {titleAuthor['author']}"
similarGoogleBooks = googleBooks.similars

amazonHrefs = GoogleSearch(f'{baseQuery} site:amazon.com').hrefs
abebooksHrefs = GoogleSearch(f'{baseQuery} site:abebooks.com').hrefs

abeBooksResultsData = list(mapping.processes(lambda abebookshref: AbeBooksBook(abebookshref).data, abebooksHrefs))
amazonBookResultsData = list(mapping.processes(lambda amazonproducthref: AbeBooksBook(amazonproducthref).data, amazonHrefs))


