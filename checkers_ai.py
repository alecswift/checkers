from Board import init_state, init_borders, State, make_move

BoardState = tuple[tuple[complex, int]]

def find_ai_move(board):
    curr_state = init_state()
    borders = init_borders()
    best_move = minimax(curr_state, 5, True, borders)[1]
    return best_move

def minimax(state, depth: int, max_player: bool, borders) -> Path:
    state_obj = State(state, borders)
    state_obj.valid_moves(state)
    game_won = not state_obj.paths
    if depth == 0 or game_won:
        return evaluate(state), None  # return move as well?

    best_move = None
    if max_player:
        max_eval = float("-inf")
        for move in state_obj.paths:
            next_state = make_move(move, state)
            curr_eval = minimax(next_state, depth - 1, False, borders)[0]
            max_eval = max(max_eval, curr_eval)
            if max_eval == curr_eval:
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float("inf")
        for move in state_obj.paths:
            next_state = make_move(move, state)
            curr_eval = minimax(next_state, depth - 1, True, borders)[0]
            min_eval = min(min_eval, curr_eval)
            if min_eval == curr_eval:
                best_move = move
        return min_eval, best_move


def evaluate(state) -> int:
    count_white = 0
    count_black = 0
    count_white_kings = 0
    count_black_kings = 0
    for _, piece in state:
        if piece != 0 and piece % 2 == 0:
            count_white += 1
        if piece != 0 and piece % 2 == 1:
            count_black += 1
        if piece == 3:
            count_black_kings += 1
        if piece == 4:
            count_white_kings += 1
    return (count_white - count_black) + (.5 * count_white_kings - .5 * count_black_kings)
