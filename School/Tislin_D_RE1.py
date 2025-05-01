import sys; args = sys.argv[1:]
# Dennis Tislin, Period 5, 2026

idx = int(args[0]) - 30
myRegexList = [
    "/^0$|^10[10]$/",
    "/^[01]*$/",
    "/0$/m",
    "/\w*[aeiou]\w*[aeiou]\w*/i",
    "/^0$|^1[01]*0$/",
    "/^[10]*110[01]*$/",
    "/^.{2,4}$/s",
    "/^\d{3} *-? *\d{2} *-? *\d{4}$/",
    "/^.*?\w*d\w*/im",
    "/^$|^[01 ]$|^1[01]*1$|^0[01]*0$/s",
]

if idx < len(myRegexList):
    print(myRegexList[idx])

# Dennis Tislin, Period 5, 2026
