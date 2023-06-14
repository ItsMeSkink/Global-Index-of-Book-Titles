from ScrappingClasses.amazonWebpage import amazonWebpage
from ScrappingClasses.abebooksWebpage import abeBooksWebpage
from ScrappingClasses.googleWebpage import googleWebpage


# print(amazonWebpage('https://www.amazon.com/Python-Programming-Taneja-Sheetal-Naveen/dp/9332585342').aboutAuthors)
# print(googleWebpage('Buy 9789332585348 Book').titles)
# print(googleWebpage('Buy 9789380703688').titles)
# print(amazonWebpage('https://www.amazon.com/Origin-Species-Penguin-Classics/dp/0140439129/ref=sr_1_1_sspa?keywordsof+species').title)


# print(amazonWebpage('https://www.amazon.com/errors/validateCaptcha'))


abe = (abeBooksWebpage(
    'https://www.abebooks.com/servlet/BookDetailsPL?bi=31450032895&searchurl=ds%3D20%26kn%3Don%2Bof%2Bthe%2Borigin%2Bof%2Bspecies%26sortby%3D17&cm_sp=snippet-_-srp1-_-image1'))
# abe = (abeBooksWebpage(
#     'https://www.abebooks.com/9789332585348/Python-Programming-Modular-Approach-NAVEEN-9332585342/plp'))

print((abe.data))
