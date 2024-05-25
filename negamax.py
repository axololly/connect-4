from bitboard import Bitboard
from transposition_table import TranspositionTable
from functools import lru_cache

class Negamax:
    def __init__(self):
        self.trans_table = TranspositionTable()
        self.move_order = [3, 2, 4, 1, 5, 0, 6]
        
        self.nodes_explored = 0
        # self.archive = []
    
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
        '''
        self.archive.append(board)
        
        i = self.nodes_explored % 10
        print(f"alpha: {alpha}  |  beta: {beta}")
        print(f"board:")
        print(board)
        print(f"bitboards: {board.bitboards}")
        print(f"moves: {board.moves}")
        print(f"this is the {self.nodes_explored}{'rd' if i == 3 else 'nd' if i == 2 else 'st' if i == 1 else 'th'} node searched")
        print(f"the heights are: {board.heights}")
        print()
        '''
        
        board = board.copy()
        move_length = len(board.moves)

        if move_length == 42:
            return 0

        if search_scores := self.trans_table.get(board):
            alpha, beta = search_scores['UB'], search_scores['LB']
        else:
            beta = max(beta, (41 - move_length) // 2)

        if beta <= alpha:
            return beta
        
        next_moves = board.getNextMoves()
        
        for x in range(7):
            if self.move_order[x] not in next_moves:
                continue

            if board.is_winning_move(self.move_order[x]):
                print(board)
                print(f"winning move found: {self.move_order[x]}")
                print(f"alpha: {alpha}  |  beta: {beta}")
                print(f"given score: {(43 - move_length) // 2}")
                print()

                return (43 - move_length) // 2

            board.makeMove(self.move_order[x])
            score = -self.negamax(board, -beta, -alpha)
            board.undoMove()
            
            alpha = max(alpha, score)

        self.trans_table.insert(board, alpha, beta)
        
        return alpha

    def get_best_move(self, board: Bitboard) -> int:
        # board = board.copy()
        best_score = -float('inf')
        best_move = None

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
        minimum = (-42 + len(board.moves)) // 2
        maximum = (43 - len(board.moves)) // 2

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