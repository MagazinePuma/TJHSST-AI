import sys; args = sys.argv[1:]
import time

class HeapPriorityQueue():
    def __init__(self):
        self.queue = ["dummy"]
        self.current = 1
   
    def next(self):
        if self.current >= len(self.queue):
            self.current = 1
            raise StopIteration
        out = self.queue[self.current]
        self.current += 1
        return out
   
    def __iter__(self):
        return self
   
    __next__ = next
   
    def isEmpty(self):
        return len(self.queue) == 1
   
    def swap(self, a, b):
        self.queue[a], self.queue[b] = self.queue[b], self.queue[a]
       
    def push(self, value):
        self.queue.append(value)
        self.heapUp(len(self.queue) - 1)
       
    def heapUp(self, k):
        while k // 2 > 0 and self.queue[k] < self.queue[k // 2]:
            self.swap(k, k // 2)
            k = k // 2
   
    def heapDown(self, k, size):
        left, right = k * 2, k * 2 + 1
        if left == size and self.queue[k] > self.queue[left]:
            self.swap(k, left)
        elif right <= size:
            maxC = (left if self.queue[left] < self.queue[right] else right)
            if self.queue[maxC] < self.queue[k]:
                self.swap(k, maxC)
                self.heapDown(maxC, size)
   
    def reheap(self):
        for i in range(len(self.queue) // 2, 0, -1):
            self.heapDown(i, len(self.queue) - 1)
   
    def pop(self):
        self.swap(1, len(self.queue) - 1)
        out = self.queue.pop()
        self.heapDown(1, len(self.queue) - 1)
        return out
   
    def remove(self, index):
        self.swap(index + 1, len(self.queue) - 1)
        out = self.queue.pop()
        self.reheap()
        return out
    
    def contains(self, value):
        return any(i for i in self.queue if i[0] == value)



#args = ['test.txt']
puzzles = open('test.txt').read().splitlines()
goalState = puzzles[0]

def a_star(start, goal):
    # if not inversion_count(start, goal): return "X"
    frontier = [HeapPriorityQueue(), HeapPriorityQueue()]
    explored = [{(start, "G"): (0, [start], "G")}, {(goal, "G"): (0, [goal], "G")}]
    frontier[0].push((0, (start, "G"), "G"))
    frontier[1].push((0, (goal, "G"), "G"))
    f = [{(start, "G")}, {(goal, "G")}]
    sg = [(start, "G"), (goal, "G")]
    k = 1
    
    while frontier[0] and frontier[1]:
        k = 1 - k
        cost, current, compact = frontier[k].pop()
        f[k] -= {current}
        
        if current in f[1 - k]:
            path, cost2 = explored[k][current][1][:-1] + explored[1 - k][current][1][::-1], explored[k][current][0] + explored[1 - k][current][0] # explored[k][current][1][:-1] +  
            return path, cost2
        
        for child in generate_children(current):
            cost3 = explored[k][current][0] + (child[0].index("_") // 4)
            if child not in explored[k] or explored[k][child][0] > cost3:
                frontier[k].push((cost3 + manhattan(child[0], sg[1 - k][0]), child, child[1]))
                f[k].add(child)
                explored[k][child] = (cost3, explored[k][current][1] + [child], child[1])
        
    return None

def revert_path(path):
    return path.replace("U", "X").replace("D", "U").replace("X", "D").replace("L", "X").replace("R", "L").replace("X", "R")

def convert_path(pathCostTuple):
    pctr = pathCostTuple[0]
    pctr.reverse()
    
    if len(pctr) == 1:
        return "G"
    
    # for x in pctr:
    #     for y in pctr:
    #         if x[0] == y[0]:
    #             pctr.remove(x)
    
    return "".join([pctr[x][1] for x in range(1, len(pctr) - 1)])

def generate_children(state):
    # write code here
    size = 4
    display = []

    if state[0].index("_") % size != 0:
        display.append((swap(state[0], state[0].index("_") - 1, state[0].index("_")), "L"))

    if (state[0].index("_") + 1) % size != 0:
        display.append((swap(state[0], state[0].index("_"), state[0].index("_") + 1), "R"))

    if state[0].index("_") >= size:
        display.append((swap(state[0], state[0].index("_") - size, state[0].index("_")), "U"))

    if not "_" in state[0][-size:]:
        display.append((swap(state[0], state[0].index("_"), state[0].index("_") + size), "D"))

    return display

def swap(state, i, j):
    # write code here
    return state[:i] + state[j] + state[i + 1:j] + state[i] + state[j + 1:]


def inversion_count(initial, goal):
    # write code here
    # initial = initial.replace("_", "")
    # inversions = 0
    # for x in range(len(initial)):
    #     for y in range(x + 1, len(initial)):
    #         if initial[x] > initial[y]:
    #             inversions += 1
    
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

def extract_path(parent, exp, goal):

    result = ""
    next_parent = None
    # Node = (0-cost, 1-level, 2-current, 3-parent, 4-compact, 5-short_compact)
    # explores = {current: (0 - parent, 1 - short_compact)}


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

        # if not is_solvable_to_goal(initialState):
        #     compact_path = 'X'
        # elif initialState == goalState:
        #     compact_path = 'G'
        # else:
        #     result = a_star(initialState, goalState)
        #     if result:
        #         #compact_path = display_path(list(result), size)
        #         compact_path = result
        #     else:
        #         compact_path = 'X'
        # #result = a_star(initialState, goalState)

        # run_time = round(time.time() - start_time, 2)
        # if run_time == 0:
        #     run_time = 0.01
        
        print(a_star(initialState, goalState))
        print(convert_path(a_star(initialState, goalState)))

        # if compact_path == "G" or compact_path == "X":
        #     print(str(initialStateIndex) + ":" + initialState, compact_path)
        # else:
        #     print(str(initialStateIndex) + ":" + initialState + " len " + str(len(compact_path) ) + 
        #       " in " + str(run_time) + " s:" + compact_path)

if __name__ == "__main__":
    main()

# Dennis Tislin, Period 5, 2026