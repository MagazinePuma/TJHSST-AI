import random

def check_complete(assignment, variables, adjs):
    return len(assignment) == 8

def select_unassigned_var(assignment, variables, adjs):
    return random.choice(variables)

def is_valid(val, assignment, variables, adjs):
    if val in assignment: return False
    for x in assignment:
        if x in adjs[val]: return False
    """
    for x in adjs[val]:
        if x in assignment:
            if assignment[x] == val:
                return False
    """
    return True

def backtracking_search(variables, adjs):
    assignment = set()
    return recursive_backtracking(assignment, variables, adjs)

def recursive_backtracking(assignment, variables, adjs):
    #if(check_complete(assignment, variables, adjs)):
        #return assignment # {", ".join(str(x) for x in sorted(assignment))}
    #solutions = set()
    #var = select_unassigned_var(assignment, variables, adjs)
    if len(assignment) == 8: return assignment
    var = random.choice([x for x in range(20)])
    for val in range(20): # adjs[var]:
        if is_valid(val, assignment, variables, adjs):
            copya = assignment.copy()
            assignment.add(val)
            result = recursive_backtracking(assignment, variables, adjs)
            if result != None:
                #print(assignment)
                return result
                #solutions.update(result)
            assignment = copya
    #if not solutions: return None
    
    return None #solutions

def solve():
    return backtracking_search([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19], {0: [1,10,19], 1: [0,2,8], 2: [1,6,3], 3: [2,4,19], 4: [17,3,5], 5: [6,15,4], 6: [2,5,7], 7: [8,14,6], 8: [7,9,1], 9: [8,13,10], 10: [9,11,0], 11:[12,10,18], 12: [16,13,11], 13: [14,9,12], 14: [7,13,15], 15: [5,16,14], 16: [15,12,17], 17: [4,18,16], 18: [17,19,11], 19: [0,3,18]})

def main():
    print(solve())
    #solve()

if __name__ == "__main__":
    main()

# Dennis Tislin, Period 5, 2026