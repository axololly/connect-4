from bitboard import Bitboard
from heuristic import Heuristic

def negamax(board: Bitboard, depth: int, alpha: int, beta: int) -> int:
    board = board.copy()

    if depth == 0:
        return Heuristic().heuristic(board)

    if board.counter == 42:
        return 0
    
    if board.isWin():
        # print("winning board:")
        # print(repr(board))
        return (42 + 1 - board.counter) // 2 * (-1 if board.counter + 1 & 1 else 1)
    
    for x in board.getNextMoves():
        if board.is_winning_move(x):
            return (42 + 1 - board.counter) // 2 * (-1 if board.counter & 1 else 1)
    
    max_score = (42 - 1 - board.counter) // 2
    
    if beta > max_score:
        beta = max_score

        if alpha >= beta:
            return beta
    
    for x in board.getNextMoves():
        board.makeMove(x)
        score = -negamax(board, depth - 1, -beta, -alpha)
        board.undoMove()
        
        alpha = max(alpha, score)
    
    return alpha

def get_best_move(board: Bitboard, /, depth: int = 10) -> int:
    board = board.copy()
    best_score = -float('inf')
    best_move = 0

    all_scores = {}

    for col in board.getNextMoves():
        board.makeMove(col)
        score = -negamax(board, depth, float('-inf'), float('inf'))
        board.undoMove()

        all_scores[col] = score

        # print(score, col)

        if score > best_score:
            best_score = score
            best_move = col
    
    print("All scores: ", all_scores)
    return best_move