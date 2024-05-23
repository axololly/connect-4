from typing import List, NewType

Binary = NewType('Binary', int)

class Bitboard:
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
    
        self.bottom_mask = 0b1000000_1000000_1000000_1000000_1000000_10000001
    
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
    
    def __eq__(self, value: object) -> bool:
        assert type(value) is Bitboard
        return self.bitboards == value.bitboards
    
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
        self.makeMove(move)
        is_winning = self.isWin()
        self.undoMove()
        
        return is_winning

    def copy(self):
        new_board = Bitboard(*self.bitboards)
        
        new_board.counter = self.counter
        new_board.heights = self.heights
        new_board.moves = self.moves

        return new_board
    
    def clear(self) -> None:
        self.bitboards = [0, 0]
        self.counter = 0
        self.moves = []
        self.heights = [n * 7 for n in range(7)]
    
    def generate_key(self) -> Binary: # used for later in transposition table
        return self.bitboards[0] ^ self.bitboards[1] ^ self.bottom_mask
    
# Used for later
class Position(Bitboard):
    def __init__(self, *args):
        super().__init__(*args)
        self.board_mask = self.bottom_mask * ((1 << 6) - 1)
    
    def compute_winning_position(self, position: Binary, mask: Binary):
        # vertical
        r = (position << 1) & (position << 2) & (position << 3)

        # horizontal
        p = (position << 7) & (position << 14)
        r |= p & (position << 21)
        r |= p & (position >> 7)
        p >>= 21
        r |= p & (position << 7)
        r |= p & (position >> 21)

        # diagonal 1
        p = (position << 6) & (position << 12)
        r |= p & (position << 18)
        r |= p & (position >> 6)
        p >>= 18
        r |= p & (position << 6)
        r |= p & (position >> 18)

        # diagonal 2
        p = (position << 8) & (position << 16)
        r |= p & (position << 24)
        r |= p & (position >> 8)
        p >>= 24
        r |= p & (position << 8)
        r |= p & (position >> 24)

        return r & (self.board_mask ^ mask)
    
    def winning_position(self):
        return self.compute_winning_position(
            self.bitboards[self.counter & 1],     # current position
            self.bitboards[0] ^ self.bitboards[1] # mask (both postions overlapped)
        )

    def possible(self):
        return (self.bitboards[0] ^ self.bitboards[1] + self.bottom_mask) & self.board_mask

    def can_win_next(self):
        return self.winning_position() & self.possible()

    def possible_non_losing_moves(self):
        assert not self.can_win_next()
