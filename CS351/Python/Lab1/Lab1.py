# Problem 1
def printHello():
    print("Hello World")
    return

# Problem 2
def someVars():
    int0 = 0
    int1 = 1
    float0 = 0.0
    float1 = 0.1

    print((int0+int1+float0+float1))
    return

# Problem 3
def myLis():
    myList = [1, 2, 3, 4, 5]
    print(myList)
    return

# Problem 4
def printStr(input_str1, input_int1):
    print(input_str1+str(input_int1))
    return

# Problem 5
def returnSum(input1, input2):
    return input1 + input2

# Problem 6
def goOverList(myList):
    for x in myList:
        print(x)
    return

def goOverList1():
    for x in range(10,18):
        print(x)
    return

def goOverList2(myList):
    for x in myList:
        print(x*2)
    return

def goOverList3(myList):
    resList = []
    for x in myList:
        x *= 2
        resList.append(x)
    return resList

# Problem 7
def goOverListw(myList):
    i = 0
    while i < len(myList):
        print(myList[i])
        i+=1
    return

def goOverList1w():
    i = 10
    while i < 18:
        print(i)
        i += 1
    return

def goOverList2w(myList):
    i = 0
    while i < len(myList):
        print(myList[i] * 2)
        i += 1
    return

def goOverList3w(myList):
    resList = []
    i = 0
    while i < len(myList):
        x = myList[i]*2
        resList.append(x)
        i += 1
    return resList