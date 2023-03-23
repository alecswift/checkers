import unittest
import game
import game


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.initial_state = game.init_state()
        self.borders = game.init_borders()
        self.b_piece = game.Piece.BLACK
        self.w_piece = game.Piece.WHITE
        self.b_king = game.Piece.BLACK_KING
        self.empty = game.Piece.EMPTY
        self.move = game.make_move

    def tearDown(self):
        del self.initial_state
        del self.borders
        del self.b_piece
        del self.w_piece
        del self.b_king
        del self.empty
        del self.move

    def test_init_state_method_with_initial_board(self):
        actual_output = set(self.initial_state)
        expected = {
            (1 + 0j, self.w_piece,),
            (3 + 0j, self.w_piece,),
            (5 + 0j, self.w_piece,),
            (7 + 0j, self.w_piece,),
            (0 + 1j, self.w_piece,),
            (2 + 1j, self.w_piece,),
            (4 + 1j, self.w_piece,),
            (6 + 1j, self.w_piece,),
            (1 + 2j, self.w_piece,),
            (3 + 2j, self.w_piece,),
            (5 + 2j, self.w_piece,),
            (7 + 2j, self.w_piece,),
            (0 + 5j, self.b_piece,),
            (2 + 5j, self.b_piece,),
            (4 + 5j, self.b_piece,),
            (6 + 5j, self.b_piece,),
            (1 + 6j, self.b_piece,),
            (3 + 6j, self.b_piece,),
            (5 + 6j, self.b_piece,),
            (7 + 6j, self.b_piece,),
            (0 + 7j, self.b_piece,),
            (2 + 7j, self.b_piece,),
            (4 + 7j, self.b_piece,),
            (6 + 7j, self.b_piece,),
            (0 + 3j, self.empty,),
            (2 + 3j, self.empty,),
            (4 + 3j, self.empty,),
            (6 + 3j, self.empty,),
            (1 + 4j, self.empty,),
            (3 + 4j, self.empty,),
            (5 + 4j, self.empty,),
            (7 + 4j, self.empty,),
        }
        self.assertEqual(actual_output, expected)

    def test_valid_move_method_with_initial_board_state(self):
        board_obj = game.Board(self.initial_state, self.borders)
        expected = {
                (self.b_piece, (5j, 1 + 4j), ()),
                (self.b_piece, (2 + 5j, 1 + 4j), ()),
                (self.b_piece, (2 + 5j, 3 + 4j), ()),
                (self.b_piece, (4 + 5j, 3 + 4j), ()),
                (self.b_piece, (4 + 5j, 5 + 4j), ()),
                (self.b_piece, (6 + 5j, 5 + 4j), ()),
                (self.b_piece, (6 + 5j, 7 + 4j), ()),
        }
        actual_output = board_obj.find_valid_moves(self.b_piece)
        self.assertEqual(expected, actual_output)

    def test_valid_move_method_with_one_valid_capture(self):
        state = self.move((self.b_piece, (5j, 1 + 4j), ()), self.initial_state)
        state = self.move((self.w_piece, (3 + 2j, 2 + 3j), ()), state)
        expected = {(self.b_piece, (1 + 4j, 3 + 2j), (2 + 3j,))}
        self.valid_paths_helper(state, expected, self.b_piece)

    def test_valid_move_method_with_one_valid_capture_2(self):
        state = self.move((self.b_piece, (2 + 5j, 3 + 4j), ()), self.initial_state)
        state = self.move((self.w_piece, (3 + 2j, 4 + 3j), ()), state)
        state = self.move((self.b_piece, (1 + 6j, 2 + 5j), ()), state)
        state = self.move((self.w_piece, (5 + 2j, 6 + 3j), ()), state)
        state = self.move((self.b_piece, (3 + 4j, 5 + 2j), (4 + 3j,)), state)
        expected = {(self.w_piece, (6 + 1j, 4 + 3j), (5 + 2j,))}
        self.valid_paths_helper(state, expected, self.w_piece)
    
    def test_valid_move_method_with_2_valid_captures(self):
        state = self.move((self.b_piece, (4 + 5j, 5 + 4j), ()), self.initial_state)
        state = self.move((self.w_piece, (5 + 2j, 6 + 3j), ()), state)
        state = self.move((self.b_piece, (5 + 6j, 4 + 5j), ()), state)
        state = self.move((self.w_piece, (3 + 2j, 4 + 3j), ()), state)
        state = self.move((self.b_piece, (5 + 4j, 3 + 2j), (4 + 3j,)), state)
        expected = {
                (self.w_piece, (2 + 1j, 4 + 3j), (3 + 2j,)),
                (self.w_piece, (4 + 1j, 2 + 3j), (3 + 2j,)),
        }
        self.valid_paths_helper(state, expected, self.w_piece)

    def test_valid_paths_method_with_double_capture(self):
        state = self.move((self.b_piece, (5j, 1 + 4j), ()), self.initial_state)
        state = self.move((self.w_piece, (5 + 2j, 4 + 3j), ()), state)
        state = self.move((self.b_piece, (6 + 5j, 7 + 4j), ()), state)
        state = self.move((self.w_piece, (6 + 1j, 5 + 2j), ()), state)
        state = self.move((self.b_piece, (1 + 6j, 5j), ()), state)
        state = self.move((self.w_piece, (4 + 3j, 3 + 4j), ()), state)
        expected = {(self.b_piece, (2 + 5j, 4 + 3j, 6 + 1j), (3 + 4j, 5 + 2j))}
        self.valid_paths_helper(state, expected, self.b_piece)

    def test_valid_paths_method_with_double_capture_2(self):
        state = self.move((self.b_piece, (5j, 1 + 4j), ()), self.initial_state)
        state = self.move((self.w_piece, (5 + 2j, 4 + 3j), ()), state)
        state = self.move((self.b_piece, (6 + 5j, 7 + 4j), ()), state)
        state = self.move((self.w_piece, (6 + 1j, 5 + 2j), ()), state)
        state = self.move((self.b_piece, (1 + 6j, 5j), ()), state)
        state = self.move((self.w_piece, (5 + 0j, 6 + 1j), ()), state)
        state = self.move((self.b_piece, (7j, 1 + 6j), ()), state)
        state = self.move((self.w_piece, (3 + 2j, 2 + 3j), ()), state)
        expected = {(self.b_piece, (1 + 4j, 3 + 2j, 5 + 0j), (2 + 3j,  4 + 1j))}
        self.valid_paths_helper(state, expected, self.b_piece)

    def test_valid_paths_with_king_double_capture(self):
        state = self.move((self.b_piece, (6 + 5j, 7 + 4j), ()), self.initial_state)
        state = self.move((self.w_piece, (1 + 2j, 2 + 3j), ()), state)
        state = self.move((self.b_piece, (5 + 6j, 6 + 5j), ()), state)
        state = self.move((self.w_piece, (1j, 1 + 2j), ()), state)
        state = self.move((self.b_piece, (4 + 7j, 5 + 6j), ()), state)
        state = self.move((self.w_piece, (2 + 3j, 3 + 4j), ()), state)
        state = self.move((self.b_piece, (4 + 5j, 2 + 3j, 1j), ( 3 + 4j, 1 + 2j)), state)
        state = self.move((self.w_piece, (2 + 1j, 1 + 2j), ()), state)
        state = self.move((self.b_piece, (5j, 1 + 4j), ()), state)
        state = self.move((self.w_piece, (1 + 0j, 2 + 1j), ()), state)
        state = self.move((self.b_piece, (1j, 1 + 0j), ()), state)  # black piece promoted
        state = self.move((self.w_piece, (3 + 2j, 4 + 3j), ()), state)
        expected = {(self.b_king, (1 + 0j, 3 + 2j, 5 + 4j), (2 + 1j, 4 + 3j))}
        self.valid_paths_helper(state, expected, self.b_piece)

    def valid_paths_helper(self, state, expected, player):
        board_state = game.Board(state, self.borders)
        actual_output = board_state.find_valid_moves(player)
        self.assertEqual(expected, actual_output)


if __name__ == "__main__":
    unittest.main()
