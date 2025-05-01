import sys; args = sys.argv[1:]
import time
import random
import math

input = "puzzles.txt"

if args and args[0]:
    input = args[0]
    
puzzles = open(args[0]).read().splitlines()

# optional helper function
def select_unassigned_var(assignment, variables, neighbors):
   pass

# optional helper function
def ordered_domain(var_index, variables, q_table):
    
    dom = variables[var_index]
    dom_dict = {}
    for val in dom:
       dom_dict[val] = q_table[int(val)]

    #dom_dict_ordered = {k: v for k, v in sorted(dom_dict.items(), key=lambda item: item[1])}
    dom_dict_ordered = {k: v for k, v in sorted(dom_dict.items(), key=lambda item: item[1], reverse=True)}
    dom_ordered = list(dom_dict_ordered.keys())

    return dom_ordered

# optional helper function
def update_variables(value, var_index, assignment, variables, neighbors):
    ''' Your code goes here'''

    curr_constraints = neighbors[var_index]
    variables_copy = {key: value[:] for key, value in variables.items()}
    for idx in curr_constraints:
       if not idx in variables_copy:
          continue
       
       curr_vars = variables_copy[idx]
       if value in curr_vars:
          curr_vars.remove(value)
       variables_copy[idx] = curr_vars
    
    return variables_copy

def shortest_domain_index(assignment, variables):
   min_dom_length = 999
   min_dom_idx = -1
   for idx, val in enumerate(assignment):
      if val == '.':
         dom_length = len(variables[idx])
         if dom_length < min_dom_length:
            min_dom_length = dom_length
            min_dom_idx = idx
   return min_dom_idx


def solve(puzzle, neighbors):
   # initialize_ds function is optional helper function. You can change this part. 
   variables, puzzle, q_table = initialize_ds(puzzle, neighbors)  # q_table is quantity table {'1': number of value '1' occurred, ...}
   constraints = {}
   for x in variables.keys():
      constraints[x] = neighbors[x]
   return recursive_backtracking(puzzle, q_table, variables, constraints)

# optional helper function: you are allowed to change it
def recursive_backtracking(assignment, q_table, variables, constraints):
    ''' Your code goes here'''
    if not '.' in assignment:
       return assignment
    
    next_var_index = shortest_domain_index(assignment, variables)

    #current_ordered_domain = ordered_domain(next_var_index, variables, q_table)
    current_ordered_domain = variables[next_var_index]

    for value in current_ordered_domain:
       
       assignment = assignment[: next_var_index] + value + assignment[next_var_index + 1:]

       if assignment_is_valid(next_var_index, assignment, constraints):
         
         q_table[value] += 1
         variables_copy = variables#{key: value[:] for key, value in variables.items()}
         variables = update_variables(value, next_var_index, assignment, variables, constraints)
         
         result = recursive_backtracking(assignment, q_table, variables, constraints)
         if result:
            return result

         assignment = assignment[: next_var_index] + '.' + assignment[next_var_index + 1:]

         q_table[value] -= 1
         variables = variables_copy

    return None


def assignment_is_valid(index, assignment, constraints):

   for constraint in constraints[index]:
      if constraint != index:
         if assignment[int(constraint)] == assignment[index]:
            return False

   return True

def sudoku_csp(puzzle_length):
  ''' Your code goes here '''
  n = int(math.sqrt(puzzle_length))
  rows = [[x for x in range(i * n, (i + 1) * n)] for i in range(n)]
  cols = [[x for x in range(i, puzzle_length, n)] for i in range(n)]
   
  #first_grid = [0, 1, 2, 9, 10, 11, 18, 19, 20]
  #beg_indices = [0, 3, 6, 27, 30, 33, 54, 57, 60]

  grid_size = puzzle_length // 9
  grid_row_length = int(math.sqrt(grid_size))

  first_grid = []
  for i in range(grid_row_length):
    for j in range(grid_row_length):
      first_grid.append(rows[i][j])

  beg_indices = []
  for i in range(n):
    beg_indices.append(rows[i][0])

  #grids = [[x + y for y in first_grid] for x in beg_indices]
  grids = []
  for i in range(9):
    arr = []
    for j in first_grid:
       #arr.append(j + i * grid_row_length + i // 3 * n)
       base = i // 3 * grid_row_length
       extra = i % 3 * grid_row_length
       arr.append(j + beg_indices[base] + extra)
    grids.append(arr)
   
  return rows + cols + grids


def find_grid(csp_table, x):
  grids = csp_table[-9:]
   
  for list in grids:
    if x in list:
      return list
   
  return None


def sudoku_neighbors(csp_table, len_puzzle): # {0:[0, 1, 2, 3, 4, ...., 8, 9, 18, 27, 10, 11, 19, 20], 1:
  ''' Your code goes here '''
  len_puzzle_sqrt = math.sqrt(len_puzzle)
  len_puzzle_sqrt = int(len_puzzle_sqrt)
  nbrs = {x: set(csp_table[x // len_puzzle_sqrt] + csp_table[(x % len_puzzle_sqrt) + len_puzzle_sqrt] + find_grid(csp_table, x)) for x in range(len_puzzle)}    # csp_table[(x % 3) + 18]
  for val in nbrs:
     nbrs[val] = list(set(nbrs[val]))
  return nbrs


# Optional helper function
def initialize_ds(puzzle, neighbors):
    ''' Your code goes here '''
    variables = {}
    vars = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    q_table = {str(i): 0 for i in range(1, 10)}
    count = 0
   
    for y in puzzle:
        if y != '.':
            #q_table[int(y)] += 1
            if y not in q_table:
               q_table[y] = 0
            q_table[y] += 1
   
    #print (vars, puzzle, q_table) 
    unassigned_variables = getVariables(puzzle)
    constraints = {}
    for x in unassigned_variables:
       constraints[x] = neighbors[x]

    for x in unassigned_variables:
      for neigh in constraints[x]:
         if puzzle[neigh] != "." and puzzle[neigh] in vars:
            vars.remove(puzzle[neigh])
               
      variables[x] = vars
      vars = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
       
    return variables, puzzle, q_table



# sum of all ascii code of each char - (length of the solution * ascii code of min char)
def checksum(solution):
   ''' write your code here'''
   return sum([ord(c) for c in solution]) - 49*81

def getVariables(puzzle):
  variables = []
  for i in range(0, len(puzzle)):
    if puzzle[i] == '.':
      variables.append(i)
  return variables


def check_valid(check_str):
    for char in check_str:
        if char not in '123456789.':
            return False
    return len(check_str) == 81


def main():
   #csp_table = sudoku_csp()   # rows, cols, and sub_blocks
   #neighbors = sudoku_neighbors(csp_table)   # each position p has its neighbors {p:[positions in same row/col/subblock], ...}
   csp_table_36 = sudoku_csp(36)  # rows, cols, and sub_blocks
   neighbors_36 = sudoku_neighbors(csp_table_36, 36)

   csp_table_81 = sudoku_csp(81)  # rows, cols, and sub_blocks
   neighbors_81 = sudoku_neighbors(csp_table_81, 81)

   start_time = time.time()
   for line, puzzle in enumerate(puzzles):
      line, puzzle = line+1, puzzle.rstrip()
      puzzle_length = len(puzzle)
      if puzzle_length == 36:
         csp_table = csp_table_36
         neighbors = neighbors_36
      elif puzzle_length == 81:
         csp_table = csp_table_81
         neighbors = neighbors_81
      else:
         csp_table = sudoku_csp(puzzle_length)  # rows, cols, and sub_blocks
         neighbors = sudoku_neighbors(csp_table, puzzle_length)

      print ("{}: {}".format(line, puzzle)) 

      start_time2 = time.time()
      solution = solve(puzzle, neighbors)
      #print ("Runtime:", (time.time() - start_time2))

      if solution == None:print ("No solution found."); break
      #else:
      print ("{}{} {}".format(" "*(len(str(line))+2), solution, checksum(solution)))
   print ("Duration:", (time.time() - start_time))

if __name__ == '__main__': main()

# Dennis Tislin, Period 5, 2026
