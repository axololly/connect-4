from bitboard import Bitboard
from functools import lru_cache

class AnotherNegamax:
    nodes_explored = 0
    move_order = [3, 2, 4, 1, 5, 0, 6]
    
    @lru_cache(maxsize = 512)
    def negamax(self, board: Bitboard, alpha: int, beta: int) -> int:
        i = self.nodes_explored % 10
        print(f"alpha: {alpha}  |  beta: {beta}\nboard:\n{board}\nthis is the {self.nodes_explored}{'rd' if i == 3 else 'nd' if i == 2 else 'st' if i == 1 else 'th'} node searched\n")
        
        self.nodes_explored += 1

        if board.counter == 42:
            return 0
        
        if board.isWin():
            return (42 - board.counter) // 2
        
        max_score = (41 - board.counter) // 2

        beta = max(beta, max_score)

        if alpha >= beta:
            return beta
        
        for x in board.getNextMoves():
            if board.is_winning_move(self.move_order[x]):
                return (43 - board.counter) // 2
            
            board.makeMove(self.move_order[x])            
            score = -self.negamax(board, -beta, -alpha)
            board.undoMove()

            if score >= beta:
                return score
            
            alpha = max(alpha, score)
        
        return alpha

    def get_best_move(self, board: Bitboard) -> int:
        board = board.copy()
        all_scores = {}

        for col in board.getNextMoves():
            board.makeMove(col)
            score = -self.negamax(board, float('-inf'), float('inf'))
            board.undoMove()

            all_scores[col + 1] = score
        
        return all_scores