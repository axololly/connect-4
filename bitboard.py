from typing import List, NewType, Self
from copy import deepcopy

Binary = NewType('Binary', int)

class Bitboard:
    STARTING_POSITION = [[0 for _ in range(7)] for _ in range(6)]

    def __init__(self, *bitboards: Binary):
        self.bitboards: List[Binary] = list(bitboards)

        if not self.bitboards:
            self.bitboards = [0, 0]
        
        if len(self.bitboards) < 2:
            self.bitboards.append(0)
        
        if len(self.bitboards) > 2:
            raise Exception("More than two bitboards were parsed as arguments.")
        
        self.heights = [n * 7 for n in range(7)]
        self.counter = 0
        self.moves = []
    
    def __repr__(self) -> str:
        state = []

        for i in range(6):
            row_str = ''

            for j in range(7):
                pos = 1 << 7 * j + i
            
                if self.bitboards[0] & pos == pos:
                    row_str += '1 '
                elif self.bitboards[1] & pos == pos:
                    row_str += '2 '
                else:
                    row_str += '. '
            
            state.append(row_str)
        
        state.reverse()
        
        return '\n'.join(state)
    
    def makeMove(self, column: int) -> None:
        self.bitboards[self.counter % 2] ^= 1 << self.heights[column]
        self.heights[column] += 1
        self.moves.append(column)
        self.counter += 1

    def undoMove(self) -> None:
        col = self.moves.pop()
        self.bitboards[self.counter % 2] ^= 1 << self.heights[col]
        self.counter -= 1
        self.heights[col] -= 1

    def isWin(self) -> bool:
        bitboard = self.bitboards[(self.counter - 1) % 2]

        directions = [1, 7, 6, 8]
        bb = None

        for direction in directions:
            bb = bitboard & (bitboard >> direction)

            if bb & (bb >> (2 * direction)) != 0:
                return True
        
        return False

    def getNextMoves(self) -> List[int]:
        moves: List[int] = []
        TOP = 0b1000000_1000000_1000000_1000000_1000000_1000000_1000000

        for i in range(7):
            if TOP & (1 << self.heights[i]) == 0:
                moves.append(i)
        
        return moves

    def is_winning_move(self, move: int) -> bool:
        separate_board = self.copy()
        separate_board.makeMove(move)
        is_winning = separate_board.isWin()
        separate_board.undoMove()
        
        return is_winning

    def copy(self) -> Self:
        return deepcopy(self)
    
    def clear(self) -> None:
        self.bitboards = [0, 0]
        self.counter = 0
        self.moves = []
        self.heights = [n * 7 for n in range(7)]
    
    def generate_key(self) -> Binary: # used for later in transposition table
        return self.bitboards[0] ^ self.bitboards[1] ^ 0b1000000100000010000001000000100000010000001000000