from bitboard import Bitboard

moves = '7675456251'

bb = Bitboard()

for move in moves:
    bb.makeMove(int(move) - 1)

x, y = bb.bitboards
n = 0b1000000100000010000001000000100000010000001000000

bbkey = Bitboard(x ^ y ^ n)
key = bbkey.bitboards[0]
print(repr(key))
print(repr(Bitboard(key ^ n)))