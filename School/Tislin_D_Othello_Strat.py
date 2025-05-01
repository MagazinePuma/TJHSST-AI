class Strategy:

   def __init__(self):
      self.white = "o"
      self.black = "x"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None
      self.static_weight_board = [[4, -3, 2, 2, 2, 2, -3, 4], 
                                  [-3, -4, -1, -1, -1, -1, -4, -3], 
                                  [2, -1, 1, 0, 0, 1, -1, 2], 
                                  [2, -1, 0, 1, 1, 0, -1, 2], 
                                  [2, -1, 0, 1, 1, 0, -1, 2], 
                                  [2, -1, 1, 0, 0, 1, -1, 2], 
                                  [-3, -4, -1, -1, -1, -1, -4, -3], 
                                  [4, -3, 2, 2, 2, 2, -3, 4]]

   def best_strategy(self, board, color, best_move, still_running, time_limit): # should look like alpha beta stuff
      # returns best move
      board = [list(board[x - 8 : x]) for x in range(0, len(board), 8) if x != 0]
      self.x_max, self.y_max = len(board[0]), len(board)

      if color == "x" or color == self.black:
         color = "x"
      else:
         color = "o"
      
      ''' Your code goes here '''
      
      v = float("-inf")
      possible_moves = self.find_moves(board, color) # ex: {19: [3, 3]}
      alpha = float("-inf")
      beta = float("inf")
      #print(possible_moves)
      #if not possible_moves: return None, 0
      strategic_depth = 4
      # moves_left = self.stones_left(board)
      
      # if moves_left <= 35: # middle - game
      #    strategic_depth = 4
      # elif moves_left <= 15:  # end - game
      #    strategic_depth = 3
         
      if possible_moves:
         for coord, flipped in possible_moves.items():
            copy = [row[:] for row in board]
            copied = self.make_move(copy, color, list(divmod(coord, 8)), flipped)
            strat_num = self.alphabeta(copied, color, strategic_depth, alpha, beta)
            #print(strat_num, v)
            
            if strat_num > v:
               v = strat_num
               # print(coord)
               strat =  list(divmod(coord, 8))
            
            alpha = max(alpha, v)
         
         # print(strat, v)
         best_move.value = coord
      else:
         best_move.value = None
   
   def terminal_test(self, board):
      # board = [list(board[x - 8 : x]) for x in range(0, len(board), 8) if x != 0]
      
      if self.stones_left(board) == 0:
         return True
      elif not self.find_moves(board, "o") and not self.find_moves(board, "x"):
         return True
      else:
         return False
   
   def max_value_ab(self, board, color, search_depth, alpha, beta):
      if color == "x" or color == self.black:
         color = "x"
      else:
         color = "o"
      
      possible_moves = self.find_moves(board, color)
      v = float("-inf")
      
      if self.terminal_test(board) or search_depth == 0:
         return self.evaluate(board, color, possible_moves)
      
      if possible_moves:
         for coord, flipped in possible_moves.items():
            copy = [row[:] for row in board]
            copied = self.make_move(copy, color, list(divmod(coord, 8)), flipped)
            v = max(v, self.min_value_ab(copied, self.opposite_color[color], search_depth - 1, alpha, beta))
            if v >= beta: return v
            alpha = max(alpha, v)
         
         return v
      else:
         return self.evaluate(board, color, possible_moves)
      
   def min_value_ab(self, board, color, search_depth, alpha, beta):
      if color == "x" or color == self.black:
         color = "x"
      else:
         color = "o"
      
      v = float("inf")
      possible_moves = self.find_moves(board, color)
      
      if self.terminal_test(board) or search_depth == 0:
         return self.evaluate(board, color, possible_moves)
      
      if possible_moves:
         for coord, flipped in possible_moves.items():
            copy = [row[:] for row in board]
            copied = self.make_move(copy, color, list(divmod(coord, 8)), flipped)
            v = min(v, self.max_value_ab(copied, self.opposite_color[color], search_depth - 1, alpha, beta))
            if v <= alpha: return v
            beta = min(beta, v)
         
         return v
      else:
         return self.evaluate(board, color, possible_moves)

   # def minimax(self, board, color, search_depth):
   #  # returns best "value"
   #    # if color == "#000000" or color == self.black:
   #    #    color = "@"
   #    # else:
   #    #    color = "O"
         
   #    return self.max_value_minimax(board, color, search_depth)

   def negamax(self, board, color, search_depth):
    # returns best "value"
      return 1
      
   def alphabeta(self, board, color, search_depth, alpha, beta):
    # returns best "value" while also pruning
      # board = [list(board[x - 8 : x]) for x in range(0, len(board), 8) if x != 0]
      return self.max_value_ab(board, color, search_depth, alpha, beta)

   def make_key(self, board, color):
    # hashes the board
      if color == "x" or color == self.black:
         color = "x"
      else:
         color = "o"
         
      weight_dict = {}
      
      for row in range(8):
         for col in range(8):
            weight_dict.update({col * self.y_max + row: self.static_weight_board[col][row]})
            
      return weight_dict
   
   def weight_sum(self, board, color):
      # board = [list(board[x - 8 : x]) for x in range(0, len(board), 8) if x != 0]
      
      if color == "x" or color == self.black:
         color = "x"
      else:
         color = "o"
         
      count = 0
      
      for row in range(8):
         for col in range(8):
            if board[row][col] == color:
               count += self.static_weight_board[row][col]
      
      return count

   def stones_left(self, board):
    # returns number of stones that can still be placed
      # board = [list(board[x - 8 : x]) for x in range(0, len(board), 8) if x != 0]
      return sum([row.count(".") for row in board])

   def make_move(self, board, color, move, flipped):
    # returns board that has been updated
      # board = [list(board[x - 8 : x]) for x in range(0, len(board), 8) if x != 0]
      
      if color == "x" or color == self.black:
         color = "x"
      else:
         color = "o"
      
      total_flipped = [move]
      # print(total_flipped)
      # print(move)
      
      if flipped:
         total_flipped += flipped
      
      for change in total_flipped:
         # print(change)
         col, row = change
         board[row][col] = color
      
      return board

   def evaluate(self, board, color, possible_moves): # mobility heuristic function or corner 
    # returns the utility value
      # board = [list(board[x - 8 : x]) for x in range(0, len(board), 8) if x != 0]
      
      if color == "x" or color == self.black:
         color = "x"
      else:
         color = "o"
         
      final_score = 0
      # moves_left = self.stones_left(board)

      my_moves = self.weight_sum(board, color)
      opponent_moves = self.weight_sum(board, self.opposite_color[color])
      
      # print("corners")
      final_score += my_moves - opponent_moves
      
      # my_moves = self.corner_count(board, color) # possible_moves
      # opponent_moves = self.corner_count(board, self.opposite_color[color])
      
      # if (my_moves + opponent_moves) != 0:
      #    corner_value = 100 * (my_moves - opponent_moves) / (my_moves + opponent_moves)
      # else:
      #    corner_value = 0
         
      # final_score += corner_value
      
      # elif moves_left >= 15:
      my_moves = possible_moves
      opponent_moves = self.find_moves(board, self.opposite_color[color])
      
      if (len(my_moves) + len(opponent_moves)) != 0:
         mobility_value = 100 * (len(my_moves) - len(opponent_moves)) / (len(my_moves) + len(opponent_moves))
      else:
         mobility_value = 0
      
      # print("mobility")
      final_score += mobility_value

      final_score += 100 * (self.score(board, color) - self.score(board, self.opposite_color[color])) / (self.score(board, color) + self.score(board, self.opposite_color[color]))
      
      return final_score

   def corner_count(self, board, color):
      # board = [list(board[x - 8 : x]) for x in range(0, len(board), 8) if x != 0]
      
      if color == "x" or color == self.black:
         color = "x"
      else:
         color = "o"
         
      count = 0
      board_corners = [[0, 0], [7, 0], [0, 7], [7, 7]]
      
      for corner in board_corners:
         col, row = corner
         if board[col][row] == color:
            count += 1
      
      return count
   
   def score(self, board, color):
    # returns the score of the board 
      # board = [list(board[x - 8 : x]) for x in range(0, len(board), 8) if x != 0]
      
      if color == "x" or color == self.black:
         color = "x"
      else:
         color = "o"
         
      return sum([row.count(color) for row in board]) 

   def find_moves(self, board, color):
    # finds all possible moves
      # board = [list(board[x - 8 : x]) for x in range(0, len(board), 8) if x != 0]
               
      if color == "x" or color == self.black:
         color = "x"
      else:
         color = "o"
         
      self.x_max, self.y_max = len(board[0]), len(board)
      moves_found = {}
      
      for i in range(len(board)):
         for j in range(len(board[i])):
            flipped_stones = self.find_flipped(board, i, j, color)
            if flipped_stones:
               moves_found.update({i * self.y_max + j: flipped_stones})
               
      #print(moves_found)
      return moves_found
      #return {}

   def find_flipped(self, board, x, y, color):
    # finds which chips would be flipped given a move and color
      # board = [list(board[x - 8 : x]) for x in range(0, len(board), 8) if x != 0]
      
      self.x_max = len(board)
      self.y_max = len(board[0])
      flipped_stones = []
      
      if board[x][y] != ".":
         return []
      
      if color == "x" or color == self.black:
         color = "x"
      else:
         color = "o"
      # color = self.opposite_color[color]
      
      for incr in self.directions:
         temp_flip = []
         x_pos = x + incr[0]
         y_pos = y + incr[1]
         
         while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
            if board[x_pos][y_pos] == ".":
               break
            if board[x_pos][y_pos] == color:
               flipped_stones += temp_flip
               break
            
            temp_flip.append([x_pos, y_pos])
            x_pos += incr[0]
            y_pos += incr[1]
            
      return flipped_stones