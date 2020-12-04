import re

def printMatching(stringthing):
    if re.match(r'\d{1,}[.]\d{1,}$',stringthing) != None: 
        print("\"" + stringthing + "\" matches the pattern: a double")
    elif re.match(r'\d{1,}$',stringthing) != None: 
        print("\"" + stringthing + "\" matches the pattern: an int")
    elif re.match(r'\d{1,}[.]\d{1,}$',stringthing) != None: 
        print("\"" + stringthing + "\" matches the pattern: a float")
    elif re.match(r'\d{1,}[.]\d{1,}[f]$',stringthing) != None: 
        print("\"" + stringthing + "\" matches the pattern: a float ending in f")
    elif re.match(r'[A-Z][a-z]{1,}$',stringthing) != None: 
        print("\"" + stringthing + "\" matches the pattern: a capital, then lowercase letters")
    elif re.match(r'[A-Z]{1,}[a-z]{1,}\d{1,}$',stringthing) != None: 
        print("\"" + stringthing + "\" matches the pattern: capital, then lowercase letters, then numbers")
    elif re.match(r'\d{1,}[A-Za-z]{1,}$',stringthing) != None:
        print("\"" + stringthing + "\" matches the pattern: numbers then letters")
    else:
        print(stringthing + "could not interpret")
    return

str0 = "452de"
str1 = "HEll0" 
str2 = "10"
str3 = "10.1"
str4 = "10.2f"
str5 = "9999999"
str6 = "7"
str7 = "24314523452"
str8 = "4543"
str9 = "685784132.541684"

printMatching(str0)
printMatching(str1)
printMatching(str2)
printMatching(str3)
printMatching(str4)
printMatching(str5)
printMatching(str6)
printMatching(str7)
printMatching(str8)
printMatching(str9)