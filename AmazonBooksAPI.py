from termcolor import colored
from ScrappingClasses import amazonWebpage, googleWebpage
from concurrent.futures import Executor, ThreadPoolExecutor
executor = ThreadPoolExecutor()


# isbnInput = int(input('Enter ISBN: '))
isbnInput = 9789380703688
isbnInput = 9789332585348


isbnQueryResults = googleWebpage(f'Buy "{isbnInput}" Book')
print(isbnQueryResults.titles)
n = 0
print(len(isbnQueryResults.titles))

while n < len(isbnQueryResults.titles):
    buyQueryResults = googleWebpage(
        isbnQueryResults.titles[n] + ' site:amazon.com')

    try:
        amazonQueryResults = buyQueryResults.hrefs
        print(amazonQueryResults, 'in try for amazon web scrap')
        try:
            # appropriate results
            print()
            # print(amazonQueryResults[0])
            amazonScrap1 = (amazonWebpage(amazonQueryResults[0]))
            # amazonScrap1 = amazonWebpage(amazonQueryResults[0])
            # print('title')
            # executor.submit(print, amazonScrap1.title)
            # print('authors')
            # executor.submit(print, amazonScrap1.authors)
            # print('description')
            # executor.submit(print, amazonScrap1.description)
            # print('publisher')
            # executor.submit(print, amazonScrap1.publisher)
            # print('thumbnail')
            # executor.submit(print, amazonScrap1.thumbnail)
            # print('about authors')
            # executor.submit(print, amazonScrap1.aboutAuthors)
            # print('about pages')
            # executor.submit(print, amazonScrap1.pages)

            print('title')
            print(amazonScrap1.title)
            print('authors')
            print(amazonScrap1.authors)
            print('description')
            print(amazonScrap1.description)
            print('publisher')
            print(amazonScrap1.publisher)
            print('thumbnail')
            print(amazonScrap1.thumbnail)
            print('about authors')
            print(amazonScrap1.aboutAuthors)
            print('pages')
            print(amazonScrap1.pages)

            print(colored('results for ' +
                  isbnQueryResults.titles[n] + ' site:amazon.com', 'green'))
            break

        except Exception as e:
            # Inappropriate Results
            print(colored(e, 'red'))

            if(e == 'You have been CAPTCHAd, change header'):
                break
            # finishes the program because it isn't the error of data error but runtime error
            print()
            print(colored('in except in except for inappropriate results for ' +
                  isbnQueryResults.titles[n] + ' site:amazon.com', 'red'))
            print()
            n += 1

    except:
        print()
        print(colored('in except for no results for ' +
              isbnQueryResults.titles[n] + ' site:amazon.com', 'red'))
        n += 1
        print()
        # no results
