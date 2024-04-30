from typing import List, NewType
from enum import Enum

Outcome = NewType("Outcome", int)

class Outcomes(Enum):
    P1_WIN: Outcome = 1
    P2_WIN: Outcome = -1
    NONE: Outcome = False
    DRAW: Outcome = 0

class Game:
    STARTING_BOARD = [[0 for _ in range(7)] for _ in range(6)]
    
    def __init__(self, board: List[List[int]] = None):
        self.board = board or self.STARTING_BOARD
        self.current_player = 1

    def valid_moves(self) -> List[int]:
        return [i for i, piece in enumerate(self.board[0]) if piece == 0]

    def place_counter(self, column: int) -> List[List[int]] | bool:
        try:
            open_space = [i for i in range(6) if self.board[i][column] == 0][-1]
        except IndexError:
            return False

        self.board[open_space][column] = self.current_player

        return self.board

    def is_game_over(self) -> Outcome:
        if not self.valid_moves():
            return Outcomes.DRAW
        
        # rotate the board to make searching columns easier
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
                    
                    if len(set(line)) == 1 and 0 not in line:
                        return Outcomes.P1_WIN if line[0] == 1 else Outcomes.P2_WIN

        # diagonals
        for x_change in (1, -1):
            for i in range(3):
                for j in range(4):
                    line = [self.board[i + x][j + x * x_change] for x in range(4)]
                    
                    if len(set(line)) == 1 and 0 not in line:
                        return Outcomes.P1_WIN if line[0] == 1 else Outcomes.P2_WIN
        
        return Outcomes.NONE

    def display_board(self, _print: bool = True) -> str:
        new_board = "\n".join([
            "".join(map(str, row)) \
                .replace('0', '⬛') \
                .replace('1', '🔴') \
                .replace('2', '🟡')
            for row in self.board
        ])

        if _print:
            print(new_board)

        return new_board

board = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]

game = Game(board)

print(game.is_game_over())