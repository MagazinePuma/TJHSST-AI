import sys; args = sys.argv[1:]
import random
import time
#puzzles = open(args[0]).read().splitlines()
puzzles = open("test.txt").read().splitlines()


# optional helper function
def select_unassigned_var(assignment, variables, neighbors):
    #return str(random.choice(list(variables.keys())))
    #return random.choice(list(variables.keys()))
    for var in variables.keys():
        if assignment[var] == ".":  # Assuming "." indicates an unassigned variable
            return var


# optional helper function
def is_valid(var_index, value, assignment, variables):
    ''' Your code goes here'''
    # print("var_index " + str(var_index))
    # print("variables " + str(variables))
    # print(variables[var_index])
    
    for x in variables[var_index]:
        if str(x) in assignment:
            if assignment[x] == value:
                return False
    return True

    # for list in csp_table:
    #     if var_index in list:
    #         for x in list:
    #             if assignment[x] == value:
    #                 return False
    
    # for index, vars in variables.items():
    #     if len(vars) == 0:
    #         return False
    
    # return True

# optional helper function
def ordered_domain(var_index, variables, q_table, assignment):
    ''' Your code goes here'''
    dict = {x: 0 for x in variables[var_index]}
    
    for x in assignment:
        if x in dict:
            dict[x] = dict[x] + 1
            
    tup_lis = [(x, val) for val, x in dict.items()]
    sort_dict = sorted(tup_lis, reverse = True)
    domain = [val for x, val in sort_dict]
    
    return domain

# optional helper function
def update_variables(value, var_index, assignment, variables, neighbors, csp_table):
    ''' Your code goes here'''
    dict = {x: {y for y in vars} for x, vars in variables.items() if x != var_index}
    
    for list in csp_table:
        if var_index in list:
            for var in list:
                if var in dict:
                    dict[var] -= {value}
    
    return dict

def solve(puzzle, neighbors):
    # initialize_ds function is optional helper function. You can change this part.
    variables, puzzle, q_table = initialize_ds(puzzle, neighbors) # q_table is quantity table {'1': number of value '1' occurred, ...}
    return recursive_backtracking_3(puzzle, variables, neighbors, q_table)

# def remove_val(neighbors, var, val, variables, assignment):
#     for neigh in neighbors[var]:
#         #print("removing val found from neighbor " + str(neigh))
#         if neigh == var:
#             #print("same neighbor as current val skipping")
#             continue
#         if neigh not in variables:
#             #print("ignoring neighbor " + str(neigh) + " as its known")
#             continue
#         try:
#             variables[neigh].remove(val[0])
#             if len(variables[neigh]) == 0:
#                 return assignment
#         except ValueError:
#             pass
        
def check_vars(variables):
    for x in list(variables.keys()):
        if len(variables[x]) == 1:
            return x, variables[x]
    return None

# import copy

def recursive_backtracking_3(assignment, variables, neighbors, q_table):
    #if not "." in assignment: return assignment
    if list(q_table.items()) == [(1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9)]:
        return assignment
    
    # copya = assignment
    # copyv = variables
    # copyn = neighbors
    # copyq = q_table
    
    #tested_vals = set()
    #unknown_vars = [x for x in variables.keys()] #copy.deepcopy(variables).keys()
    #changed = False
    #print(variables)
    # for var in unknown_vars:
    #     val = variables[var]
    #     if len(val) == 1:
    if check_vars(variables) != None:
        #print("Found var " + str(var) + " has only one possible answer " + str(val))
        var, val = check_vars(variables)
        assignment = assignment[:var] + val[0] + assignment[var + 1:]
        q_table[int(val[0])] += 1
        del variables[var]
        for neigh in neighbors[var]:
            #print("removing val found from neighbor " + str(neigh))
            if neigh == var:
                #print("same neighbor as current val skipping")
                continue
            if neigh not in variables:
                #print("ignoring neighbor " + str(neigh) + " as its known")
                continue
            try:
                variables[neigh].remove(val[0])
                if len(variables[neigh]) == 0:
                    return assignment
                    # if not "." in assignment:
                    #     return assignment
                    # return recursive_backtracking_3(copya, copyv, copyn, copyq)
            except ValueError:
                pass
        #print(variables)
    else:
        #print("No values changed, nothing deterministic, therefore randomly picking a possible solution")
        var = random.choice(list(variables.keys()))
        #print("randomly picked " + str(var))
        val = random.choice(variables[var])
        #tested_vals.add(val)
        #print("randomly assigned pick to " + str(val))
        assignment = assignment[:var] + val[0] + assignment[var + 1:]
        q_table[int(val[0])] += 1
        del variables[var]
        for neigh in neighbors[var]:
            #print("removing val found from neighbor " + str(neigh))
            if neigh == var:
                #print("same neighbor as current val skipping")
                continue
            if neigh not in variables:
                #print("ignoring neighbor " + str(neigh) + " as its known")
                continue
            try:
                variables[neigh].remove(val)
                if len(variables[neigh]) == 0:
                    return assignment
                    # if not "." in assignment:
                    #     return assignment
                    # return recursive_backtracking_3(copya, copyv, copyn, copyq)
            except ValueError:
                pass
    
    return recursive_backtracking_3(assignment, variables, neighbors, q_table)


def recursive_backtracking_2(assignment, variables, neighbors, q_table):
    if not "." in assignment: return assignment
    
    #tested_vals = set()
    unknown_vars = [x for x in variables.keys()] #copy.deepcopy(variables).keys()
    changed = False
    #print(variables)
    for var in unknown_vars:
        val = variables[var]
        if len(val) == 1:
            #print("Found var " + str(var) + " has only one possible answer " + str(val))
            assignment = assignment[:var] + val[0] + assignment[var + 1:]
            del variables[var]
            changed = True
            for neigh in neighbors[var]:
                #print("removing val found from neighbor " + str(neigh))
                if neigh == var:
                    #print("same neighbor as current val skipping")
                    continue
                if neigh not in variables:
                    #print("ignoring neighbor " + str(neigh) + " as its known")
                    continue
                try:
                    variables[neigh].remove(val[0])
                    if len(variables[neigh]) == 0:
                        return assignment
                except ValueError:
                    pass
            #print(variables)

    if not changed:
        #print("No values changed, nothing deterministic, therefore randomly picking a possible solution")
        var = random.choice(list(variables.keys()))
        #print("randomly picked " + str(var))
        val = random.choice(variables[var])
        #tested_vals.add(val)
        #print("randomly assigned pick to " + str(val))
        assignment = assignment[:var] + val[0] + assignment[var + 1:]
        del variables[var]
        for neigh in neighbors[var]:
            #print("removing val found from neighbor " + str(neigh))
            if neigh == var:
                #print("same neighbor as current val skipping")
                continue
            if neigh not in variables:
                #print("ignoring neighbor " + str(neigh) + " as its known")
                continue
            try:
                variables[neigh].remove(val)
                if len(variables[neigh]) == 0:
                    return assignment
            except ValueError:
                pass
    
    return recursive_backtracking_2(assignment, variables, neighbors, q_table)
    

# optional helper function: you are allowed to change it
def recursive_backtracking(assignment, variables, neighbors, q_table):
    # print("assingment:")
    # print(assignment)
    # print("variables:")
    # print(variables)
    # print("neighbors:")
    # print(neighbors)
    # print("q_table:")
    # print(q_table)
    ''' Your code goes here'''
    if not "." in assignment: return assignment
    var = select_unassigned_var(assignment, variables, neighbors)
    # print("var")
    # print(var)
    
    #for val in ordered_domain(assignment.index(var), variables, q_table, assignment):
        #if is_valid(assignment.index(var), val, assignment, variables):

    # print(ordered_domain(var, variables, q_table, assignment))
    for val in list(variables[var]):
        # print("is_valid")
        # print(is_valid(var, val, assignment, variables))
        if is_valid(var, val, assignment, neighbors):
            # copya = assignment
            # copyb = variables.copy()
            # copyc = neighbors.copy()
            # copyd = q_table.copy()
            
            assignment = assignment[:var] + val + assignment[var + 1:]
            del variables[var]
            for neigh in neighbors[var]:
                #print("removing val found from neighbor " + str(neigh))
                if neigh == var:
                    #print("same neighbor as current val skipping")
                    continue
                if neigh not in variables:
                    #print("ignoring neighbor " + str(neigh) + " as its known")
                    continue
                try:
                    variables[neigh].remove(val[0])
                    # if len(variables[neigh]) == 0:
                    #     return assignment
                        # if not "." in assignment:
                        #     return assignment
                        # return recursive_backtracking_3(copya, copyv, copyn, copyq)
                except ValueError:
                    pass
            #print(variables)
            result = recursive_backtracking(assignment, variables, neighbors, q_table)
            
            if result != None: 
                return result
            
            # assignment = copya
            # variables = copyb
            # neighbors = copyc
            # q_table = copyd
            
    return None

def sudoku_csp(n=9):
    ''' Your code goes here '''
    rows = [[x for x in range(i * n, (i + 1) * n)] for i in range(n)]
    cols = [[x for x in range(i, 81, n)] for i in range(n)]
    
    first_grid = [0, 1, 2, 9, 10, 11, 18, 19, 20]
    beg_indices = [0, 3, 6, 27, 30, 33, 54, 57, 60]
    grids = [[x + y for y in first_grid] for x in beg_indices]
    
    return rows + cols + grids

def find_grid(csp_table, x):
    grids = csp_table[18:]
    
    for list in grids:
        if x in list:
            return list
    
    return None

def sudoku_neighbors(csp_table): # {0:[0, 1, 2, 3, 4, ...., 8, 9, 18, 27, 10, 11, 19, 20], 1:
    ''' Your code goes here '''
    return {x: set(csp_table[x // 9] + csp_table[(x % 9) + 9] + find_grid(csp_table, x)) for x in range(81)}    # csp_table[(x % 3) + 18]
    
    # neighbors = {}
    
    # for x in range(81):
    #     for list in csp_table:
    #         neighbors_list = []
    #         if x in list:
    #             neighbors_list += list
    #             neighbors[x] = neighbors_list
    
    # return neighbors

# Optional helper function
def initialize_ds(puzzle, neighbors):
    ''' Your code goes here '''
    #print (vars, puzzle, q_table)
    variables = {}
    vars = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    q_table = {i: 0 for i in range(1, 10)}
    count = 0
    
    for y in puzzle:
        if y != '.':
            q_table[int(y)] += 1
    
    for x in range(81):
        if puzzle[x] == ".":            
            for neigh in neighbors[x]:
                if puzzle[neigh] != "." and puzzle[neigh] in vars:
                    vars.remove(puzzle[neigh])
                    
            variables[x] = vars
            vars = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        
    return variables, puzzle, q_table

# sum of all ascii code of each char - (length of the solution * ascii code of min char)
def checksum(solution):
    ''' write your code here'''
    # ascii_list = [ord(x) for x in solution]
    # smallest_ascii = min(ascii_list)
    return sum([ord(c) for c in solution]) - 49*81
    #return sum([int(char) for char in solution]) - 81 * ord(min(list(solution)))

def check_valid(check_str):
    for char in check_str:
        if char not in '123456789.':
            return False
    return len(check_str) == 81

def main():
    csp_table = sudoku_csp() # rows, cols, and sub_blocks
    neighbors = sudoku_neighbors(csp_table) # each position p has its neighbors {p:[positions in same row/col/subblock], ...}
    start_time = time.time()
    for line, puzzle in enumerate(puzzles):
        line, puzzle = line+1, puzzle.rstrip()
        print("{}: {}".format(line, puzzle))

        if not check_valid(puzzle):
            print("{}{}".format(" "*(len(str(line))+2), puzzle))
            continue
        
        mychecksum = 0
        #x = 0
        while mychecksum != 405:
            solution = solve(puzzle, neighbors)
            if '.' in solution:
                #print("bad solution returned")
                continue
            mychecksum = sum([int(char) for char in solution])
            #print("checksum was equal to " + str(mychecksum))

            #x += 1
            #print("Attempt " + str(x))
        #solution = solve(puzzle, neighbors)
        if solution == None:
            print("No solution found.")
            break
        print("{}{} {}".format(" "*(len(str(line))+2), solution, checksum(solution)))
        #print("{}{}".format(" "*(len(str(line))+2), solution))
    print("Duration:", (time.time() - start_time))

if __name__ == '__main__': 
    main()

# Required comment: Your name, Period #, 2023
# Check the example below. You must change the line below before submission.
# Dennis Tislin, Period 5, 2026