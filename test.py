from bitboard import Bitboard
from negamax import Negamax
from another_negamax import AnotherNegamax
from time import time

BN = AnotherNegamax()
NN = Negamax()

def setup():
    bb = Bitboard()
    cases = ['445566', '6146', '3153', '17516442226766']
    moves = cases[1]

    for move in moves:
        bb.makeMove(int(move) - 1)
    
    print('starting board:')
    print(bb)
    print()
    print("player", (bb.counter & 1) + 1, "to play")
    print()
    print()

    return bb

def test_it():
    bb = setup()
    
    t0 = time()

    print("best move:", NN.get_best_move(bb)) #, alpha = float('-inf'), beta = float('inf')))
    print(f"time taken: {time() - t0:.4f}s")
    print()
    print("nodes explored:", NN.nodes_explored)

def run_checks(NN: Negamax):
    print()
    print("-" * 50)
    print()

    for i, board in enumerate(NN.archive):
        board: Bitboard
        print(f"evaluating node #{i + 1}")
        print(f"valid move count? {'yes' if len(board.moves) < 42 else 'no'}")
        checks = [board.heights[x] < (n + 1) * 7 - 1 for x, n in enumerate(range(7))]
        print(f"valid heights? {'yes' if all(checks) else 'no'}  |  {checks}")
        print()

def play_game():
    bb = Bitboard()

    while not bb.isWin():
        move = int(input('Enter column: ')) - 1
        bb.makeMove(move)
        print(bb)
        print()
        
        if bb.isWin():
            print(f'Player {bb.counter % 2 + 1} wins!')
            break

        move = Negamax().get_best_move(bb)
        bb.makeMove(move)
        print(bb)
        print()
        print(f'Player {bb.counter % 2 + 1} played in column {move}')
        print()
        
        if bb.isWin():
            print(f'Player {bb.counter % 2 + 1} wins!')
            break

def redirect_output(func: callable):
    from contextlib import redirect_stdout

    with open('results.txt', 'w') as f:
        with redirect_stdout(f):
            func()

def column_test():
    bb = Bitboard()

    for move in range(7):
        print(f"placing a counter in column #{move + 1}")
        bb.makeMove(move)
        print(bb)
        print(f"bitboards: {bb.bitboards}")
        print(f"heights: {bb.heights}")
        print(f"counter: {bb.counter}")
        print(f"moves: {bb.moves}")
        print()

        bb.undoMove()
        print(f"removing a counter on column #{move + 1}")
        print(bb)
        print(f"bitboards: {bb.bitboards}")
        print(f"heights: {bb.heights}")
        print(f"counter: {bb.counter}")
        print(f"moves: {bb.moves}")

        print()
        print()

def something():
    bb = Bitboard(*[356532226, 44072961])
    heights = [2, 7, 16, 27, 29, 35, 42]
    bb.counter = len(heights)
    bb.heights = heights
    bb.moves = [2, 0, 4, 2, 0, 3, 3, 3, 3, 3, 3]
    print(bb.getNextMoves()) # should be [0, 1, 2, 4, 5, 6]

redirect_output(test_it)
# something()