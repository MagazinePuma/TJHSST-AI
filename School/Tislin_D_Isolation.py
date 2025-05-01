# Name: Dennis Tislin, Period 5, 2026
# Date:
import random

class RandomPlayer:
   def __init__(self):
      self.white = "#ffffff" #"O"
      self.black = "#000000" #"X"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None
      self.first_turn = True
      
   def best_strategy(self, board, color):
      # Terminal test: when there's no more possible move
      #                return (-1, -1), 0
      # returns best move
      # (column num, row num), 0
      v, my_move = float("-inf"), -1
      
      for move in possible_moves:
         temp_board = make_move(move, boad)
         val = min_value(temp_board, opp_color)
         if v < val:
            v = val
            my_move = move
      
      return (my_move // y_max, my_move % y_max), v
      #return best_move, 0
      
     
   def find_moves(self, board, color):
      # finds all possible moves
      # returns a set, e.g., {0, 1, 2, 3, ...., 24} 
      # 0 5 10 15 20
      # 1 6 11 16 21
      # 2 7 12 17 22
      # 3 8 13 18 23
      # 4 9 14 19 24
      # if 2 has 'X', board = [['.', '.', 'X', '.', '.'], [col 2], .... ]
      moves_found = set()
      self.x_max = len(board)
      self.y_max = len(board[0])
      count = len([y for x in board for y in x if y != "."])
      for i in range(len(board)):
         for j in range(len(board[i])):
            if count < 2 and board[i][j] == ".":
               moves_found.add(i * self.y_max + j)
            elif (colo == self.black and board[i][j] == "X") or (color == self.white)
      return set()

class CustomPlayer:

   def __init__(self):
      self.white = "#ffffff" #"O"
      self.black = "#000000" #"X"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None
      self.first_turn = True

   def best_strategy(self, board, color):
      # returns best move
      return best_move, 0

   def minimax(self, board, color, search_depth):
      # search_depth: start from 2
      # returns best "value"
      return best_move, 1

   def negamax(self, board, color, search_depth):
      # returns best "value"
      return 1
      
   def alphabeta(self, board, color, search_depth, alpha, beta):
      # returns best "value" while also pruning
      pass

   def make_move(self, board, color, move):
      # returns board that has been updated
      stone = "X"
      if color == self.white: stone = "O"
      new_board = []
      
      for i in range(self.x_max):
         new_board +=[[]]
         for j in range(self.y_max):
            new_board[i] += [board[i][j]]
            if board[i][j] == stone:
               new_board[i][j] = "W"
               
      new_board[move[0]][move[1]] = stone
      return new_board

   def evaluate(self, board, color, possible_moves):
      # returns the utility value
      # count possible_moves (len(possible_moves)) of my turn at current board
      # opponent's possible_moves: self.find_moves(board, self.opposite_color(color))
      return 1

   def find_moves(self, board, color):
      # finds all possible moves
      return set()
   
   def min_value(self, board, color, search_depth):
      if len(possible_moves) == 0: return 1000
      elif len(self.find_moves(board, self.opposite_color[color])) == 0: return -1000
      if search_depth == 1:
         return 

