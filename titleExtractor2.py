import re


titleList = ['Python Programming, 1e Reviews &amp; Ratings - Amazon.in', 'Buy Python Programming : A Modular Approach book - SapnaOnline', 'Python Programming: A modular approach, 1/e Sheetal Taneja', 'Python Programming - A Modular Approach with Graphics ... - Flipkart', 'Python Programming |A modular approach | First Edition | By ...', 'Python Programming: A Modular Approach - Softcover - AbeBooks', 'Python Programming a Modular Approach With Graphics Database ...', 'Python Programming: A Modular Approach by Kumar And Taneja ...', 'Python Programming A Modular Approach 2017 Edition - Meripustak', 'Buy Python Programing, 9789332585348 at Best Price Online', 'Buy Python Programming - A Modular Approach with Graphics ...', 'Python Programming A Modular Approach with Graphics Database ...', 'Python programming : a modular approach = with graphics ...', 'python programming: a modular approach with graphics database ...', 'Python programming : › Central Library, Tezpur University catalog', '[PDF] PTG Catalogue - Pearson | India', 'Details for: Python programming - BITS Hyderabad catalog', 'Python Programming - A Modular Approach with Graphics ...', 'Python Programming |A modular approach | First Edition | By Pearson',
             'Fast Ship Python Programming 1e by Taneja Sheetal and Kumar ...', 'SHEETAL TANEJA, NAVEEN KUMAR | PEARSON | Pragationline.com', 'Python programming : a modular approach - macfast', 'A Modular Approach with Graphics, Database, Mobile and Web ...', 'Python Programming 1st Edition - Mysuperday.in', 'PYTHON PROGRAMMING A MODULAR APPROACH WITH ...', 'PYTHON PROGRAMMING - A MODULAR APPROACH', 'Expographic Books - Expographic Book shop', 'Python Programming: A modular approach', '[PDF] Books Procured During 2019-2020.pdf - Deshbandhu College', '[XLS] Sheet1', '[PDF] Samrat Ashok Technological Institute, Vidisha, MP', 'Library - Kendriya Vidyalaya Kanjikode - Books are just the beginning!', 'Request for Quotation', 'sitemap-1-24.xml - Atlantic Publishers', 'Python Programming: A Modular Approach Paperback 1st Edition', '[PDF] 96 Annual Report 2018-2019 Part-I - Delhi University', '[PDF] CENTRAL LIBRARY - Vignan University', 'Updated Price List for the month of August 2018 - DocPlayer.net', 'Catalog Cse 2019 Final | PDF | Theory Of Computation - Scribd', 'Price List - May 2019 | PDF | Discrete Mathematics - Scribd', 'Python programming a modular approach', 'Python Programming: A Modular Approach']


buyString = ""
currentIndex = 0

while buyString == "":
    buyMatch = re.match(r'^Buy[\w+\W]+', titleList[currentIndex])

    if (buyMatch != None):
        buyString = buyMatch.string
        break
    else:
        currentIndex += 1

print(buyString, 'amazon.com')
