import threading
import queue
from requests import Session, get
from termcolor import colored
from globalFunctions import threadMap


proxyQueue = queue.Queue()
proxies = []
validProxies = []

with open('proxies.txt', 'r') as file:
    proxies = file.read().split('\n')

    # for proxy in proxies:
    #     proxyQueue.put(proxy)

# quene up all the proxies addresses

index = 0
reProxyNumbers = dict()


def checkProxy(proxyLink):
    global index
    global reProxyNumbers
    proxyLink = 'http://' + proxyLink

    try:
        res = get('http://ipinfo.io/json', proxies={
            "http": proxyLink,
            'https': proxyLink
        })

        if (res.status_code == 200):
            print(colored(str(index) + ') ' + proxyLink, 'green'))
            print(res.json()['country'], res.json()['reigon'])
            with open('validProxies.txt', 'a') as file:
                file.write(proxyLink + '\n')

            index += 1
            return proxyLink

    except Exception as e:
        print(colored(str(index) + ') ' + proxyLink, 'red'))
        index += 1

a = list(threadMap(checkProxy, proxies))

print(a)
print(validProxies)

# def checkProxies():
#     global q
#     while not q.empty():
#         proxy = q.get()
#         # each time the for loop is run, it would use a different link

#         try:
#             res = requests.get('http://ipinfo.io/json', proxies={
#                 "http": proxy,
#                 "https": proxy
#             })
#             if (res.status_code == 200):
#                 print(proxy)
#                 validProxies.join(proxy)
#         except:
#             continue

# for _ in range(10):
#    thread = threading.Thread(target=checkProxies).start()


# use 10 threads to perform the proxies
# but the checking wouldn't be repetitive because the "queue" is constant and the "popping" is continuos


print(validProxies)
