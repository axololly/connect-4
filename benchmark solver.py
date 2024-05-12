import sqlite3, os
from glob import glob
from time import time, sleep
from bitboard import Bitboard
from negamax import negamax

conn = sqlite3.connect('results.sql')

conn.execute("""
CREATE TABLE "results" IF NOT EXISTS (
	"id"	INTEGER,
	"moves"	TEXT,
	"given_eval"	INTEGER,
	"curr_eval"	INTEGER,
	"difference"	INTEGER,
	"time_taken"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)""")

conn.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'results'")
conn.commit()

conn.execute("DELETE FROM results")
conn.commit()

files = glob('./test cases/*')

bb = Bitboard()

operations = 0

for file in files:
    with open(file) as f:
        lines = f.read().splitlines()
        
        for i, line in enumerate(lines):
            bb.clear()

            moves, score = line.split(' ')
            score = int(score)

            for column in moves:
                bb.makeMove(int(column) - 1)
            
            try:
                t0 = time()
                best = negamax(bb, 10, float('-inf'), float('inf'))
                time_taken = time() - t0

                os.system('cls')
                operations += 1

                print(f"Completed {operations}/6000 operations so far!")
                print(f"Time to complete the {operations}{'th' if operations % 10 != 1 else 'st' if operations % 10 != 2 else 'nd'} operation: {time_taken:.2f}s")
                print("Progress Bar:")
                print("❚" * int(operations * 182 / 6000))

            except Exception as e:
                os.system('cls')
                print(repr(bb))
                print()
                print()
                print("Error.\nMoves:", moves)
                print()
                raise e

            # print(f"Given eval: {score}\nTime taken: {time_taken:.2f}s\nMy eval: {best}\nDifference: {best - score}\n")

            conn.execute("""INSERT INTO results (
                                moves,
                                given_eval,
                                curr_eval,
                                difference,
                                time_taken
                         ) VALUES (?, ?, ?, ?, ?)""", (
                                                        moves,
                                                        score,
                                                        best,
                                                        best - score,
                                                        f"{time_taken:.2f}s"
                                                      )
                        )
            conn.commit()

