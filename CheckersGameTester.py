import unittest
from unittest import TestCase
from CheckersGame import Checkers, Player


class CheckersTester(TestCase):
    """Tests for the CheckersGame module"""

    def setUp(self):
        self.checkers = Checkers()

    def test_checkers_create_player_method(self):
        """Test the Checkers class create player method"""
        create_player_return = self.checkers.create_player("Jiminy Cricket", "Black")
        self.assertIsInstance(create_player_return, Player)
        player_in_dict = self.checkers.get_players()["Jiminy Cricket"]
        self.assertEqual(player_in_dict, create_player_return)


if __name__ == "__main__":
    unittest.main()
