# Dennis Tislin
# Aug 19, 2024

# Warmup 1:

def sleep_in(weekday, vacation):
  return True if not weekday or vacation else False

def monkey_trouble(a_smile, b_smile):
  return True if a_smile and b_smile or not a_smile and not b_smile else False

def sum_double(a, b):
  return (a + b) * 2 if a == b else a + b

def diff21(n):
  return abs(21 - n) if n <= 21 else abs(21 - n) * 2

def parrot_trouble(talking, hour):
  return True if talking and hour < 7 or talking and hour > 20 else False

def makes10(a, b):
  return True if a == 10 or b == 10 or a + b == 10 else False

def near_hundred(n):
  return True if abs(200 - n) <= 10 or abs(100 - n) <= 10 else False

def pos_neg(a, b, negative):
  return True if negative and a < 0 and b < 0 or not negative and a < 0 and b > 0 or not negative and a > 0 and b < 0 else False 

# String 1:

def hello_name(name):
  return "Hello " + name + "!"

def make_abba(a, b):
  return a + (b * 2) + a

def make_tags(tag, word):
  return "<" + tag + ">" + word + "</" + tag + ">"

def make_out_word(out, word):
  return out[:len(out)//2] + word + out[len(out)//2:]

def extra_end(str):
  return str[len(str) - 2:] * 3

def first_two(str):
  return str[:2] if len(str) > 2 else str

def first_half(str):
  return str[:len(str)//2]

def without_end(str):
  return str[1:len(str) - 1]

# List 1:

def first_last6(nums):
  return True if str(nums[0]) == "6" or str(nums[len(nums) - 1]) == "6" else False

def same_first_last(nums):
  return True if len(nums) >= 1 and str(nums[0]) == str(nums[len(nums) - 1]) else False

def make_pi(n):
  return [ int(x) for x in list("31415926535897")[:n] ]

def common_end(a, b):
  return True if a[0] == b[0] or a[len(a) - 1] == b[len(b) - 1] else False

def sum3(nums):
  return sum(nums)

def rotate_left3(nums):
  return [nums[x - len(nums) + 1] for x in range(len(nums))]

def reverse3(nums):
  return nums[::-1]

def max_end3(nums):
  return [nums[0 if nums[0] >= nums[len(nums) - 1] else len(nums) - 1] for x in nums]

# Logic 1:

def cigar_party(cigars, is_weekend):
  return True if is_weekend and cigars >= 40 or cigars >= 40 and cigars <= 60 else False

def date_fashion(you, date):
  return 2 if you >= 8 and date > 2 or you > 2 and date >= 8 else 0 if you <= 2 or date <= 2 else 1

def squirrel_play(temp, is_summer):
  return True if is_summer and temp >= 60 and temp <= 100 or not is_summer and temp >= 60 and temp <= 90 else False

def caught_speeding(speed, is_birthday):
  return 0 if is_birthday and speed <= 65 else 0 if not is_birthday and speed <= 60 else 1 if speed <= 80 and speed >= 61 or is_birthday and speed <= 85 else 2 

def sorta_sum(a, b):
  return 20 if a + b >= 10 and a + b <= 19 else a + b

def alarm_clock(day, vacation):
  return "10:00" if vacation and day >= 1 and day <= 5 or not vacation and day == 6 or not vacation and day == 0 else "off" if vacation and day == 6 or vacation and day == 0 else "7:00" 

def love6(a, b):
  return True if a == 6 or b == 6 or abs(a - b) == 6 or a + b == 6 else False

def in1to10(n, outside_mode):
  return True if not outside_mode and n >= 1 and n <= 10 or outside_mode and n <= 1 or outside_mode and n >= 10 else False

# Dennis Tislin Period 5 2026
