import time
from ScrappingClasses.amazonWebpage import amazonWebpage
from ScrappingClasses.abebooksWebpage import abeBooksWebpage
from ScrappingClasses.googleWebpage import googleResults, googleWebpage


# print(amazonWebpage('https://www.amazon.com/Python-Programming-Taneja-Sheetal-Naveen/dp/9332585342').aboutAuthors)
# print(googleWebpage('Buy 9789332585348 Book').titles)
# print(googleWebpage('Buy 9789380703688').titles)
# print(amazonWebpage('https://www.amazon.com/Origin-Species-Penguin-Classics/dp/0140439129/ref=sr_1_1_sspa?keywordsof+species').title)


# print(amazonWebpage('https://www.amazon.com/errors/validateCaptcha'))


# abe = (abeBooksWebpage(
#     'https://www.abebooks.com/servlet/BookDetailsPL?bi=31450032895&searchurl=ds%3D20%26kn%3Don%2Bof%2Bthe%2Borigin%2Bof%2Bspecies%26sortby%3D17&cm_sp=snippet-_-srp1-_-image1'))
# abe = (abeBooksWebpage(
#     'https://www.abebooks.com/9789332585348/Python-Programming-Modular-Approach-NAVEEN-9332585342/plp'))

# print((abe.data))

# while True:
#     print(bookResults.webHeaders)
#     try:
#         print(bookResults.titles)
#         print('try')
#     except:
#         try:
#             print(bookResults.titles)
#             print('except')
#             exceptCount += 1
#         except Exception as e:
#             print(e)
#             print(exceptCount)
#             break


# def getGoogleResultsRecurring(query):
#     bookResults = (googleWebpage(query))
#     try:
#         data = (bookResults.data)

#         if data == []:
#             getGoogleResultsRecurring()
#         # variable declaration is necessary
#         return (data)
#     except Exception as e:
#         getGoogleResultsRecurring()


# print(getGoogleResultsRecurring('Buy Python Programming A Modular Approach'))

results = (googleResults('Buy Python Programming : A Modular Approach book - SapnaOnline site:amazon.com'))

print(results.titles)
print(results.hrefs)

# I have observed that the first time that we print the data can print a blank but if we print it the second time using a second call it can yield a useful data.
# An error I'm getting is related to lxml and it returns a blank array what I have done to solve it is reoccur the function if it returns a blank array other than that any exception would also reoccur the function.
# Very successful outcome of applying a recurring algorithm to retrieve the titles for definite Results is that no matter whattime it takes it would definitely return the titles or the data