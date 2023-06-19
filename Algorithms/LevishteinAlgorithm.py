DPTable = {}

def lev(string1, string2):

    string1 = " " + string1
    xAxisLength = len(string1)
    # + 1 is for blank
    # the result would be 11
    # string 2 on y-axis

    string2 = " " + string2
    yAxisLength = len(string2)
    # + 1 is for blank
    # this results would be 10
    # string 1 on x-axis

    for y in range(yAxisLength):
        for x in range(xAxisLength):
            if(x == 0 or y==0):
                DPTable[(0,y)] = y
                DPTable[(x,0)] = x

            else:
                if(string1[x] == string2[y]):
                    DPTable[(x,y)] = DPTable[(x-1), (y-1)]
                else:
                    # when the characters are not equal
                    previousNumberOfOperations = [DPTable[(x-1, y)], DPTable[(x, y-1)], DPTable[(x-1,y-1)]]
                    previousNumberOfOperations.sort()
                    # print(previousNumberOfOperations)
                    DPTable[(x,y)] = previousNumberOfOperations[0] + 1

    return DPTable[(xAxisLength -1, yAxisLength -1 )]

print(lev('programming','programing'), ' is the levishtein distance')