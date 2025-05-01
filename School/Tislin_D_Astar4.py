import sys; args = sys.argv[1:]
import time

#args = ['test.txt']
puzzles = open(args[0]).read().splitlines()
goalState = puzzles[0]


def a_star(start, goal):
    if start == goal: return [{"current": start, "parent": start, "cost": 0, "level": 0, "compact": "G"}]
    current = None
    min = 0
    frontier = [{"current": start, "parent": start, "cost": 0, "level": 0, "compact": ""}]
    explored = []
    #count = 0

    print_log = False
    
    while len(frontier)>0:
        min = 999
        min_level = 999
        minIndex = -1

        for x in range(len(frontier)):
            if frontier[x]["cost"] < min:
                minIndex = x
                min = frontier[x]["cost"]
        
        if minIndex > -1:
            current = frontier.pop(minIndex)
            #explored.append(current)

        current_in_explored = next(( x for x in explored if x["current"] == current["current"]), None)
        if current_in_explored:
            continue
            


        explored.append(current)

        for child in generate_children(current["current"]):
            if child["current"] == goal:
                explored.append(current)
                child["level"] = current["level"] + 1
                child["cost"] = child["level"] + manhattan(child["current"], goal)
                explored.append(child)
                return explored
            
            child_in_explored = next(( x for x in explored if x["current"] == child["current"]), None)
            if child_in_explored:
                continue

            child["level"] = current["level"] + 1
            child["cost"] = child["level"] + manhattan(child["current"], goal)

            #== close-1 ==
            #on_frontier_list = next(( x for x in frontier if x["level"] < child["level"] and x["cost"] < child["cost"]), None)
            #on_frontier_list2 = next(( x for x in frontier if x["level"] <= child["level"] and x["cost"] < child["cost"]), None)

            #on_closed_list = next((x for x in explored if x["level"] == child["level"] and \
            #                    x["cost"] < child["cost"]), None)

            # == Close-1 ==
            #on_closed_list = next( (x for x in explored if x["current"] == child["current"] or (x["level"] > child["level"] and x["cost"] < child["cost"]) ), None)
            on_closed_list = next( (x for x in explored if (x["level"] > child["level"] and x["cost"] < child["cost"]) ), None)
            #on_closed_list = next( (x for x in explored if (x["level"] > child["level"] ) ), None)

            #already_in_explored = len([x for x in explored if x["level"] > successor_current_cost and x["current"] == child["current"]]) > 0

            #==
            #if on_frontier_list:
            #    continue

            #==
            if on_closed_list:
                continue

            frontier.append(child)

    return [{"current": start, "parent": start, "cost": 0, "level": 0, "compact": "X"}]


def generate_children(state):
    # write code here
    size = 4
    display = []

    if state.index("_") % size != 0:
        display.append({"current": swap(state, state.index("_") - 1, state.index("_")), "parent": state, "cost": 0, "level": 0, "compact": "L"})

    if (state.index("_") + 1) % size != 0:
        display.append({"current": swap(state, state.index("_"), state.index("_") + 1), "parent": state, "cost": 0, "level": 0, "compact": "R"})

    if state.index("_") >= size:
        display.append({"current": swap(state, state.index("_") - size, state.index("_")), "parent": state, "cost": 0, "level": 0, "compact": "U"})

    if not "_" in state[-size:]:
        display.append({"current": swap(state, state.index("_"), state.index("_") + size), "parent": state, "cost": 0, "level": 0, "compact": "D"})

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

def inversion_to_goal_count(initial, goal):
    # write code here
    initial = initial.replace("_", "")
    goal = goal.replace("_", "")
    inversions = 0
    for x in range(len(initial)):
        for y in range(x + 1, len(goal)):
            g = goal.index(initial[x])
            #if initial[x] > goal[y]:
            if goal.index(initial[y]) < g:
                inversions += 1
    return (inversions % 2 == 0 and abs(find_level(initial.index("_")) - find_level(goal.index("_"))) % 2 == 0) or (inversions % 2 != 0 and abs(find_level(initial.index("_")) - find_level(goal.index("_"))) % 2 != 0)
    # return inversions


def is_solvable(initialState, size=4):
    puzzle_is_solvable = False
    #number_of_inversions = inversion_count(initialState)
    number_of_inversions = inversion_to_goal_count(initialState, goalState)
    is_number_of_inversions_even = number_of_inversions % 2 == 0
    blank_row_in_init = initialState.index("_") // size + 1
    is_blank_on_even_row = abs(size - blank_row_in_init) % 2 == 0
    row_of_blank_of_initial = initialState.index("_") // size
    row_of_blank_of_goal = goalState.index("_") // size
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
def path_length(explored):
    if explored[initialState] == -1:
        return "X"

    if explored[(initialState, None)] == "G":
        return "G"

    count = 0
    initial = initialState
    goal = list(explored.keys())[len(explored) - 1]

    while True:
        initial = explored[goal]
        if initial == goal:
            return count
        goal = initial
        count += 1

    return count
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


def minimum(a, b):
    if a <= b:
        return a
    else:
        return b

def extractPath(input, initialState):

    if len(input) == 1:
        return input
    
    out = [x for x in input if x["current"] == goalState]
    end = ''
    while not end == initialState:
        inter = [x for x in input if x["current"] == out[-1]["parent"]]

        if inter[0]["current"] != inter[0]["parent"]:
            out.append(inter[0])
        end = inter[0]["current"]

    out.reverse()
    return out

def main():

    for initialStateIndex in range(0, len(puzzles)):
        initialState = puzzles[initialStateIndex]
        start_time = time.time()

        if not is_solvable_to_goal(initialState, goalState):
            result = [{"current": initialState, "parent": initialState, "cost": 0, "level": 0, "compact": "X"}]
        else:
            result = a_star(initialState, goalState)
        #result = a_star(initialState, goalState)

        run_time = round(time.time() - start_time, 2)
        if run_time == 0:
            run_time = 0.01
        # print(path(result, initialState, goalState))
        #print(str(initialStateIndex) + ": " + initialState + " len " + str(len(path(result, initialState, goalState)) + 1) 
        #      + " in " + str(run_time) + "s:", "".join([str(x) for x in path(result, initialState, goalState)]))


        #output = extrqactPath(initialState, result)

        if display(result) == "G" or display(result) == "X":
            print(str(initialStateIndex) + ":" + initialState, display(result))
        else:
            print(str(initialStateIndex) + ": " + initialState + " len " + str(len(display(extractPath(result, initialState))))
              + " in " + str(run_time) + "s:" + display(extractPath(result, initialState)))

if __name__ == "__main__":
    main()

# Dennis Tislin, Period 5, 2026
