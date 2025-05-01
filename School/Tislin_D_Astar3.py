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
    
    while len(frontier):
        min = 999
        min_level = 999
        minIndex = -1
        for x in range(len(frontier)):
            if frontier[x]["level"] <= min_level:
            #if frontier[x]["cost"] <= min:
                min_level = frontier[x]["level"]

        for x in range(len(frontier)):
            if frontier[x]["level"] == min_level and frontier[x]["cost"] <= min:
                min_level = frontier[x]["level"]
                minIndex = x
                min = frontier[x]["cost"]
            
        
        if minIndex > -1:
            current = frontier.pop(minIndex)

        #count += 1

        for child in generate_children(current["current"]):
            if child["current"] == goal:
                explored.append(current)
                child["level"] = current["level"] + 1
                child["cost"] = child["level"] + manhattan(goal, child["current"])
                explored.append(child)
                return explored
            
            #existsInExplored = filter(lambda x: x["current"] == child["current"], explored)


            child["level"] = current["level"] + 1
            child["cost"] = child["level"] + manhattan(goal, child["current"])

            existsInFrontier = [x for x in frontier if x["level"] == child["level"]]
            existsInExplored = [x for x in explored if x["level"] == child["level"]]
            
            skip_frontier_based = False
            if len(existsInFrontier):
                for x in existsInFrontier:
                    if x["cost"] < child["cost"]:
                        skip_frontier_based = True
                        break
            
            if skip_frontier_based:
                continue;

            
            skip_explored_based = False
            if len(existsInExplored):
                for x in existsInExplored:
                    if x["cost"] < child["cost"]:
                        skip_explored_based = True
                        break
                    else:
                        idx = explored.index(x)
                        to_move = explored.pop(idx)
                        frontier.append(to_move)

            if skip_explored_based:
                continue;
            

            frontier.append(child)


        #existsInExplored = filter(lambda x: x["current"] == current["current"] and x["level"] == current["level"], explored)
        currentExistsInExplored = [x for x in explored if x["level"] == current["level"] and x["cost"] < current["cost"]]

        if not len(currentExistsInExplored):
            explored.append(current)
        #else:
        #    return explored
        #    return [{"current": start, "parent": start, "cost": 0, "level": 0, "compact": "X"}]

        #explored.append(current)

        

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

def inversion_count(initial, final):

    # write code here
    count = 0
    for x in range(len(initial) - 1):
        for y in range(x + 1, len(initial)):
            if initial[x] > initial[y] and initial[x] != "_":
                count += 1
    '''
    countTwo = 0
    for x in range(len(final) - 1):
        for y in range(x + 1, len(final)):
            if final[x] > final[y] and final[x] != "_":
                countTwo += 1
    '''

    #return countTwo % 2 == count % 2 or find_width(initial) > 5
    return count

def manhattan(start, goal):
    distance = 0
    
    for x in start:
        if x != "_":
            distance += (abs(find_level(goal.index(x))-find_level(start.index(x))) + abs(find_position(goal.index(x)) - find_position(start.index(x)))
        #distance += abs((((find_level(start.index(x)) + 1) * 4) - (start.index(x) + 1)) - (((find_level(goal.index(x)) + 1) * 4) - (goal.index(x) + 1))) + abs(find_level(goal.index(x)) - find_level(start.index(x))
                                                                                                                                                   )

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

def isPuzzleSolvable(initialState):
    puzzle_is_solvable = False

    number_of_inversions = inversion_count(initialState, goalState)
    is_number_of_inversions_even = number_of_inversions % 2 == 0
    blank_level_in_init = initialState.index("_") // 4 + 1
    blank_level_in_goal = goalState.index("_") // 4 + 1
    is_blank_on_even_row = abs(blank_level_in_goal - blank_level_in_init) % 2 == 0

    if (is_blank_on_even_row and is_number_of_inversions_even) or (not is_blank_on_even_row and not is_number_of_inversions_even):
        puzzle_is_solvable = True
    return puzzle_is_solvable

def extrqactPath(initialState, input):


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

        if not isPuzzleSolvable(initialState):
            result = [{"current": initialState, "parent": initialState, "cost": 0, "level": 0, "compact": "X"}]
        else:
            result = a_star(initialState, goalState)

        run_time = round(time.time() - start_time, 2)
        if run_time == 0:
            run_time = 0.01
        # print(path(result, initialState, goalState))
        #print(str(initialStateIndex) + ": " + initialState + " len " + str(len(path(result, initialState, goalState)) + 1) 
        #      + " in " + str(run_time) + "s:", "".join([str(x) for x in path(result, initialState, goalState)]))


        output = extrqactPath(initialState, result)

        if display(output) == "G" or display(output) == "X":
            print(str(initialStateIndex) + ":" + initialState, display(output))
        else:
            print(str(initialStateIndex) + ": " + initialState + " len " + str(len(display(output)))
              + " in " + str(run_time) + "s:" + display(output))

if __name__ == "__main__":
    main()
    
# Dennis Tislin, Period 5, 2026
