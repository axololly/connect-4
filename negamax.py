from enum import Enum
from game import Game
from typing import List
from copy import deepcopy

class Results(Enum):
    WIN: int = 1
    DRAW: int = 0
    LOSE: int = -1

class Negamax:
    def __init__(self, board: List[List[int]]):
        self.board = board
    
    def contains(self, sublist: List, lst: List) -> bool:
        return any(sublist == lst[i : i + len(sublist)] for i in range(len(lst) - len(sublist) + 1))

    def heuristic(self) -> int | float:
        if self.board == [[[0] for _ in range(6)] for _ in range(7)]:
            return 0

        outcome = Game(self.board).is_game_over()

        if outcome == Results.WIN:
            return 1
        elif outcome == Results.DRAW:
            return 0
        elif outcome == Results.LOSE:
            return -1
        
        my_lines_of_3 = 0
        opp_lines_of_3 = 0

        rotated_board = [
            [
                self.board[-1 - i][x] for i, _ in enumerate(self.board)
            ]
            for x, _ in enumerate(self.board[0])
        ]

        # vertical and horizontal
        for board in [self.board, rotated_board]:
            for row in board:
                for i in range(4):
                    line = row[i : i + 4]
                    
                    my_lines_of_3 += 1 if self.contains([0, 1, 1], line) else 0
                    my_lines_of_3 += 1 if self.contains([1, 1, 0], line) else 0

                    opp_lines_of_3 += 1 if self.contains([0, 2, 2], line) else 0
                    opp_lines_of_3 += 1 if self.contains([2, 2, 0], line) else 0
        
        for x_change in (1, -1):
            for i in range(3):
                for j in range(4):
                    line = [self.board[i + x][j + x * x_change] for x in range(4)]
                    
                    my_lines_of_3 += 1 if self.contains([0, 1, 1], line) else 0
                    my_lines_of_3 += 1 if self.contains([1, 1, 0], line) else 0

                    opp_lines_of_3 += 1 if self.contains([0, 2, 2], line) else 0
                    opp_lines_of_3 += 1 if self.contains([2, 2, 0], line) else 0
        
        return (my_lines_of_3 - opp_lines_of_3) / 8

    def get_children(self, board: List[List[int]]) -> List[List[List[int]]]:
        children = []

        for move in Game(board).valid_moves():
            new_board = deepcopy(board)
            new_board.place_counter(move)
            children.append(new_board)
        
        return children

    def negamax(self, state: List[List[int]], depth: int, alpha: int, beta: int, maximizing_player: bool) -> int | float:
        game = Game(state)
        
        if depth == 0 or game.is_game_over():
            return self.heuristic()

        if maximizing_player:
            maxEval = float('-inf')

            for position in self.get_children(game.board):                
                evaluation = self.negamax(position, depth - 1, alpha, beta, False)

                maxEval = max(maxEval, evaluation)
                alpha = max(alpha, evaluation)
                
                if beta <= alpha:
                    break
            
            return maxEval
        
        else:
            minEval = float('inf')

            for position in self.get_children(game.board):
                evaluation = self.negamax(position, depth - 1, alpha, beta, True)

                minEval = min(minEval, evaluation)
                beta = min(beta, evaluation)

                if beta <= alpha:
                    break
            
            return minEval