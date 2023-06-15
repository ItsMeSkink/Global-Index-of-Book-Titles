from concurrent.futures import ProcessPoolExecutor
import time


numberList = range(1, 100)


executor = ProcessPoolExecutor()


def square(number):

    if (number > 15):
        raise ValueError('above 15')
        
    try:
        return (number ** 2)
    except:
        pass


if __name__ == "__main__":
    print(list(executor.map(square, range(20))))
