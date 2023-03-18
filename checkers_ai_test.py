import unittest
from board import Board
import checkers_ai


class TestCheckersAi(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.initial_board_dict = self.board.board
        self.initial_state = checkers_ai.init_state(self.initial_board_dict)
        self.borders = checkers_ai.init_borders()

    def tearDown(self):
        del self.board
        del self.initial_board_dict
        del self.initial_state
        del self.borders

    def test_init_state_method_with_initial_board(self):
        actual_output = set(self.initial_state)
        expected = set((
            (1+0j, 2,),
            (3+0j, 2,),
            (5+0j, 2,),
            (7+0j, 2,),
            (0+1j, 2,),
            (2+1j, 2,),
            (4+1j, 2,),
            (6+1j, 2,),
            (1+2j, 2,),
            (3+2j, 2,),
            (5+2j, 2,),
            (7+2j, 2,),
            (0+5j, 1,),
            (2+5j, 1,),
            (4+5j, 1,),
            (6+5j, 1,),
            (1+6j, 1,),
            (3+6j, 1,),
            (5+6j, 1,),
            (7+6j, 1,),
            (0+7j, 1,),
            (2+7j, 1,),
            (4+7j, 1,),
            (6+7j, 1,),
            (0+3j, 0,),
            (2+3j, 0,),
            (4+3j, 0,),
            (6+3j, 0,),
            (1+4j, 0,),
            (3+4j, 0,),
            (5+4j, 0,),
            (7+4j, 0,),
        ))
        self.assertEqual(actual_output, expected)

    def test_valid_move_method_with_initial_board_state(self):
        state_obj = checkers_ai.State(self.initial_state, self.borders)
        state_obj.valid_moves(False)
        expected = set(
            [
                (1, 5j, 1 + 4j),
                (1, 2 + 5j, 1 + 4j),
                (1, 2 + 5j, 3 + 4j),
                (1, 4 + 5j, 3 + 4j),
                (1, 4 + 5j, 5 + 4j),
                (1, 6 + 5j, 5 + 4j),
                (1, 6 + 5j, 7 + 4j),
            ]
        )
        actual_output = set(state_obj.paths)
        self.assertEqual(expected, actual_output)

    def test_capture_move(self):
        state = checkers_ai.make_move((1, 5j, 1 + 4j), self.initial_state)
        state = checkers_ai.make_move((2, 3 + 2j, 2 + 3j), state)
        expected = set([(1, 1 + 4j, 2 + 3j, 3 + 2j)])
        self.valid_paths_helper(state, expected)

    def test_valid_paths_method_with_double_capture(self):
        state = checkers_ai.make_move((1, 5j, 1 + 4j), self.initial_state)
        state = checkers_ai.make_move((2, 5 + 2j, 4 + 3j), state)
        state = checkers_ai.make_move((1, 6 + 5j, 7 + 4j), state)
        state = checkers_ai.make_move((2, 6 + 1j, 5 + 2j), state)
        state = checkers_ai.make_move((1, 1 + 6j, 5j), state)
        state = checkers_ai.make_move((2, 4 + 3j, 3 + 4j), state)
        expected = {(1, 2 + 5j, 3 + 4j, 4 + 3j, 5 + 2j, 6 + 1j)}
        self.valid_paths_helper(state, expected)
        
        

    def test_valid_paths_method_with_double_capture_2(self):
        state = checkers_ai.make_move((1, 5j, 1 + 4j), self.initial_state)
        state = checkers_ai.make_move((2, 5 + 2j, 4 + 3j), state)
        state = checkers_ai.make_move((1, 6 + 5j, 7 + 4j), state)
        state = checkers_ai.make_move((2, 6 + 1j, 5 + 2j), state)
        state = checkers_ai.make_move((1, 1 + 6j, 5j), state)
        state = checkers_ai.make_move((2, 5 + 0j, 6 + 1j), state)
        state = checkers_ai.make_move((1, 7j, 1 + 6j), state)
        state = checkers_ai.make_move((2, 3 + 2j, 2 + 3j), state)
        expected = {(1, 1 + 4j, 2 + 3j, 3 + 2j, 4 + 1j, 5 + 0j)}
        self.valid_paths_helper(state, expected)

    def test_valid_paths_with_king_double_capture(self):
        state = checkers_ai.make_move((1, 6 + 5j, 7 + 4j), self.initial_state)
        state = checkers_ai.make_move((2, 1 + 2j, 2 + 3j), state)
        state = checkers_ai.make_move((1, 5 + 6j, 6 + 5j), state)
        state = checkers_ai.make_move((2, 1j, 1 + 2j), state)
        state = checkers_ai.make_move((1, 4 + 7j, 5 + 6j), state)
        state = checkers_ai.make_move((2, 2 + 3j, 3 + 4j), state)
        state = checkers_ai.make_move(
            (1, 4 + 5j, 3 + 4j, 2 + 3j, 1 + 2j, 1j), state
        )
        state = checkers_ai.make_move((2, 2 + 1j, 1 + 2j), state)
        state = checkers_ai.make_move((1, 5j, 1 + 4j), state)
        state = checkers_ai.make_move((2, 1 + 0j, 2 + 1j), state)
        state = checkers_ai.make_move((1, 1j, 1 + 0j), state)  # black piece promoted
        state = checkers_ai.make_move((2, 3 + 2j, 4 + 3j), state)
        expected = {(3, 1 + 0j, 2 + 1j, 3 + 2j, 4 + 3j, 5 + 4j)}
        self.valid_paths_helper(state, expected)

    def valid_paths_helper(self, state, expected):
        state_obj = checkers_ai.State(state, self.borders)
        state_obj.valid_moves(False)
        actual_output = state_obj.paths
        self.assertEqual(expected, actual_output)

if __name__ == "__main__":
    unittest.main()