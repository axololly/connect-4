import sqlite3
from os import system
from negamax import Negamax
from bitboard import Bitboard
from time import time
from glob import glob

conn = sqlite3.connect('new results.sql')

conn.execute("""
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY,
    moves TEXT,
    given_eval INTEGER,
    curr_eval INTEGER,
    difference INTEGER ALWAYS AS (given_eval - curr_eval),
    time_taken REAL,
    nodes_explored INTEGER
)
""")
conn.execute("DELETE FROM results")
conn.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'results'")

bb = Bitboard()

files = glob('./test cases/*')

for file in files:
    with open(file) as f:
        content = f.read()
        lines = content.splitlines()
        
        for i, line in enumerate(lines):
            bb.clear()
            moves, score = line.split(' ')
            
            for move in moves:
                bb.makeMove(int(move) - 1)
            
            try:
                t0 = time()
                N = Negamax()
                evaluation = N.solve(bb)
                time_taken = float(f"{time() - t0:.4f}")
                
                conn.execute(
                    "INSERT INTO results (moves, curr_eval, given_eval, time_taken, nodes_explored) VALUES (?, ?, ?, ?, ?)",
                    (moves, evaluation, int(score), time_taken, N.nodes_explored)
                )
                conn.commit()
            
            except Exception as e:
                system('cls')
                print(repr(bb))
                print()
                print()
                print("Error.\nMoves:", moves)
                print()
                raise e

            system('cls')
            print(f"Completed test case #{i + 1}.\nFinished evaluating {moves}.\nScore by algorithm: {evaluation}.\nTime taken: {time_taken:.4f}s.\nProgress bar:")
            print('❚' * int(i / 60))

print()
print("Done with everything!")