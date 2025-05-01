import sys; args = sys.argv[1:]
import random
import re

BLOCKCHAR = "#"
OPENCHAR = "-"
PROTECTEDCHAR = "~"

def initialize(): 
    inTest = [r"^\w+.txt$", r"^(\d+)x(\d+)$", r"^\d+$", r"^(H|V)(\d+)x(\d+)(.+)$"]
    xheight, xwidth, blockCt, dictSeen = 4, 4, 0, False
    fixedWords = []
    file = ""
    # blocks = []
    
    for arg in args:
        # if os.path.isfile(arg):
        #     dictLines = open(arg, "r").read().splitlines()
        #     dictSeen = True
        #     continue
        
        for testNum, retest in enumerate(inTest):
            match = re.search(retest, arg, re.I)
            if not match: continue
            if testNum == 1:
                xheight = int(match.group(1))
                xwidth = int(match.group(2))
            elif testNum == 2:
                blockCt = int(arg)
            elif testNum == 3:
                vpos = int(match.group(2))
                hpos = int(match.group(3))
                word = match.group(4).upper()
                fixedWords.extend([(arg[0].upper(), vpos, hpos, word)])
            else:
                file = arg
                
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
    
    return file, blockCt, xheight, xwidth, puzzle, fixedWords

def solve(puzzle, width, wordSet, wordPatterns, startPositions):
    for pos, l in startPositions[0]:
        sp = pos[0][0] * width + pos[0][1]
        word = puzzle[sp: sp + 1]
        
        if word == '-' * len(word): puzzle = puzzle[: sp] + random.choice(wordSet[l]) + puzzle[sp + 1:]
        
        elif word in wordPatterns:
            puzzle = puzzle[: sp] + random.choice(list(wordPatterns[word])) + puzzle[sp + 1:]
            
    return puzzle

def readWords():
    infile_list = open(args[0], "r")
    wordPatterns, wordSet = {}, {}
    
    for w in infile_list.readlines():
        w = w.strip().upper()
        l = len(w)
        
        if l in wordSet: 
            wordSet[l].append(w)
        else: 
            wordSet[l] = [w]
        
        for i, c in enumerate(w):
            nw = '-' * i + c + "-" * (1 - i - 1)
            if nw in wordPatterns: wordPatterns[nw].add(w)
            else: wordPatterns[nw] = {w}
            
    return wordSet, wordPatterns

def findStartPositions(puzzle, width, height):
    startPositions = [[], []]
    
    for r in range(height):
        c = 0
        
        while c < width:
            new_col = c
            req_len = 0
            
            if puzzle[r * width + c] == "#":
                c += 1
                continue
            
            while c < width and puzzle[r * width + c] != "#":
                req_len += 1
                c += 1
            
            if req_len >= 2:
                startPositions[0].append(([(r, new_col + i) for i in range(req_len)], req_len))
    
    for c in range(width):
        r = 0
        
        while r < height:
            new_row = c
            req_len = 0
            
            if puzzle[r * width + c] == "#":
                r += 1
                continue
            
            while r < height and puzzle[r * width + c] != "#":
                req_len += 1
                r += 1
            
            if req_len >= 2:
                startPositions[1].append(([(r, new_row + i) for i in range(req_len)], req_len))
    
    return startPositions
    
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

def valid_placement(puzzle, width, height):
    chars = [i for i in range(len(puzzle)) if puzzle[i] in {OPENCHAR, PROTECTEDCHAR}]
    
    if not chars: return False
    
    visited = set()
    future = {chars[0]}
    
    while future:
        current = future.pop()
        
        if current in visited: continue
        
        visited.add(current)
        dirs = [current - width, current + width, current - 1, current + 1]
        
        for d in dirs:
            if d < 0 or d >= len(puzzle) or puzzle[d] == "#" or d in visited:
                continue
            
            if (current % width == 0 and d % width == width - 1) or (current % width == width - 1 and d % width == 0):
                continue
            
            if puzzle[d] in {OPENCHAR, PROTECTEDCHAR}:
                future.add(d)
    
    tot_op = sum(1 for col in puzzle if col in {OPENCHAR, PROTECTEDCHAR})
    return len(visited) >= tot_op * 0.95

def check_length(puzzle, width, height):
    for r in range(height):
        word = ""
        
        for c in range(width):
            car = puzzle[r * width + c]
            
            if car not in {BLOCKCHAR, PROTECTEDCHAR}:
                word += car
            else:
                if 0 < len(word) < 3:
                    return False
                
                word = ""
        
        if 0 < len(word) < 3:
            return False
    
    for c in range(width):
        word = ""
        
        for r in range(height):
            car = puzzle[r * width + c]
            
            if car not in {BLOCKCHAR, PROTECTEDCHAR}:
                word += car
            else:
                if 0 < len(word) < 3:
                    return False
                
                word = ""
        
        if 0 < len(word) < 3:
            return False
    
    return True

def area_fill(board, sp, dirs, width, height): # all open should be connected
    dirs = [-1, width, 1, -1 * width]
    
    if sp < 0 or sp >= len(board) or board[sp] not in {OPENCHAR, PROTECTEDCHAR}: return board #, False
    
    board = board[:sp] + '?' + board[sp + 1:]
        
    for d in dirs:
        if d == -1 and sp % width == 0: continue      # dirs[1]
        if d == 1 and sp + 1 % width == 0: continue     # dirs[1]
        
        pos = sp + d
        
        if 0 <= pos < len(board):
            board = area_fill(board, pos, dirs, width, height)
    
    return board

def add_block(puzzle, blockCt, width, height, pos_list):
    if puzzle.count(BLOCKCHAR) == blockCt:
        return puzzle
    elif puzzle.count(BLOCKCHAR) > blockCt or not pos_list:
        return None
    
    # pos_list = [i for i in pos_list if i not in [r * width + c for r, c in preserve]]
    
    random.shuffle(pos_list)
    
    for idx in pos_list:
        # for row, col in preserve:
        #     if idx == row * width + col:
        #         continue
            
        newp = puzzle[:idx] + "#" + puzzle[idx + 1:]
        newp = augmented_board(newp, width)
        newp, check = block_helper(newp, width, height, blockCt)
        newp = take_out_boundary(newp, width, height)
        
        if check and valid_placement(newp, width, height):
            result = add_block(newp, blockCt, width, height, [i for i, c in enumerate(newp) if c not in {BLOCKCHAR, PROTECTEDCHAR}])

            if result != None:
                return result
    
    return None

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
    file_name, block_count, height, width, puzzle, fixedWords = initialize()
    
    if block_count == height * width:
        puzzle = BLOCKCHAR * (height * width)
        #print("after (block count is equal to board size):")
        print(display(puzzle, height, width))
    else:
        xw = augmented_board(puzzle, width)
        new_puz, valid = block_helper(xw, width, height, block_count)
        puzzle = take_out_boundary(new_puz, width, height)
        # checked_puz = area_fill(puzzle, puzzle.find(OPENCHAR), [], width, height)
        # connected = area_helper(puzzle, width, height)
        # added = add_block(puzzle, block_count, width, height, [x for x in range(len(puzzle)) if puzzle[x] == OPENCHAR and puzzle[len(puzzle) - x - 1] == OPENCHAR])
        # final = add_words_back(added, width, height, fixedWords)
        # print(file_name)
        # print(puzzle)
        word_set, word_pat = readWords()
        positions = findStartPositions(puzzle, width, height)
        soln = solve(puzzle, width, word_set, word_pat, positions)
        print(display(soln, height, width))
        
        # for i in range(500):
        #     added = add_block(puzzle, block_count, width, height, [x for x in range(len(puzzle)) if puzzle[x] == OPENCHAR and puzzle[len(puzzle) - x - 1] == OPENCHAR])
            
        #     if added:
        #         final = add_words_back(added, width, height, fixedWords)
                
        #         if check_length(final, width, height):
        #             print(display(final, height, width))
        #             return
                
        # print(display(final, height, width))
        
        # if connected:
        #     print(display(final, height, width))
        # else:
        #     print("Not connected")
        
        # if valid and connected:
        #     added = add_block(puzzle, block_count, width, height, [])
        #     print("after (passed area_fill and displaying block_helper/add_block):")
        #     print(display(new_puz, height, width))
        #     print(added)
  
if __name__ == "__main__":
    main()
    
# Dennis Tislin, Period 5, 2026