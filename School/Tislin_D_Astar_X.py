import sys; args = sys.argv[1:]
import time

puzzles = open(args[0]).read().splitlines()
goalState = puzzles[0]

def pop_frontier(f):
    min_key = min(f.keys())
    if min_key in f:
        val = f[min_key]
        if len(val) == 1:
            return f.pop(min_key).pop()
        else:
            return f[min_key].pop()

def a_star(start, goal):

    if start == goal: return "G"
    frontier2 = {}
    frontier2[0] = [(0, 0, start, None, "", "")]
    explored = {}

    frontier2_back = {}
    frontier2_back[0] = [(0, 0, goal, None, "", "")]
    explored_back = {}


    while frontier2.keys() or frontier2_back.keys():
        cost, level, current, parent, compact, short_compact = pop_frontier(frontier2)
        
        if current == goal:
            return "G"

        if current in explored:
            continue

        explored[current] = (parent, short_compact, cost, compact, level)
        

        for child, child_compact in generate_children(current):
            if child == goal:
                return compact + child_compact
            
            #if child in explored:
            #    continue

            child_level = level + 1
            child_cost = child_level + manhattan(child, goal)
            new_child_compact = compact + child_compact

            if child_cost in frontier2:
                frontier2[child_cost] += [(child_cost, child_level, child, current, new_child_compact, child_compact)]
            else:
                frontier2[child_cost] = [(child_cost, child_level, child, current, new_child_compact, child_compact)]

            if child in explored_back:# and explored_back[child][4] <= child_cost - child_level:
                return new_child_compact + revert_path(explored_back[child][3])

        cost_back, level_back, current_back, parent_back, compact_back, short_compact_back = pop_frontier(frontier2_back)
        
        if current_back == start:
            return "G"

        if current_back in explored_back:
            continue

        explored_back[current_back] = (parent_back, short_compact_back, cost_back, compact_back, level_back)

        for child_back, child_compact_back in generate_children(current_back):

            if child_back == start:
                return child_compact_back + compact_back
            
            if child_back in explored_back:
                continue

            child_level_back = level_back + 1
            child_cost_back = child_level_back + manhattan(child_back, start)
            new_child_compact_back = child_compact_back + compact_back

            if child_cost_back in frontier2_back:
                frontier2_back[child_cost_back] += [(child_cost_back, child_level_back, child_back, current_back, new_child_compact_back, child_compact_back)]
            else:
                frontier2_back[child_cost_back] = [(child_cost_back, child_level_back, child_back, current_back, new_child_compact_back, child_compact_back)]


            #if child_back in explored:# and explored[child_back][4] == child_cost_back - child_level_back:
            #    return explored[child_back][3][:-1] + revert_path(compact_back)

    return None


def revert_path(path):
    return path.replace("U", "X").replace("D", "U").replace("X", "D").replace("L", "X").replace("R", "L").replace("X", "R")


def generate_children(state):
    # write code here
    size = 4
    display = []

    if state.index("_") % size != 0:
        display.append((swap(state, state.index("_") - 1, state.index("_")), "L"))

    if (state.index("_") + 1) % size != 0:
        display.append((swap(state, state.index("_"), state.index("_") + 1), "R"))

    if state.index("_") >= size:
        display.append((swap(state, state.index("_") - size, state.index("_")), "U"))

    if not "_" in state[-size:]:
        display.append((swap(state, state.index("_"), state.index("_") + size), "D"))

    return display

def swap(state, i, j):
    # write code here
    return state[:i] + state[j] + state[i + 1:j] + state[i] + state[j + 1:]


def inversion_count(initial):
    # write code here
    initial = initial.replace("_", "")
    inversions = 0
    for x in range(len(initial)):
        for y in range(x + 1, len(initial)):
            if initial[x] > initial[y]:
                inversions += 1
    return inversions

def is_solvable(initialState, size=4):
    puzzle_is_solvable = False
    number_of_inversions = inversion_count(initialState)
    is_number_of_inversions_even = number_of_inversions % 2 == 0
    blank_row_in_init = initialState.index("_") // size + 1
    is_blank_on_even_row = abs(size - blank_row_in_init) % 2 == 0

    if size % 2 == 0:
        if (is_blank_on_even_row and is_number_of_inversions_even) or (not is_blank_on_even_row and not is_number_of_inversions_even):
            puzzle_is_solvable = True
    else:
        return is_number_of_inversions_even
    return puzzle_is_solvable


def is_solvable_to_goal(initialState, size=4):
    number_of_inversions_init = inversion_count(initialState)
    number_of_inversions_init_even = number_of_inversions_init % 2

    number_of_inversions_goal = inversion_count(goalState)
    number_of_inversions_goal_even = number_of_inversions_goal % 2


    blank_row_in_init = initialState.index("_") // size
    blank_row_in_goal = goalState.index("_") // size

    is_blank_parity_even = abs(blank_row_in_goal - blank_row_in_init) % 2 == 0

    return (number_of_inversions_goal_even and ((number_of_inversions_init_even and is_blank_parity_even) or (not number_of_inversions_init_even and not is_blank_parity_even))) or \
           (not number_of_inversions_goal_even and ((not number_of_inversions_init_even and is_blank_parity_even) or (number_of_inversions_init_even and not is_blank_parity_even)))



def manhattan(start, goal):
    distance = 0
    goal = goal.replace("_", "")
    for x in goal:
        distance += (abs(find_level(start.index(x))-find_level(goal.index(x))) + abs(find_position(start.index(x)) - find_position(goal.index(x))))
    return distance

    
def find_level(idx):
    return idx // 4

def find_position(idx):
    return idx % 4

'''
def compactPath(explored):
    cPath = ""
    for x in range(len(explored)):
        cPath += explored[x]["compact"]

    return cPath

def display(explored):
    compactPath = ""
    for x in range(len(explored)):
        compactPath += explored[x]["compact"]
    return compactPath

def path(explored, initialState, goalState):
    # if explored[(initialState, None)] == "X":
    #     return ["X"]

    # if explored[(initialState, None)] == "G":
    #     return ["G"]

    result = {}
    result[goalState] = goalState
    val = initialState
    key = list(explored.keys())[len(explored) - 1]

    while True:
        val = explored[key]
        result[key] = val[1]
        if key == val:
            #return result
            compactPath = list(result.values())
            compactPath.reverse()
            return compactPath

        key = val

    compactPath = list(result.values())
    compactPath.reverse()
    return compactPath
'''

def minimum(a, b):
    if a <= b:
        return a
    else:
        return b

def extract_path(current, current_compact, exp, goal):

    result = current_compact
    next_parent = None
    # Node = (0-cost, 1-level, 2-current, 3-parent, 4-compact, 5-short_compact)
    # explores = {current: (0 - parent, 1 - short_compact)}

    next_parent = exp[current]


    parent = None

    if not next_parent:
        return result
    else:
        result += next_parent[1]
        parent = next_parent[0]


    while parent:
        next_parent = exp[parent]

        if next_parent:
            result += next_parent[1]
            parent = next_parent[0]

    '''
    out = [x for x in input if x["current"] == goalState]
    end = ''
    while not end == initialState:
        inter = [x for x in input if x["current"] == out[-1]["parent"]]

        if inter[0]["current"] != inter[0]["parent"]:
            out.append(inter[0])
        end = inter[0]["current"]

    out.reverse()
    return out
    '''
    return result[::-1]

def extract_copact_path(path_array):
    result = ''
    for x in path_array:
        result += x[5]
    
    return result

'''
def display_path(path_list, size=4):
    moves = []
    for i in range(1, len(path_list)):
        prev_blank = path_list[i-1].index('_')  # Adjust if your blank is not '_'
        curr_blank = path_list[i].index('_')    # Adjust if your blank is not '_'
        diff = curr_blank - prev_blank
        if diff == -size:
            moves.append('U')
        elif diff == size:
            moves.append('D')
        elif diff == -1:
            moves.append('L')
        elif diff == 1:
            moves.append('R')
    return ''.join(moves)
'''


def main():
    for initialStateIndex in range(0, len(puzzles)):
        initialState = puzzles[initialStateIndex]
        size = 4
        start_time = time.time()

        if not is_solvable_to_goal(initialState):
            compact_path = 'X'
        elif initialState == goalState:
            compact_path = 'G'
        else:
            result = a_star(initialState, goalState)
            if result:
                #compact_path = display_path(list(result), size)
                compact_path = result
            else:
                compact_path = 'X'
        #result = a_star(initialState, goalState)

        run_time = round(time.time() - start_time, 2)
        if run_time == 0:
            run_time = 0.01

        if compact_path == "G" or compact_path == "X":
            print(str(initialStateIndex) + ":" + initialState, compact_path)
        else:
            print(str(initialStateIndex) + ":" + initialState + " len " + str(len(compact_path) ) + 
              " in " + str(run_time) + " s:" + compact_path)

if __name__ == "__main__":
    main()

# Dennis Tislin, Period 5, 2026
