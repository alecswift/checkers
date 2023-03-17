from board import Piece, BoardDict
from player import Path, Direction

BoardState = tuple[tuple[complex, int]]

def init_state(board: BoardDict) -> BoardState:
    state = []
    for pos, val in board.items():
        if isinstance(val, Piece):
            if val.color == "black":
                color = 1
            else:
                color = 2
            if val.rank == "king":
                color += 2
            state.append((val.pos, color))
        elif val == "empty":
            state.append((pos, -0))
    return tuple(state)

def init_borders():
    """Return a set of border coordinates for a checkers board"""
    borders = set()
    borders_nums = [-1, 8]
    for num1 in borders_nums:
        for num2 in range(0,7):
            borders.add(complex(num1, num2))
            borders.add(complex(num2, num1))
    return borders

def minimax(state, depth: int, max_player: bool) -> Path:
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
    
class State:

    def __init__(self, board_state, borders):
        self._board_state = board_state
        self._borders = borders
        self._paths = []

    @property
    def paths(self):
        return self._paths

    def valid_moves(self, max_player) -> list[Path]:
        color = 0 if max_player else 1
        for pos, piece in self._board_state:
            if piece % 2 == color:
                path = (pos, )
                capture = False
                self.next_move(path, piece, capture)
        self.prune_paths()

    def next_move(self, path: Path, piece: int, capture: bool) -> None:
        if not capture:
            prev_pos = None
            *_, curr_pos = path
        else:
            *_, prev_pos, curr_pos = path
        forward_left = Direction.FORWARD_LEFT.move(curr_pos, piece % 2, 1)
        forward_right = Direction.FORWARD_RIGHT.move(curr_pos, piece % 2, 1)
        next_positions = [forward_left, forward_right]
        if piece <= 2:
            for next_position in next_positions:
                next_path = *path, next_position
                self.build_path(next_path, piece, capture)
        else:
            back_left = Direction.BACK_LEFT.move(curr_pos, piece % 2, 1)
            back_right = Direction.BACK_RIGHT.move(curr_pos, piece % 2, 1)
            next_positions.extend([back_left, back_right])
            for next_position in next_positions:
                if prev_pos == next_position:
                    continue
                next_path = *path, next_position
                self.build_path(next_path, piece % 2, capture)

    def build_path(self, path: Path, piece: int, capture: bool) -> None:
        *rest, curr_pos, next_pos = path
        for pos, val in self._board_state:
            if pos == next_pos:
                next_val = val
                break
        else:
            next_val = None

        opp_color = 1 if piece % 2 == 0 else 0
        if not capture and next_val == 0:
            self._paths.append(path)
        elif capture and not next_val:
            self._paths.append((*rest, curr_pos))
        elif capture and next_val and next_val % 2 != opp_color:
            self._paths.append((*rest, curr_pos))
        elif next_val and next_val % 2 == opp_color:
            move = next_pos - curr_pos
            jump = next_pos + move
            if self.board.get(jump) == "empty":
                self.next_move((*path, jump), piece, True)
            elif capture:
                self._paths.append((*rest, curr_pos))

    def prune_paths(self) -> list[Path]:
        """
        Removes all invalid paths from the given paths list. A path is invalid if
        there is another path in the list with more captures
        """
        if self._paths:
            max_length = max(len(path) for path in self._paths)
            return [path for path in self._paths if len(path) == max_length]
        return self._paths

def make_move(move: Path, state: State):
    pass

def game_won(state: State) -> bool:
    pass

def evaluate(state: State) -> int:
    pass
