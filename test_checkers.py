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

    def tearDown(self):
        del self.board
        del self.player_1
        del self.player_2

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
        self.prune_test_helper(expected)

    def test_prune_paths_method_with_double_capture(self):
        self.player_1.no_capture_move(5j, 1 + 4j)
        self.player_2.no_capture_move(5 + 2j, 4 + 3j)
        self.player_1.no_capture_move(6 + 5j, 7 + 4j)
        self.player_2.no_capture_move(6 + 1j, 5 + 2j)
        self.player_1.no_capture_move(1 + 6j, 5j)
        self.player_2.no_capture_move(4 + 3j, 3 + 4j)
        expected = {(2 + 5j, 3 + 4j, 4 + 3j, 5 + 2j, 6 + 1j)}
        self.prune_test_helper(expected)

    def test_prune_paths_method_with_double_capture_2(self):
        self.player_1.no_capture_move(5j, 1 + 4j)
        self.player_2.no_capture_move(5 + 2j, 4 + 3j)
        self.player_1.no_capture_move(6 + 5j, 7 + 4j)
        self.player_2.no_capture_move(6 + 1j, 5 + 2j)
        self.player_1.no_capture_move(1 + 6j, 5j)
        self.player_2.no_capture_move(5 + 0j, 6 + 1j)
        self.player_1.no_capture_move(7j, 1 + 6j)
        self.player_2.no_capture_move(3 + 2j, 2 + 3j)
        expected = {(1 + 4j, 2 + 3j, 3 + 2j, 4 + 1j, 5 + 0j)}
        self.prune_test_helper(expected)

    def test_prune_paths_with_king_double_capture(self):
        self.player_1.no_capture_move(6 + 5j, 7 + 4j)
        self.player_2.no_capture_move(1 + 2j, 2 + 3j)
        self.player_1.no_capture_move(5 + 6j, 6 + 5j)
        self.player_2.no_capture_move(1j, 1 + 2j)
        self.player_1.no_capture_move(4 + 7j, 5 + 6j)
        self.player_2.no_capture_move(2 + 3j, 3 + 4j)
        new_path = self.player_1.capture_move(
            (4 + 5j, 3 + 4j, 2 + 3j, 1 + 2j, 1j), self.player_2
        )
        self.player_1.capture_move(new_path, self.player_2)
        self.player_2.no_capture_move(2 + 1j, 1 + 2j)
        self.player_1.no_capture_move(5j, 1 + 4j)
        self.player_2.no_capture_move(1 + 0j, 2 + 1j)
        self.player_1.no_capture_move(1j, 1 + 0j)  # black piece promoted
        self.player_2.no_capture_move(3 + 2j, 4 + 3j)
        expected = {(1 + 0j, 2 + 1j, 3 + 2j, 4 + 3j, 5 + 4j)}
        print(self.board.board_array())
        self.prune_test_helper(expected)

    def prune_test_helper(self, expected):
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
