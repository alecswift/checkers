import unittest
from unittest import TestCase
from checkers import Board, Player


class TestCheckers(TestCase):
    """Tests for the CheckersGame module"""

    def setUp(self):
        self.board = Board()
        self.player_1 = Player('black', self.board)

    def test_valid_path_method_with_initial_board_state(self) -> None:
        expected = [
            (5j, 1 + 4j),
            (2 + 5j, 1 + 4j),
            (2 + 5j, 3 + 4j),
            (4 + 5j, 3 + 4j),
            (4 + 5j, 5 + 4j),
            (6 + 5j, 5 + 4j),
            (6 + 5j, 7 + 4j),
        ]
        actual_output = self.player_1.valid_paths()
        self.assertEqual(expected, actual_output)


if __name__ == "__main__":
    unittest.main()
