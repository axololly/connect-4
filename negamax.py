from bitboard import Bitboard
from transposition_table import TranspositionTable
from functools import lru_cache

class Negamax:
    def __init__(self):
        self.trans_table = TranspositionTable()
        self.move_order = [3, 2, 4, 1, 5, 0, 6]
        self.nodes_explored = 0
    
    def heuristic(self, board: Bitboard):
        score = 0

        for row in range(6):
            for col in range(7):
                mask = 1 << (col + row * 7)
                    
                if board.bitboards[0] & mask:
                    score += 100 / ((5 * abs(3 - col)) + (10 * abs(2.5 - row)))
                else: # board.bitboards[1] & mask:
                    score -= 100 / ((5 * abs(3 - col)) + (10 * abs(2.5 - row)))

        return score # int(score)
    
    @lru_cache(maxsize = 512)
    def negamax(self, board: Bitboard, alpha: int, beta: int) -> int:
        self.nodes_explored += 1
        
        board = board.copy()

        if search_score := self.trans_table.get(board):
            return search_score

        if board.counter == 42:
            return 0
        
        if board.isWin():
            return (43 - board.counter) // 2
        
        beta = max(beta, (41 - board.counter) // 2)

        if beta <= alpha:
            return beta
        
        for x in board.getNextMoves():
            if board.is_winning_move(x):
                return (43 - board.counter) // 2
        
            board.makeMove(self.move_order[x])
            score = -self.negamax(board, -beta, -alpha)
            board.undoMove()
            
            alpha = max(alpha, score)

        self.trans_table.insert(board, alpha)
        
        return alpha

    def get_best_move(self, board: Bitboard) -> int:
        board = board.copy()
        best_score = -float('inf')
        best_move = 0

        for col in board.getNextMoves():
            board.makeMove(col)
            score = -self.solve(board)
            board.undoMove()

            print(score, col)

            if score > best_score:
                best_score = score
                best_move = col
        
        return best_move

    def solve(self, board: Bitboard, /, weak: bool = False) -> int:
        minimum = -(42 - board.counter) // 2
        maximum = (43 - board.counter) // 2

        if weak:
            minimum = -1
            maximum = 1
        
        while minimum < maximum:
            median = minimum + (maximum - minimum) // 2

            if median <= 0 and minimum // 2 < median:
                median = minimum // 2
            elif median >= 0 and maximum // 2 > median:
                median = maximum // 2
            
            score = -self.negamax(board, median, median + 1)

            if score <= median:
                maximum = score
            else:
                minimum = score
            
        return minimum