from enum import Enum
from game import Game, Outcomes
from typing import List, Tuple
from copy import deepcopy

class Results(Enum):
    WIN: int = 1
    DRAW: int = 0
    LOSE: int = -1

class Players(Enum):
    P1: int = 1
    P2: int = -1

class Negamax:
    def __init__(self, board: List[List[int]]):
        self.board = board
        self.iterations = 0
    
    def contains(self, sublist: List, lst: List) -> bool:
        return any(sublist == lst[i : i + len(sublist)] for i in range(len(lst) - len(sublist) + 1))

    def heuristic(self, board: List[List[int]]) -> int | float:
        if board == [[[0] for _ in range(6)] for _ in range(7)]:
            return 0

        outcome = Game(board).is_game_over()

        if outcome is Outcomes.P1_WIN:
            return 1
        elif outcome is Outcomes.DRAW:
            return 0
        elif outcome is Outcomes.P2_WIN:
            return -1
        
        my_lines_of_nearly_3 = 0
        opp_lines_of_nearly_3 = 0

        my_lines_of_nearly_4 = 0
        opp_lines_of_nearly_4 = 0

        rotated_board = [
            [
                board[-1 - i][x] for i, _ in enumerate(board)
            ]
            for x, _ in enumerate(self.board[0])
        ]

        # vertical and horizontal
        for board in [board, rotated_board]:
            for row in board:
                for i in range(4):
                    line = row[i : i + 4]
                    
                    my_lines_of_nearly_3 += 1 if self.contains([0, 1, 1], line) else 0
                    my_lines_of_nearly_3 += 1 if self.contains([1, 1, 0], line) else 0

                    opp_lines_of_nearly_3 += 1 if self.contains([0, 2, 2], line) else 0
                    opp_lines_of_nearly_3 += 1 if self.contains([2, 2, 0], line) else 0

                    my_lines_of_nearly_4 += 1 if self.contains([0, 1, 1, 1], line) else 0
                    my_lines_of_nearly_4 += 1 if self.contains([1, 1, 1, 0], line) else 0

                    opp_lines_of_nearly_4 += 1 if self.contains([0, 2, 2, 2], line) else 0
                    opp_lines_of_nearly_4 += 1 if self.contains([2, 2, 2, 0], line) else 0
        
        for x_change in (1, -1):
            for i in range(3):
                for j in range(3):
                    line = [board[i + x][j + x * x_change] for x in range(4)]
                        
                    my_lines_of_nearly_3 += 1 if self.contains([0, 1, 1], line) else 0
                    my_lines_of_nearly_3 += 1 if self.contains([1, 1, 0], line) else 0

                    opp_lines_of_nearly_3 += 1 if self.contains([0, 2, 2], line) else 0
                    opp_lines_of_nearly_3 += 1 if self.contains([2, 2, 0], line) else 0

                    my_lines_of_nearly_4 += 1 if self.contains([0, 1, 1, 1], line) else 0
                    my_lines_of_nearly_4 += 1 if self.contains([1, 1, 1, 0], line) else 0
        
        return 1.75 * (my_lines_of_nearly_4 - opp_lines_of_nearly_4) / 7 + 1.25 * (my_lines_of_nearly_3 - opp_lines_of_nearly_3) / 7

    def get_children(self, board: List[List[int]], *, player: int) -> Tuple[int, List[List[int]]]:
        children = []

        for move in Game(board).valid_moves():
            new_board = deepcopy(board)
            Game(new_board).place_counter(move, player)
            children.append((move, new_board))
        
        return children

    def negamax(self, state: List[List[int]], depth: int, alpha: int, beta: int) -> int | float:
        self.iterations += 1
        game = Game(state)
        
        if depth == 0 or game.is_game_over() != Outcomes.NONE:
            return self.heuristic(state)

        value = float('-inf')

        for _, position in self.get_children(game.board, player = 1 if self.min_or_max(state) == Players.P1 else 2):
            value = max(value, -self.negamax(position, depth - 1, alpha, beta))
            alpha = max(alpha, value)
                
            if beta <= alpha:
                break
            
        return value
    
    def min_or_max(self, state: List[List[int]] = None):
        state = state or self.board

        count_1s = sum(row.count(1) for row in state)
        count_2s = sum(row.count(2) for row in state)

        if count_1s - count_2s not in (1, 0, -1):
            raise Exception(f"Invalid board state. Player 1 has {count_1s} counters and Player 2 has {count_2s} counters.")

        return Players.P1 if count_1s == count_2s else Players.P2
    
    def get_best_move(self, state: List[List[int]] = None, depth: int = 10) -> int:
        state = state or self.board
        
        best_move = None
        
        max_eval = float('-inf')

        for move, next_position in self.get_children(state, player = 1 if self.min_or_max(state) == Players.P1 else 2):
            evaluation = -self.negamax(next_position, depth, float('-inf'), float('inf'))

            print(move, evaluation)

            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
        
        return best_move