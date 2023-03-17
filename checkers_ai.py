from board import Piece, BoardDict
from player import Path, Direction

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

def minimax(state: State, depth: int, max_player: bool) -> Path:
    if depth == 0 or game_won(state):
        return evaluate(state) # return move as well?
    
    if max_player:
        max_eval = float(-'inf')
        for move in valid_moves(state):
            state = make_move(state)
            curr_eval = minimax(state, depth - 1, False)
            max_eval = max(max_eval, curr_eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in valid_moves(state):
            state = make_move(move, state)
            curr_eval = minimax(state, depth - 1, True)
            min_eval = min(max_eval, curr_eval)
        return min_eval

def valid_moves(state: State, max_player) -> list[Path]:
    color = 0 if max_player else 1
    paths: list[Path] = []
    for pos, piece in state:
        if piece % 2 == color:
            path = (pos, )
            capture = False
            next_move(path, paths, piece, capture)
    return paths

def next_move(path: Path, paths: list[Path], piece: int, capture: bool) -> None;
    pass

def make_move(move: Path, state: State):
    pass

def game_won(state: State) -> bool:
    pass

def evaluate(state: State) -> int:
    pass
