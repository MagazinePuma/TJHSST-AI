import sys; args = sys.argv[1:]
idx = int(args[0]) - 50

myRegexList = [
    "/(\w)+\w*\\1\w*/i",  #(\w)+\w\\1\w
    "/(\w)+\w*(\\1\w*){3}/i", #\\1\w*\\1\w*
    "/^([01])([01]*\\1)*$/s",
    "/\\b(?=\w*cat)\w{6}\\b/i",
    "/\\b(?=\w*bri)(?=\w*ing)\w{5,9}\\b/i",
    "/\\b(?!\w*cat)\w{6}\\b/i",
    "/\\b(?!(\w)+\w*\\1)\w+/i", #(?=(\w)+)(?!\1)\w+  (\w)\w*(?=(?!\1))\w*   \b(?!(\w)+\w*\1)\w*
    "/^(?![01]*10011)[01]*$/s",
    "/\\b\w*([aeiou])(?!\\1)[aeiou]\w*/i",
    "/^(?![01]*101)(?![01]*111)[01]*$/s",
]

if idx < len(myRegexList):
    print(myRegexList[idx])

# Dennis Tislin, Period 5, 2026