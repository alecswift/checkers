import unittest
from board import Board
import checkers_ai


class TestCheckersAi(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.initial_board_dict = self.board.board
        self.initial_state = checkers_ai.init_state(self.initial_board_dict)

    def tearDown(self):
        del self.board
        del self.initial_board_dict
        del self.initial_state

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
        borders = checkers_ai.init_borders()
        state = checkers_ai.State(self.initial_state, borders)
        state.valid_moves(False)
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
        actual_output = set(state.paths)
        self.assertEqual(expected, actual_output)

if __name__ == "__main__":
    unittest.main()