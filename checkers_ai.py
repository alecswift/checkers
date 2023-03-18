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
            state.append((pos, 0))
    return tuple(state)


def init_borders():
    """Return a set of border coordinates for a checkers board"""
    borders = set()
    borders_nums = [-1, 8]
    for num1 in borders_nums:
        for num2 in range(0, 7):
            borders.add(complex(num1, num2))
            borders.add(complex(num2, num1))
    return borders


def minimax(state, depth: int, max_player: bool, borders) -> Path:
    state_obj = State(state, borders)
    state_obj.valid_moves(state)
    game_won = not state_obj.paths
    if depth == 0 or game_won:
        return evaluate(state)  # return move as well?

    if max_player:
        max_eval = float(-"inf")
        for move in state_obj.paths:
            next_state = make_move(state)
            curr_eval = minimax(next_state, depth - 1, False)
            max_eval = max(max_eval, curr_eval)
        return max_eval
    else:
        min_eval = float("inf")
        for move in state_obj.paths:
            next_state = make_move(move, state)
            curr_eval = minimax(next_state, depth - 1, True)
            min_eval = min(max_eval, curr_eval)
        return min_eval


class State:
    def __init__(self, board_state, borders):
        self._board_state = board_state
        self._borders = borders
        self._paths = set()

    @property
    def paths(self):
        return self._paths

    def valid_moves(self, max_player) -> list[Path]:
        color = 0 if max_player else 1
        for pos, piece in self._board_state:
            if piece % 2 == color:
                path = (
                    piece,
                    pos,
                )
                capture = False
                self.next_move(path, capture)
        self.prune_paths()

    def next_move(self, path: Path, capture: bool) -> None:
        if not capture:
            prev_pos = None
            piece, curr_pos = path
        else:
            piece, *_, prev_pos, curr_pos = path
        forward_left = Direction.FORWARD_LEFT.move(curr_pos, piece % 2, 1)
        forward_right = Direction.FORWARD_RIGHT.move(curr_pos, piece % 2, 1)
        next_positions = [forward_left, forward_right]
        if piece <= 2:
            for next_position in next_positions:
                next_path = *path, next_position
                self.build_path(next_path, capture)
        else:
            back_left = Direction.BACK_LEFT.move(curr_pos, piece % 2, 1)
            back_right = Direction.BACK_RIGHT.move(curr_pos, piece % 2, 1)
            next_positions.extend([back_left, back_right])
            for next_position in next_positions:
                if prev_pos == next_position:
                    continue
                next_path = *path, next_position
                self.build_path(next_path, capture)

    def build_path(self, path: Path, capture: bool) -> None:
        # Check if I really need the piece in the path
        piece, *rest, curr_pos, next_pos = path
        next_val = self.search_state(next_pos)

        opp_color = 1 if piece % 2 == 0 else 0
        if not capture and next_val == 0:
            self._paths.add(path)
        elif capture and not next_val:
            self._paths.add((piece, *rest, curr_pos))
        elif capture and next_val and next_val % 2 != opp_color:
            self._paths.add((piece, *rest, curr_pos))
        elif next_val and next_val % 2 == opp_color:
            move = next_pos - curr_pos
            jump = next_pos + move
            jump_val = self.search_state(jump)
            if jump_val == 0:
                self.next_move((*path, jump), True)
            elif capture:
                self._paths.add((piece, *rest, curr_pos))

    def search_state(self, next_pos):
        for pos, val in self._board_state:
            if pos == next_pos:
                next_val = val
                break
        else:
            next_val = None
        return next_val

    def prune_paths(self) -> list[Path]:
        """
        Removes all invalid paths from the given paths list. A path is invalid if
        there is another path in the list with more captures
        """
        if self._paths:
            max_length = max(len(path) for path in self._paths)
            self._paths = set(path for path in self._paths if len(path) == max_length)


def make_move(move: Path, state):
    if len(move) == 3:
        piece, start_pos, end_pos = move
        remove = set([start_pos, end_pos])
        removed = tuple((pos, val) for pos, val in state if pos not in remove)
        if piece <= 2:
            piece = handle_promotion(end_pos.imag, piece)
        new_state = *removed, (end_pos, piece), (start_pos, 0)
    else:
        piece, *path = move
        opp_pos = set([pos for idx, pos in enumerate(path) if idx % 2 == 1])
        start_pos, *_, end_pos = path
        removed_opp = tuple(
            (pos, 0) if pos in opp_pos else (pos, val) for pos, val in state
        )
        remove = set([start_pos, end_pos])
        removed = tuple((pos, val) for pos, val in state if pos not in remove)
        if piece <= 2:
            piece = handle_promotion(end_pos.imag, piece)
        new_state = *removed_opp, (end_pos, piece), (start_pos, 0)
    return new_state


def handle_promotion(row, piece):
    promotion_row = 7 if piece == 2 else 0
    if promotion_row == row:
        return piece + 2
    return piece


def evaluate(state) -> int:
    count_white = 0
    count_black = 0
    for _, piece in state:
        if piece != 0 and piece % 2 == 0:
            count_white += 1
        if piece != 0 and piece % 2 == 1:
            count_black += 1
    return count_white - count_black


def state_print(state) -> str:
    """Returns the string version of the checker board for debugging"""
    board_array = [[None] * 8 for _ in range(8)]
    for pos, piece in state:
        if piece:
            x_coord, y_coord = int(pos.real), int(pos.imag)
            val = "black" if piece == 1 else "white"
            board_array[y_coord][x_coord] = val

    board_str = []
    for num in range(8):
        board_str.append(f"  {num}")
    board_str.append("\n")
    for idx, row in enumerate(board_array):
        board_str.append(f"{idx} ")
        for val in row:
            if val is None:
                board_str.append("|  ")
            elif "white" in val:
                board_str.append("| w")
            else:
                board_str.append("| b")
        board_str.append("|\n")
    return "".join(board_str)
