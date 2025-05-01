# Dennis Tislin: Lab due 8/28

# Warmup - 2

def string_times(str, n):
  return str*n

def string_splosion(str):
  return "".join([str[0:i] for i in range(len(str)+1)])

def array_front9(nums):
  return 9in nums and nums.index(9)<4

def front_times(str, n):
  return str[:3]*n

def last2(str):
  return len([x for x in range(len(str)-1) if str[x-1:x+1]==str[-2:]])

def array123(nums):
  return True in [nums[x:x+3]==[1,2,3]for x in range(len(nums)-2)]

def string_bits(str):
  return str[0:len(str):2]

def array_count9(nums):
  return len([x for x in nums if x==9])

def string_match(a, b):
  return [1if a[x:x+2]==b[x:x+2]else 0 for x in range(min(len(a),len(b))-1)].count(1)

# Logic - 2

def make_bricks(small, big, goal):
  return big!=0and goal%(big*5)==0 or goal-5*(goal//5)<=small and big!=0 and big*5+small>=goal or small>=goal and big==0

def no_teen_sum(a, b, c):
 return sum([[a,b,c][x]if [a,b,c][x]==15 or [a,b,c][x]==16 or not [a,b,c][x]in [y for y in range(13,20)] else 0 for x in range(3)])

def make_chocolate(small, big, goal):
  return (sorted([y for x in range(big-1)if 0<= (y:=(goal - x*5))<=small])+[-1])[0]

def lone_sum(a, b, c):
  return sum([x for x in [a,b,c] if [a,b,c].count(x)==1])

def round_sum(a, b, c):
  sum([x-int(str(x)[1])if len(str(x))>1 and int(str(x)[1])<5 else x+10-int(str(x)[1])if len(str(x))>1 and int(str(x)[1])>=5 else 0 if x<5 else 10 for x in [a,b,c]])

def lucky_sum(a, b, c):
  return sum([a,b,c][0:[a,b,c].index(13)])if 13in[a,b,c]else a+b+c

def close_far(a, b, c):
  return (abs(a-b)<=1 and abs(a-c)>1) and (abs(a-c)<=1 and abs(a-b)>1) or not max([a,b,c])==min([a,b,c])+2

# String - 2

def double_char(str):
  return "".join([x+x for x in str])

def count_code(str):
  return [1 if str[x:x+2]=="co" and str[x+3]=="e" else 0 for x in range(len(str)-3)].count(1) 

def count_hi(str):
  return str.count("hi")

def end_other(a, b):
  return a.lower()[len(a)-len(b):]==b.lower()or b.lower()[len(b)-len(a):]==a.lower()  

def cat_dog(str):
  return str.count("dog")==str.count("cat")

def xyz_there(str):
  return "xyz"in str.replace(".xyz","0")

# List - 2

def count_evens(nums):
  return len(y:=([nums[x] if nums[x]%2==0else""for x in range(len(nums))]))-y.count("")

def sum13(nums):
  return sum(nums)if not 13in nums else sum([nums[x]if(nums[x]!=13and nums[x-1]!=13)or(nums[x]!=13 and x==0)else 0 for x in range(len(nums))])

def big_diff(nums):
  return max(nums)-min(nums)

def sum67(nums):
    return sum([0 if nums[i]==6 or 6 in nums[:i] and 7 in nums[i:] else nums[i] for i in range(len(nums))])

def centered_average(nums):
  return (sum(nums)-(max(nums)+min(nums)))//(len(nums)-2)

def has22(nums):
  return True in[nums[x]==2and nums[x+1]==2for x in range(len(nums)-1)]

# Dennis Tislin, Period 5, 2026
