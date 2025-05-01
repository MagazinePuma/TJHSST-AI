# Name: Dennis Tislin
# Period: 5
from tkinter import *
from graphics import *
import random

def check_complete(assignment, vars, adjs):
    # check if assignment is complete or not. Goal_Test
    ''' your code goes here '''
    return len(assignment) == len(vars)

def select_unassigned_var(assignment, vars, adjs):
    # Select an unassigned variable - forward checking, MRV, or LCV
    # returns a variable
    ''' your code goes here '''
    return random.choice([x for x in vars.keys() if x not in assignment])    #forward checking

def isValid(value, var, assignment, variables, adjs):
    # value is consistent with assignment
    # check adjacents to check 'var' is working or not.
    ''' your code goes here '''
    return var in assignment and variables[var] == value

def backtracking_search(variables, adjs, shapes, frame):
    return recursive_backtracking({}, variables, adjs, shapes, frame)

def recursive_backtracking(assignment, variables, adjs, shapes, frame):
    # Refer the pseudo code given in class.
    ''' your code goes here '''
    if check_complete(assignment, variables, adjs): return assignment
    
    var = select_unassigned_var(assignment, variables, adjs)
    for x in variables[var]:
        if isValid(x, var, assignment, variables, adjs):
            assignment[var] = x
            result = recursive_backtracking(assignment, variables, adjs, shapes, frame)
        if result != None: return result
        assignment[var].remove(x)
    
    return None

# return shapes as {region:[points], ...} form
def read_shape(filename):
    infile = open(filename)
    region, points, shapes = "", [], {}
    for line in infile.readlines():
        line = line.strip()
        if line.isalpha():
            if region != "": shapes[region] = points
            region, points = line, []
        else:
            x, y = line.split(" ")
            points.append(Point(int(x), 300-int(y)))
    shapes[region] = points
    return shapes

# fill the shape
def draw_shape(points, frame, color):
    shape = Polygon(points)
    shape.setFill(color)
    shape.setOutline("black")
    shape.draw(frame)
    space = [x for x in range(9999999)] # give some pause
    
def main():
    regions, variables, adjacents = [], {}, {}
    
    # Read mcNodes.txt and store all regions in regions list
    ''' your code goes here '''
    x = open("mcNodes.txt", "r")
    for node in x.readlines():
        w = node.split()
        regions.append(w)
        
    # Fill variables by using regions list -- no additional code for this part
    for r in regions: variables[r] = {'red', 'green', 'blue'}
    
    # Read mcEdges.txt and fill the adjacents. Edges are bi-directional.
    ''' your code goes here '''
    x = open("mcEdges.txt", "r")
    for node in x.readlines():
        w = node.split()
        if w[0] in adjacents:
            adjacents[w[0]].add(w[1])
        else:
            adjacents[w[0]] = set()
            adjacents[w[0]].add(w[1])
    
    # Set graphics -- no additional code for this part
    frame = GraphWin('Map', 300, 300)
    frame.setCoords(0, 0, 299, 299)
    shapes = read_shape("mcPoints.txt")
    for s, points in shapes.items():
        draw_shape(points, frame, 'white')
        # solve the map coloring problem by using backtracking_search -- no additional code for this part
    solution = backtracking_search(variables, adjacents, shapes, frame)
    print(solution)
    mainloop()

if __name__ == '__main__':
    main()

''' Sample output:
{'WA': 'red', 'NT': 'green', 'SA': 'blue', 'Q': 'red', 'NSW': 'green', 'V':
'red', 'T': 'red'}
By using graphics functions, visualize the map.
'''