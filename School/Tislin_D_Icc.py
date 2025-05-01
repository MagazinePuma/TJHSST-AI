import sys; args = sys.argv[1:]

def solve(word, starting_loc):
    board = [[],[],[],[]]
    words = {"A":1, "E":1, "D":2, "R":2, "B":3, "M":3, "V":4, "Y":4, "J":8, "X":8}

    for row in range(4):
        for col in range(10):
            board[row].append((row * 10) + (col + 1))

    # print(board)
    x = (int(starting_loc) % 10) - 1
    # print(x)
    y = int(starting_loc) // 10
    # print(y)
    score = 0

    if (x + len(word)) <= 10:
        tl = False
        dw = False
        tw = False
        multiples = [3, 9, 15, 21, 27, 33, 39]
        idx = 0
        for letter in word:
            if board[y][x + idx] % 3 == 0 and board[y][x + idx] in multiples:   # word.index(letter)
                score += words[letter] * 2 # board[x + word.index(letter)] * 2
                idx += 1
                dl = True
                # print(board[y][x + idx])
                # print("double letter")

            elif board[y][x + idx] % 5 == 0 and tl == False:
                score += words[letter] * 3 # board[x + word.index(letter)] * 3
                idx += 1
                tl = True
                # print(board[y][x + idx])
                # print("tripple letter")

            elif board[y][x + idx] % 7 == 0 and dw == False and tw == False:
                copys = score
                score += words[letter] #(words[letter] + copys) * 2
                idx += 1
                dw = True
                # print(board[y][x + idx])
                # print("double word")

            elif board[y][x + idx] % 8 == 0 and tw == False and dw == False:
                copys = score
                score += words[letter] #(words[letter] + copys) * 3
                idx += 1
                tw = True
                # print(board[y][x + idx])
                # print("tripple word")

            else:
                score += words[letter] # board[x + word.index(letter)]
                idx += 1
                # print(board[y][x + idx])
                # print("avg")

    if dw or tw:
        if dw:
            score = score * 2
        else:
            score = score * 3
            
    return score

def main():
    print(solve(args[0], args[1]))

if __name__ == "__main__":
    main()
