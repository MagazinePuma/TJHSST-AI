import sys; args = sys.argv[1:]
import random
import re

BLOCKCHAR = "#"
OPENCHAR = "-"
PROTECTEDCHAR = "~"

def initialize(): 
    inTest = [r"^(\d+)x(\d+)$", r"^\d+$", r"^(H|V)(\d+)x(\d+)(.+)$"]
    xheight, xwidth, blockCt, dictSeen = 4, 4, 0, False
    fixedWords = []
    
    for arg in args:
        # if os.path.isfile(arg):
        #     dictLines = open(arg, "r").read().splitlines()
        #     dictSeen = True
        #     continue
        
        for testNum, retest in enumerate(inTest):
            match = re.search(retest, arg, re.I)
            if not match: continue
            if testNum == 0:
                xheight = int(match.group(1))
                xwidth = int(match.group(2))
            elif testNum == 1:
                blockCt = int(arg)
            else:
                vpos = int(match.group(2))
                hpos = int(match.group(3))
                word = match.group(4).upper()
                fixedWords.extend([(arg[0].upper(), vpos, hpos, word)])
                
    #if not dictSeen:
        #exit("whatever...")
    
    puzzle = OPENCHAR * (xheight * xwidth)
    # print(puzzle)
    # print(fixedWords)
    
    for v_or_h, row, col, word in fixedWords:
        list_puzzle = list(puzzle)
        current_ind = row * xwidth + col
        count = 0
        listw = list(word)
        
        if v_or_h == "V":
            # print(col)
            # print(current_ind)
            for i in range(current_ind, current_ind + xwidth * len(word), xwidth):
                #print(i)
                list_puzzle[i] = listw[count]
                count += 1
            
            puzzle = "".join(list_puzzle)
            
        else:
            list_puzzle[current_ind: current_ind + len(word)] = [*word]
            puzzle = "".join(list_puzzle)
            
    # print(puzzle)
    
    regpat = r"[a-zA-z]"
    puzzle = re.sub(regpat, PROTECTEDCHAR, puzzle)
    #print("before:")
    #print(display(puzzle, xheight, xwidth))
    # print(xheight)
    # print(xwidth)
    # print(puzzle)
    
    return blockCt, xheight, xwidth, OPENCHAR * (xheight * xwidth), puzzle, fixedWords

    
def display(puzzle, height, width):
    # display the puzzle in 2D
    news = ""
    
    for i in range(len(puzzle)):
        news += puzzle[i]
        if (i + 1) % width == 0:
            news += "\n"
            
    return news
    
def make_palindrome(puzzle, width, height):
    
    puzzle_list = list(puzzle)# [*puzzle]
    
    for i in range(len(puzzle_list)):
        row, col = divmod(i, width)
        current_index = row * width + col
        symmetric = ((height - row - 1) * width) + (width - col - 1)
        
        # symmetric = len(puzzle) - current_index - 1
        #print(symmetric)
        # print(current_index)
        # print(puzzle_list)
        # print(len(puzzle_list))
        
        if puzzle_list[current_index] + puzzle_list[symmetric] in {"#~", "~#"}:
            return puzzle, False
        elif puzzle_list[current_index] == PROTECTEDCHAR or puzzle_list[symmetric] == PROTECTEDCHAR:
            if puzzle_list[current_index] != PROTECTEDCHAR:
                puzzle_list[current_index] = PROTECTEDCHAR
            else:
                puzzle_list[symmetric] = PROTECTEDCHAR
                
        elif puzzle_list[current_index] == BLOCKCHAR or puzzle_list[symmetric] == BLOCKCHAR:
            if puzzle_list[current_index] != BLOCKCHAR:
                puzzle_list[current_index] = BLOCKCHAR
            else:
                puzzle_list[symmetric] = BLOCKCHAR
        
        
            
    return "".join(puzzle_list), True
    
def transpose(puzzle, newWidth):
    # rotate the board 90 degrees
    return "".join(puzzle[col::newWidth] for col in range(newWidth))

def augmented_board(word, width):
    #xw = puzzle[:]
    xw = BLOCKCHAR * (width + 3)
    xw += ("##").join([word[p: p + width] for p in range(0, len(word), width)])
    xw += BLOCKCHAR * (width + 3)
    return xw
    
def block_helper(xw, width, height, block_count):
        
    newH = len(xw) // (width + 2)
    illegRE = "[{}].?[{}][{}]".format(BLOCKCHAR, PROTECTEDCHAR, BLOCKCHAR)
    subRE = "[{}]{}(?=[{}])".format(BLOCKCHAR, OPENCHAR, BLOCKCHAR)
    subRE2 = "[{}]{}{}(?=[{}])".format(BLOCKCHAR, OPENCHAR, OPENCHAR, BLOCKCHAR)
    
    for turn in range(2):
        if re.search(illegRE, xw): 
            return xw, False
        
        xw = re.sub(subRE, BLOCKCHAR * 2, xw)
        xw = re.sub(subRE2, BLOCKCHAR * 3, xw)
        xw = transpose(xw, len(xw) // newH)
        newH = len(xw) // newH
    
    # print(xw)
    #print("before and after palindrome")
    #print(display(xw, height+2, width+2))
    symmetry, valid = make_palindrome(xw, width + 2, height + 2)
    #print("this is after palindrome")
    #print(display(symmetry, height+2, width+2))
    """
    if not valid or xw.count(BLOCKCHAR) > block_count:
        return symmetry, False
    
    if re.search(r"#(-~|~-|~~)#", symmetry) or re.search(r"#~#", symmetry):
        return symmetry, False
    
    if re.search(r"#-#", symmetry) or re.search(r"#--#", symmetry):
        if re.search(r"#-#", symmetry):
            re.sub("#-#", "###", symmetry)
        else:
            re.sub("#--#", "####", symmetry)
    
    if re.search(r"#(-~-|~--|~~-|~-~|--~|-~~)", symmetry):
        re.sub(r"#(-~-|~--|~~-|~-~|--~|-~~)", "#~~~", symmetry)
    """
    return symmetry, True
    
def area_fill(board, sp, dirs, width, height): # all open should be connected
    dirs = [-1, width, 1, -1 * width]
    
    if sp < 0 or sp >= len(board): return board #, False
    
    if board[sp] in {OPENCHAR, PROTECTEDCHAR}:
        board = board[0: sp] + '?' + board[sp + 1:]
        
        for d in dirs:
            if d == -1 and sp % width == 0: continue      # dirs[1]
            if d == 1 and sp + 1 % width == 0: continue     # dirs[1]
            board = area_fill(board, sp + d, dirs, width, height)
    
    return board

def add_block(puzzle, blockCt, width, height, pos_list):
    if puzzle.count(BLOCKCHAR) == blockCt:
        return puzzle
    elif puzzle.count(BLOCKCHAR) > blockCt or not pos_list:
        return None
    
    idx = random.choice(pos_list)
    newp = puzzle[:idx] + "#" + puzzle[idx + 1:]
    newp = augmented_board(newp, width)
    newp, check = block_helper(newp, width, height, blockCt)
    newp = take_out_boundary(newp, width, height)
    temp_list = list(set(pos_list) - {idx})
    
    if not check:
        return add_block(puzzle, blockCt, width, height, temp_list)
    
    pos_list = [i for i, c in enumerate(newp) if c not in "#~"]
    result = add_block(newp, blockCt, width, height, pos_list)
    
    if result != None:
        return result
    
    return add_block(puzzle, blockCt, width, height, temp_list)
    

def take_out_boundary(new_puz, width, height):
    new_puz, p = new_puz[width + 3:], ""
    for h in range(height):
        p += new_puz[0: width]
        new_puz = new_puz[width + 2:]
    return p

def add_words_back(puzzle, width, height, words):
    for v_or_h, row, col, word in words:
        list_puzzle = list(puzzle)
        current_ind = row * width + col
        listw = list(word)
        count = 0
        
        if v_or_h == "V":
            # for i in range(current_ind, (width - current_ind + 1) + (width * (len(word) - 2)) + (current_ind + 1), width):
            for i in range(current_ind, current_ind + width * len(word), width):
                # print(i)
                #print(count)
                list_puzzle[i] = listw[count]
                count += 1
            
            puzzle = "".join(list_puzzle)
            
        else:
            list_puzzle[current_ind: current_ind + len(word)] = [*word]
            puzzle = "".join(list_puzzle)
            
    puzzle = re.sub(PROTECTEDCHAR, OPENCHAR, puzzle)
    
    return puzzle
    
def main():
    block_count, height, width, empty_puz, puzzle, fixedWords = initialize()
    
    if block_count == height * width:
        puzzle = BLOCKCHAR * (height * width)
        #print("after (block count is equal to board size):")
        print(display(puzzle, height, width))
    else:
        xw = augmented_board(puzzle, width)
        new_puz, valid = block_helper(xw, width, height, block_count)
        puzzle = take_out_boundary(new_puz, width, height)
        # checked_puz = area_fill(puzzle, puzzle.find(OPENCHAR), [], width, height)
        # connected = checked_puz.count("?") == (len(puzzle) - puzzle.count(BLOCKCHAR))
        added = add_block(puzzle, block_count, width, height, [x for x in range(len(puzzle)) if puzzle[x] == OPENCHAR and puzzle[len(puzzle) - x - 1] == OPENCHAR])
        final = add_words_back(added, width, height, fixedWords)
        print(display(final, height, width))
        
        # if valid and connected:
        #     added = add_block(puzzle, block_count, width, height, [])
        #     print("after (passed area_fill and displaying block_helper/add_block):")
        #     print(display(new_puz, height, width))
        #     print(added)
  
if __name__ == "__main__":
    main()
    
# Dennis Tislin, Period 5, 2026