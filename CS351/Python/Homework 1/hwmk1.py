# Name: Kevyn Higbee
# Assignment: Homework 1
# Date: 6 Sept, 2019
# Course: CS351

import random   # for last problem

#############################
#   FUNCTION DEFINITIONS    #
#############################

# Problem 1
def countHello(input_int):
    i = 1
    while i <= input_int:
        print(str(i)+"th Hello")
        i += 1
    return

# Problem 2
def smallerValue(input1, input2):
    if input1 < input2:
        return input1
    else:
        return input2

# Problem 3
def my_len(myList):
    number = 0
    for i in myList:
         number += 1
    return number

# Problem 4
def cate_letters(myList):
    two = []
    three = []
    four = []

    for x in myList:
        if len(x) == 2:
            two.append(x)
        elif len(x) == 3:
            three.append(x)
        elif len(x) == 4:
            four.append(x)

    return two, three, four

# Problem 5
def two_string(str1,str2):
    index = 0
    while index < len(str1) or index < len(str2):
        val_1 = "empty" if index >= len(str1) else str1[index] 
        val_2 = "empty" if index >= len(str2) else str2[index]
        print("The elements at index " + str(index) 
            + " from string 1 is " + val_1
            + ", from string 2 is " + val_2)
        index += 1
    return

# Problem 6
def two_strings(str1, str2):
    index = 0
    oddstring = ""
    evenstring = ""
    while index < len(str1) or index < len(str2):
        if (int(str2[index])%2) == 0:
            evenstring += str1[index]
        else:
            oddstring += str1[index]
        index += 1
    return evenstring, oddstring

# Problem 7
def love6(inta,intb):
    return ((abs(inta+intb)==6) | (abs(inta-intb)==6) | (abs(inta)==6) | (abs(intb) == 6))

# Problem 8
def check_legit_ISBN(isbn):
    value = 0
    index = 0
    while index < 10:
        value += (10-index) * isbn[index]
        index += 1
    return "Legit" if value%11==0 else "Not Legit"

def format_ISBN(ISBNlis):
    isbn = "ISBN "
    index = 0
    while index < (len(ISBNlis)-1):
        isbn += str(ISBNlis[index])
        index += 1
    return isbn + "-" +  str(ISBNlis[index])

def checksum_ISBN(partISBN):
    value = 0

    while value < 10 and check_legit_ISBN(partISBN + [value]) == "Not Legit":
        value += 1

    if value < 10:
        partISBN.append(value)
        print("The Correct checksum digit is " + str(value)
                + ". Now we have a legit ISBN: " + format_ISBN(partISBN))
    
    return value < 10

def generate_ten_ISBN():
    x = 0
    while x < 10:
        tmpISBN = []
        for y in range(9):
            tmpISBN.append(random.randint(0,9))
        if checksum_ISBN(tmpISBN) :
            x += 1
        else:
            x -= 1
    return

######################
#   FUNCTION CALLS   #
######################

countHello(4)

print(smallerValue(1,2))
print(smallerValue(4,-1))
print(smallerValue(1,1))

print(my_len("Hello World"))

print(cate_letters(['rt','asdf','ton','er','user']))

two_string("Hello","World")

two_strings("helloworld","2435232399")

print(love6(6, 4))
print(love6(4, 5))
print(love6(1, 5))

generate_ten_ISBN()