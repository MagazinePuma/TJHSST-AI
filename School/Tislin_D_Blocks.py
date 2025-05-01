import sys; args = sys.argv[1:]
import re, random

def select_unassigned_var(assignment):
    #return random.randint(0, len(assignment) - 1)
    return assignment.index(".")

def is_valid(pair, container, assignment, var):
    cheight, cwidth = container
    pheight, pwidth = pair
    vars = []
    valid = False
    
    if assignment[var] == "x":
        for x in range(0, len(assignment)):
            if assignment[x] == ".":
                vars.append(x)
    
    row, col = var // cwidth, var % cwidth
    
    if vars:
        for idx in vars:
            row = idx // cwidth
            col = idx % cwidth
            
            if (row + pheight) <= cheight and (col + pwidth) <= cwidth:
                columns = [n for n in range(col, col + pwidth)]
                for x in range(col + row * cwidth, (col + row * cwidth) + (pwidth * pheight) + (cwidth - pwidth) * (pheight - 1)):
                    if x % cwidth in columns:
                        if assignment[x] == "x":
                            valid = False
                            break
                        valid = True
            if valid:
                return idx, True 
        
        return False
            
    if (row + pheight) <= cheight and (col + pwidth) <= cwidth:
        columns = [n for n in range(col, col + pwidth)]
        for x in range(col + row * cwidth, (col + row * cwidth) + (pwidth * pheight) + (cwidth - pwidth) * (pheight - 1)): # pheight * pwidth + (pwidth - cwidth) * pheight
            if x % cwidth in columns:
                if assignment[x] == "x":
                    return False
        return var, True
    
    else: return False

# 4x4   1 2 - 5 6
# 0, 0 + 4 + 2 * 1 = 0, 0 + 4 + 2 = 0, 6
'''
. . . . 
. x x . 
. x x . 
. . . .

'''
# 1, 1 + 9 + 1 * 2 = 1, 12
'''
x x x x
x x x x 
. . x x 
. . . .

'''

def add_block(pair, container, assignment, idx):
    container_height, container_width = container
    height, width = pair
    columns = [n for n in range(idx % container_width, idx % container_width + width)]
    na = assignment[:]
    for x in range(idx % container_width + (idx // container_width) * container_width, (idx % container_width + (idx // container_width) * container_width) + (width * height) + (container_width - width) * (height - 1)):
        if x % container_width in columns:
            na[x] = "x"
    return na   
def make_block(pairs, assignment, final_pairs):
    container_height, container_width = pairs[0]
    # assignment = "".join(["." for x in range(container_height * container_width)])
    sorted_pairs = sort_pairs(pairs[1:])
    # print(sorted_pairs[::-1])
    return recur_blocks(pairs[0], sorted_pairs[::-1], assignment, final_pairs)

def recur_blocks(container, pairs, assignment, final_pairs):
    
    if "." not in assignment:
        return final_pairs #there's any '.' in assignment??? -> return final_pairs
    
    #copied = sorted_pairs
    #copya = assignment
    # final_pairs = set()
    var = assignment.index(".")#select_unassigned_var(assignment)
    # global copyp 
    # copyp = [x for x in pairs]
    """
    if len(sorted_pairs) == 1: # and final_area(sorted_pairs) == assignment.count("x"):
        if (container_height * container_width) - find_area(pairs) != 0:
            for x in range((container_height * container_width) - final_area(final_pairs)):
                final_pairs.append((1, 1))
        return final_pairs#, "".join(assignment)
    """
    
    for pair in pairs:
        height, width = pair
        rotate = (width, height)
        # print(var, pair)
        if is_valid(pair, container, assignment, var) != False:
            idx, boo = is_valid(pair, container, assignment, var)
            na = add_block(pair, container, assignment, idx)
            fp = final_pairs + [pair]
            # pp = [pr for pr in pairs if pr != pair]
            pp = [pr for pr in pairs[1:]]
            result = recur_blocks(container, pp, na, fp)
            if result != None: return result #, "".join(assignment)
            
            else:
                if is_valid(rotate, container, assignment, var) != False:
                    idx, boo = is_valid(rotate, container, assignment, var)
                    na = add_block(rotate, container, assignment, idx)
                    fp = final_pairs + [rotate]
                    # pp = [pr for pr in pairs if pr != rotate]
                    pp = [pr for pr in pairs[1:]]
                    result = recur_blocks(container, pp, na, fp)
                # return make_blocks(sorted_pairs, assignment, final_pairs)
                    if result != None: return result #, "".join(assignment)
                    
        elif is_valid(rotate, container, assignment, var) != False:
            idx, boo = is_valid(rotate, container, assignment, var)
            na = add_block(rotate, container, assignment, idx)
            fp = final_pairs + [rotate]
            # pp = [pr for pr in pairs if pr != rotate]
            pp = [pr for pr in pairs[1:]]
            result = recur_blocks(container, pp, na, fp)
            # return make_blocks(sorted_pairs, assignment, final_pairs)
            if result != None: return result #, "".join(assignment)
            
    return None
    #return recur_blocks(container, copyp, ["." for x in range(container[0] * container[1])], [])

def final_area(final_pairs):
    blocks_area = 0
    
    for pair in final_pairs:
        height, width = pair
        area = height * width
        blocks_area += area
    
    return blocks_area
    
def find_area(pairs):
    blocks_area = 0
    
    for pair in pairs[1:]:
        height, width = pair
        area = height * width
        blocks_area += area
    
    return blocks_area

def solvable(pairs):
    container_height, container_width = pairs[0]
    container_area = container_height * container_width
    blocks_area = 0
    max_dim = 0
    
    for pair in pairs[1:]:
        height, width = pair
        max_dim = max(max_dim, max(height, width))
        # if height > container_height or height > container_width or width > container_height or width > container_width:
        #     return False
        area = height * width
        blocks_area += area
    
    return container_area >= blocks_area and max_dim <= max(container_height, container_width)

def sort_pairs(pairs):
    area_list = sorted([h * w for h, w in pairs])
    final_sort = []
    copyp = [tup for tup in pairs]
    
    for area in area_list:
        for pair in pairs:
            height, width = pair
            if height * width == area and pair in copyp:
                final_sort.append(pair)
                copyp.remove(pair)
    
    return final_sort

def main():
    # finditer returns a list of matches: finditer(pattern, subject, options)
    matches = re.finditer(r"(\d+)( |x)(\d+)", ' '.join(args), re.I)
    # group(0) is the entire match, group(1 or higher) is captured
    pairs = [(int(m.group(1)), int(m.group(3))) for m in matches]
    #print(pairs)
    # board_size = pairs[0] # the first pair is the board size
    height, width = pairs[0]
    solve = solvable(pairs)
    
    if not solve: 
        print("Impossible to solve")
        return
    
    assignment = ["." for x in range(height * width)]
    final_pairs = list()
    #solutionp, solutiona = make_blocks(pairs, assignment, final_pairs)
    #print("Container:", str(height) + "h x " + str(width) + "w")
    #print("Pairs:", pairs[1:])
    #print("Solvable?", solve)
    pairs_area = find_area(pairs)
    container_area = height * width
    pairs = pairs + [(1, 1) for d in range(container_area - pairs_area)]
    #print(pairs)
    solution = make_block(pairs, assignment, final_pairs)
    # if find_area(pairs) == len(assignment):
    #     print("Decomposition:", pairs[1:]) #, "".join(["x" for x in range(height * width)])
    #     return
    
    # while solution == None:
    #     solution = make_blocks(pairs, assignment, final_pairs)
            
    #print("Decomposition:", solution)
    #print("Assignment:", solutiona)
    decomp = [str(p[0]) + "x" + str(p[1]) for p in solution]
    # how you are supposed to print the solution
    print("Decomposition:", ' '.join(decomp))

if __name__ == '__main__': main()

# Dennis Tislin, Period 5, 2026