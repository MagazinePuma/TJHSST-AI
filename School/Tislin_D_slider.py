import sys; args = sys.argv[1:]
import time
# Dennis Tislin, Period 5, 2026

arg_1 = ''
if len(args) > 0:
    arg_1 = args[0]

arg_2 = ''
if len(args) > 1:
    arg_2 = args[1]

initialState = arg_1
goalState = arg_2

if goalState == "":
    for n in range(1, len(initialState)):
        goalState += str(n)
    goalState += "_"

def bfs(initial, goal):
    # write your code here
    if not inversion_count(initial, goal): return {initial:-1} 
    if initial == goal: return {initial: goal}
    frontier = [initial]
    explored = {initial: initial}
    
    count = 0
    
    while count < len(frontier):
        current = frontier[count]
        count += 1
        for child in generate_children(current):
            if child == goal:
                explored[child] = current
                return explored
            if not child in explored:
                frontier.append(child)
                explored[child] = current

    return {initial:-1} 
    '''
    def bfs(initial, goal):
    # write your code here
    if initial == goal: return {initial: goal}
    frontier = [initial]
    explored = {initial: initial}
    
    while frontier:
        current = frontier.pop(0)
        for child in generate_children(current):
            if child == goal:
                explored[child] = current
                return explored
            if not child in explored:
                frontier.append(child)
                explored[child] = current
    return {initial:-1}
    '''

def display_path(pzl, goal, maxBand):
    # write code here
    #index = 0
    #if bfs(pzl, goal) == -1:
    #   return
    unreversed_display = list(path(pzl).keys())
    display = unreversed_display[::-1]
    break_num = len(display) // maxBand
    w = find_width(initialState)

    if break_num == 0: break_num = 1
    if break_num * maxBand < len(display):
        break_num += 1

    for z in range(break_num):
        for y in range(len(initialState) // w):
            for x in range(maxBand):
                if x + z * maxBand < len(display):
                    print(display[x + z * maxBand][y * w: w + y * w], end = " ")
            print()
        print()
    '''
    for z in range(maxBand):
        for y in range(len(initialState) // find_width(initialState)):
            for x in range(len(shortestPath) // (len(shortestPath) // maxBand)):
                if x + z * maxBand < len(shortestPath):
                    print(shortestPath[x + z * maxBand][y * find_width(initialState): find_width(initialState) + y * find_width(initialState)], end = " ")
    '''

    '''
    for x in shortestPath:
        for y in range(len(pzl) // find_width(pzl)):
            for z in range(find_width(pzl)):
                print(x[index], end = "")
                index += 1
            print()
        index = 0
        print()
    '''
    '''
    for y in range((len(pzl) // 6) + 1):
        for x in range(find_width(pzl)):
            for sub in pzl[6 * y: 6 * (y + 1)]:
                print(sub[x * find_width(pzl): (x + 1) * find_width(pzl)], end = " ")
            print()
        print()
    '''

    '''
    for band in range(0, len(pzl), maxBand):
        puz = pzl[band: band + maxBand]
        for y in range(len(pzl) // find_width(pzl)):
            for sub in puz:
                print(pzl[y * find_width(pzl): (y + 1) * find_width(pzl)], end = " ")
            print()
        print()
    '''
             
def generate_children(state):
    # write code here
    display = []

    if state.index("_") % find_width(state) != 0:
        display.append(swap(state, state.index("_") - 1, state.index("_")))

    if (state.index("_") + 1) % find_width(state) != 0:
        display.append(swap(state, state.index("_"), state.index("_") + 1))

    if state.index("_") >= find_width(state):
        display.append(swap(state, state.index("_") - find_width(state), state.index("_")))

    if not "_" in state[-find_width(state):]:
        display.append(swap(state, state.index("_"), state.index("_") + find_width(state)))

    return display

def swap(state, i, j):
    # write code here
    return state[:i] + state[j] + state[i + 1:j] + state[i] + state[j + 1:]

def inversion_count(initial, final):
    # write code here
    count = 0
    for x in range(len(initial) - 1):
        for y in range(x + 1, len(initial)):
            if initial[x] > initial[y] and initial[x] != "_":
                count += 1

    countTwo = 0
    for x in range(len(final) - 1):
        for y in range(x + 1, len(final)):
            if final[x] > final[y] and final[x] != "_":
                countTwo += 1
    #return count % 2 == countTwo % 2 
    #return (count % 2 == countTwo % 2) if abs(count - countTwo) % 2 != 1 else Fals
    #return abs(count - countTwo) == 0
    #return absCount == 1 and abs(count - countTwo) > 1
    return countTwo % 2 == count % 2 or find_width(initial) > 5
    #return ((countTwo % 2 == 0 and count % 2 == 0) or (countTwo % 2 != 0 and count %2 != 0) or ()) and find_width(initial) % 2 == 1 

    #   count = 0
    #   for current in initial:
    #       pos = initial.index(current)
    #       for currentOther in goal:
    #           if pos > goal.index(currentOther):
    #               count += 1

def find_width(pzl):
    # write code here
    greatNum = len(pzl)
    for num in range(int(len(pzl)**0.5), len(pzl)):
        if len(pzl) % num == 0:
            greatNum = num
            break
    if greatNum < len(pzl) // greatNum:
        greatNum = len(pzl) // greatNum
    return greatNum

def path_length(explored):
    if explored[initialState] == -1:
        return -1

    count = 0
    initial = initialState
    goal = goalState

    while True:
        initial = explored[goal]
        if initial == goal:
            return count
        goal = initial
        count += 1

    return count

def path(explored):
    if explored[initialState] == -1:
        return explored

    result = {}
    result[goalState] = goalState
    val = initialState
    key = goalState

    while True:
        val = explored[key]
        result[key] = val
        if key == val:
            return result
        key = val

    return result
    '''
    short = []
    initial = initialState
    goal = goalState

    while True:
        initial = explored[goal]
        if initial == goal:
            short.reverse()
            short.append(goalState)
            return short
        goal = initial
        short.append(initial)
    '''

def main():
    print()
    start_time = time.time()
    result = bfs(initialState, goalState)
    #if result != -1:
    display_path(path(result), goalState, 5)
    #print("Steps: ",len(bfs(initialState, goalState)) - 1 if bfs(initialState, goalState) != -1 else -1)
    print("Steps: ", path_length(result))
    run_time = round(time.time() - start_time, 2)
    if run_time == 0:
        run_time = 0.01
    print("Time: ", str(run_time) + "s") 

if __name__ == "__main__":
    main()

'''
def main():
    start_time = time.time()
    bread = bfs(initialState, goalState)
    display_path(initialState, goalState)
    print("Steps:",path_length(bread) if bread != -1 else -1)
    run_time = round(time.time() - start_time, 2)
    if run_time == 0:
        run_time = 0.01
    print("Time:", str(run_time) + "s")

if __name__ == "__main__":
    main()
'''

# read one or two input puzzles
# if there's only one puzzle, goal is "12345678_" initial, goal = "", "" size = len(initial)
# some puzzles are not 3 by 3. You may calculate width and height.(width >= height) width, height = 0, 0 start = time.time() # you may use this to calculate duration
# test bfs and print output. You may also check special cases, e.g. len 0 and len -1
# You must print 5 to 12 puzzles per row. Refer to the sample output below.
# If the path length is greater than 12, print at the next row. Maximum length of path is 31.
# print the number of steps
# Steps: #
# print duration
# Time: #.## (only 3 significant digits)
"""
python Lab3_8pzl_2024.py 52_671348 26_158743
52_ 521
261 261
3_8 _38
754 754
521 521 521 521 _21 2_1 261 261 261 261
671 67_ 678 678 6_8 _68 568 568 5_8 _58 358 358
348 348 34_ 3_4 374 374 374 374 374 374 _74 7_4
_61 6_1 61_ 618 618 6_8 _68 268 268 268
238 238 238 23_ 2_3 213 213 _13 1_3 153
754 754 754 754 754 754 754 754 754 7_4
268 268 26_
153 15_ 158
74_ 743
743
Steps : 26
Time: 1.23s
Test cases:
python your_filename.py 12346875_ => solution is Steps 4
python your_filename.py 1324_7856 _74235861 => solution is Steps 18
python your_filename.py E8B03_4D692175AC E8B0394D65217_AC => solution is Steps 2
python your_filename.py 2871456_3 38_162547 => solution is Steps -1
"""
# Dennis Tislin, Period 5, 2026
