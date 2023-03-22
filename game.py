from board import Piece

def make_move(move, state):
    #Change to take one jump at a time except for in the minimax algo
    piece, positions, jumps = move
    start_pos, *_, end_pos = positions
    remove = set([start_pos, end_pos])
    removed = tuple((pos, val) for pos, val in state if pos not in remove)
    removed_opp = tuple(
            (pos, Piece.EMPTY) if pos in jumps else (pos, val) for pos, val in removed
        )
    if Piece.KING not in piece:
        piece = handle_promotion(end_pos.imag, piece)
    new_state = *removed_opp, (end_pos, piece), (start_pos, Piece.EMPTY)
    return new_state


def handle_promotion(row, piece):
    promotion_row = 7 if piece == Piece.WHITE else 0
    if promotion_row == row:
        return Piece.BLACK_KING if piece == Piece.BLACK else Piece.WHITE_KING
    return piece

def game_won(state):
    """Return if the checkers game has been won from the given board state"""
