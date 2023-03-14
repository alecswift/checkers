import unittest
from unittest import TestCase
from board import Board
from player import Player


class TestPlayer(TestCase):
    """Tests for the player module"""

    def setUp(self):
        self.board = Board()
        self.player_1 = Player("black", self.board)
        self.player_2 = Player("white", self.board)

    def test_potential_path_method_with_initial_board_state(self) -> None:
        expected = set(
            [
                (5j, 1 + 4j),
                (2 + 5j, 1 + 4j),
                (2 + 5j, 3 + 4j),
                (4 + 5j, 3 + 4j),
                (4 + 5j, 5 + 4j),
                (6 + 5j, 5 + 4j),
                (6 + 5j, 7 + 4j),
            ]
        )
        actual_output = set(self.player_1.potential_paths())
        self.assertEqual(expected, actual_output)

    def test_prune_paths_method_with_capture_move(self):
        self.player_1.no_capture_move(5j, 1 + 4j)
        self.player_2.no_capture_move(3 + 2j, 2 + 3j)
        expected = set([(1 + 4j, 2 + 3j, 3 + 2j)])
        potential_paths = self.player_1.potential_paths()
        actual_output = set(self.player_1.prune_paths(potential_paths))
        self.assertEqual(expected, actual_output)

    def test_capture_move_method_return_for_single_capture(self):
        self.player_1.no_capture_move(5j, 1 + 4j)
        self.player_2.no_capture_move(3 + 2j, 2 + 3j)
        expected = (3 + 2j,)
        actual_output = self.player_1.capture_move(
            (1 + 4j, 2 + 3j, 3 + 2j), self.player_2
        )
        self.assertEqual(expected, actual_output)


if __name__ == "__main__":
    unittest.main()
