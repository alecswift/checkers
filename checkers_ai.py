from board import Piece, BoardDict

State = tuple[tuple[complex, int]]

def init_state(board: BoardDict) -> State:
    state = []
    for val in board.values():
        if isinstance(val, Piece):
            if val.color == "black":
                color = 1
            else:
                color = 0
            if val.rank == "king":
                color += 1
            state.append((val.pos, color))
    return tuple(state)



