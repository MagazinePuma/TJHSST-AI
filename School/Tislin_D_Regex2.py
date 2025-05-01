import sys; args = sys.argv[1:]
idx = int(args[0])-40
myRegexLst = [
    "/^[.ox]{64}$/i",
    "/^[XO]*\.[XO]*$/im", 
    "/^(X+O*)?\.|\.(O*X+)?$/im", # (|X+\.X+O*|O*X+\.X+)  |(X+O*)\.|\.(O*X+)
    "/^.(..)*$/s",
    "/^((0([01]{2})*|1[01]([01]{2})*))$/s", 
    "/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i",
    "/^(1?0)*1*$/s", 
    "/^([bc]+|[bc]*a[bc]*)$/", # ^([bc]+|[bc]*a[bc]*)$  
    "/^[bc]*(((a[bc]*){2})+|[bc]+)$/", # AA+$|^[BC]*(AA)*[BC]+
    "/^2?(1[02]*1)*[02]*$/" # [12][012]+[02] ([12]){1}[012]*[02] 2?(1[02]*1)*[02]*
]

# /^(|[110 ]|^(110)][01]*)$/s

if idx < len(myRegexLst):
    print(myRegexLst[idx])

# Dennis Tislin, Period 6, 2026
