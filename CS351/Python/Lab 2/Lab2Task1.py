import re

# \s == Space
# * == 0 or more instances
# ? == 0 or 1 instance
# + == 1 or more instances
# () == grouping or including
# {1,5} == 1 to 5 times of instances
# {5} == 5 instances

# [a-z] == a letter from a to z, a range
# [a-z][a-z] == two letters next to each other
# \d or [0-9] == a digit
# \w == a number or a character [a-zA-Z0-9]

# . == any thing
# ^ == except
print(re.findall(r'\d{1,5}', 'this 45 is a random string asr234a 98asd82 23 d*&@'))
if(re.match(r'\d\s\w+', '4 street') != None ):
    print("a match found")
else:
    print("no match")
    
if(re.match(r'\d\s\w+', '4th street') != None ):
    print("a match found")
else:
    print("no match")
#re.match & re.search

myregex= re.compile('\d+')
result=myregex.search ('101 Math; 102 Biology; 105 CS')
print (result)
print('Starting Position: ', result.start())
print ('End Position', result.end())





#identifier: start with a letter, followed by any number of letters or numbers, followed by space


#integer: any number of digits


#float: digits followed by . followed by digits, followed by space