from bitboard import Bitboard

class Heuristic:
    def heuristic(self, board: Bitboard):
        if board.isWin():
            return (1 if board.counter % 2 == 0 else -1) * 1_000_000
        
        if len(board.moves) == 42:
            return 0
        
        score = 0

        current_player = board.counter % 2

        if current_player == 0:
            for row in range(6):
                for col in range(7):
                    mask = 1 << (col + row * 7)
                    
                    if board.bitboards[0] & mask:
                        score += 100 / ((5 * abs(3 - col)) + (10 * abs(2.5 - row)))
                    elif board.bitboards[1] & mask:
                        score -= 100 / ((5 * abs(3 - col)) + (10 * abs(2.5 - row)))
        else:
            for row in range(6):
                for col in range(7):
                    mask = 1 << (col + row * 7)

                    if board.bitboards[0] & mask:
                        score -= 100 / ((5 * abs(3 - col)) + (10 * abs(2.5 - row)))
                    elif board.bitboards[1] & mask:
                        score += 100 / ((5 * abs(3 - col)) + (10 * abs(2.5 - row)))

        return score # int(score)