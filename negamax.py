from bitboard import Bitboard
from heuristic import Heuristic
from transposition_table import TranspositionTable

class Negamax:
    def __init__(self):
        self.trans_table = TranspositionTable()
        self.move_order = [3, 2, 4, 1, 5, 0, 6]
        self.nodes_explored = 0

    def negamax(self, board: Bitboard, depth: int, alpha: int, beta: int) -> int:
        board = board.copy()
        self.nodes_explored += 1

        if search_score := self.trans_table.get(board):
            return search_score

        if depth == 0:
            return Heuristic().heuristic(board)

        if board.counter == 42:
            return 0
        
        if board.isWin():
            return (42 + 1 - board.counter) // 2
        
        for x in board.getNextMoves():
            if board.is_winning_move(x):
                return (42 + 1 - board.counter) // 2
        
        max_score = (42 - 1 - board.counter) // 2
        
        beta = max(beta, max_score)

        if beta <= alpha:
            return beta
        
        for x in board.getNextMoves():
            board.makeMove(self.move_order[x])
            score = -self.negamax(board, depth - 1, -beta, -alpha)
            board.undoMove()
            
            alpha = max(alpha, score)

        self.trans_table.insert(board, alpha)
        
        return alpha

    def get_best_move(self, board: Bitboard, /, depth: int = 10) -> int:
        board = board.copy()
        best_score = -float('inf')
        best_move = 0

        for col in board.getNextMoves():
            board.makeMove(col)
            # score = -self.negamax(board, depth, float('-inf'), float('inf'))
            score = -self.solve(board, depth)
            board.undoMove()

            print(score, col)

            if score > best_score:
                best_score = score
                best_move = col
        
        return best_move

    def solve(self, board: Bitboard, /, depth: int = 10, weak: bool = False) -> int:
        minimum = -(42 - board.counter) // 2
        maximum = (43 - board.counter) // 2

        if weak:
            minimum = -1
            maximum = 1
        
        while minimum < maximum:
            median = minimum + (maximum - minimum) // 2

            if median <= 0 and minimum / 2 < median:
                median = minimum / 2
            elif median >= 0 and maximum / 2 > median:
                median = maximum / 2
            
            score = -self.negamax(board, depth, median, median + 1)

            if score <= median:
                maximum = score
            else:
                minimum = score
            
        return minimum