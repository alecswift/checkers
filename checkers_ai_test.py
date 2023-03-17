import unittest
from board import Board
import checkers_ai


class TestCheckersAi(unittest.TestCase):

    def test_init_state_method_with_initial_board(self):
        board = Board()
        initial_board_dict = board.board
        actual_output = set(checkers_ai.init_state(initial_board_dict))
        expected = set((
            (1+0j, 0,),
            (3+0j, 0,),
            (5+0j, 0,),
            (7+0j, 0,),
            (0+1j, 0,),
            (2+1j, 0,),
            (4+1j, 0,),
            (6+1j, 0,),
            (1+2j, 0,),
            (3+2j, 0,),
            (5+2j, 0,),
            (7+2j, 0,),
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
            (0+3j, None,),
            (2+3j, None,),
            (4+3j, None,),
            (6+3j, None,),
            (1+4j, None,),
            (3+4j, None,),
            (5+4j, None,),
            (7+4j, None,),
        ))
        self.assertEqual(actual_output, expected)

if __name__ == "__main__":
    unittest.main()