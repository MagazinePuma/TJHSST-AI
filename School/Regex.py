import re
def num_31(str):
    # Current test checks if the string is '0'
    pattern = "^0$|^10[10]$" #notice that python does not want / /
    match = re.match(pattern, str)
    print ("string is either 0, 100, or 101: ", match != None)

def num_32(str):
    # Current test checks if the string is '0'
    print ("string is a binary string:", re.match("^[01]*$", str) != None)
# Pre-condition: input is a binary string, so you do not need to check if it's a binary or not.
def num_33(str):
    pattern = '0$'
    print ("string is an even binary number:", re.search(pattern, str, re.MULTILINE) != None)

def num_34(str):
    # Current test searches words with 'a'
    pattern = "\w*[aeiou]\w*[aeiou]\w*"
# Notice that python does not support /i in the pattern.
# Use re.I for case insensitive when you match(exact same) or search(has one or more)
    print ("there's a word at least two vowels:", re.search(pattern, str, re.I) != None)

def num_35(str):
    # ^1[^- ]*[01]+0$
    pattern = "^1?[01]*0$"
    print ("even binary integer string:", re.search(pattern, str, re.S) != None)

def num_36(str):
    pattern = ""
    print ("binary string including 110:", re.match(pattern, str) != None)

def num_37(str):
    pattern = "^.{2,4}$"
    print ("length at least two, but at most four:", re.search(pattern, str, re.MULTILINE) !=
None)

def num_38(str):
    # /^\d{9}$|^\d{3} *-? *\d{2} *-? *\d{4}$/m
    pattern = "^\d{9}$|^\d{3} *-? *\d{2} *-? *\d{4}$"
    print ("valid social security number:", (re.search(pattern, str, re.MULTILINE)) != None)

def num_39(str):
# When you read multiline input such as "I\nAM\nSAM."
    str = str.replace('\\n', '\n')
    pattern = "\w*d\w*"
# When you want to use /im options:
    d_search = re.search(pattern, str, re.I | re.MULTILINE)
    print ("first word with d on a line:", d_search)

def num_40(str):
    # /^1*?0?[01]*1?$|^0*?1?[01]*0?$/s
    # "/^ $|^$|^0$|^1$|^00$|^11$|^1+?0+[01]*1$|^0+?1+[01]*0$/s"
    pattern = "^[01 ]$|^1[01]*1$|^0[01]*0$"
    print ("There's same number of 01 substrings as 10 substrings: ", re.match(pattern, str) != None)

while(True):
    input_num = input("Choose the exercise # (31 - 40 or -1 to terminate):")
    if input_num == '-1': exit("Good bye")
    input_str = input("Input string: ")
    eval("num_"+input_num)(input_str)
    print()
