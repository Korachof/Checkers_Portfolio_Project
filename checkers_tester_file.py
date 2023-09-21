
import unittest

from CheckersGame import CheckersBoard
from CheckersGame import Checkers
from CheckersGame import Player


class TestStandardMoves(unittest.TestCase):
    """Test to see if player standard moves are correct"""

    def test_1(self):
        """Test to make sure standard moves actually move the pieces to destination"""
        joes_game = Checkers()

        joe = joes_game.create_player("Joe", "White")
        bob = joes_game.create_player("Bob", "Black")
        joes_game.print_board()

        joes_game.play_game("Bob", (5, 0), (4, 1))
        joes_game.play_game("Joe", (2, 1), (3, 2))
        self.assertEqual(joes_game.get_checker_details((4, 1)), "Black")
        self.assertEqual(joes_game.get_checker_details((3, 2)), "White")

    def test_2(self):
        """Test to make sure starting location is None when standard moves are made"""
        joes_game = Checkers()

        joe = joes_game.create_player("Joe", "White")
        bob = joes_game.create_player("Bob", "Black")
        joes_game.print_board()

        joes_game.play_game("Bob", (5, 0), (4, 1))
        joes_game.play_game("Joe", (2, 1), (3, 2))
        self.assertIs(joes_game.get_checker_details((5, 0)), None)
        self.assertIs(joes_game.get_checker_details((2, 1)), None)

    def test_3(self):
        """Test to make sure pieces that are supposed to be captured are actually captured"""
        joes_game = Checkers()

        joe = joes_game.create_player("Joe", "White")
        bob = joes_game.create_player("Bob", "Black")
        joes_game.print_board()

        joes_game.play_game("Bob", (5, 0), (4, 1))
        joes_game.play_game("Joe", (2, 1), (3, 2))
        joes_game.play_game("Bob", (5, 6), (4, 5))
        joes_game.play_game("Joe", (2, 3), (3, 4))
        joes_game.play_game("Bob", (4, 1), (2, 3))


        self.assertIs(joes_game.get_checker_details((3, 2)), None)          # piece that should be captured
        self.assertEqual(bob.get_captured_pieces_count(), 1)                # bob's captured pieces should be 1


    def test_4(self):
        """Make sure white's captures also work"""
        joes_game = Checkers()

        joe = joes_game.create_player("Joe", "White")
        bob = joes_game.create_player("Bob", "Black")
        joes_game.print_board()

        joes_game.play_game("Bob", (5, 0), (4, 1))
        joes_game.play_game("Joe", (2, 1), (3, 2))
        joes_game.play_game("Bob", (5, 6), (4, 5))
        joes_game.play_game("Joe", (2, 3), (3, 4))
        joes_game.play_game("Bob", (4, 1), (2, 3))
        joes_game.play_game("Joe", (1, 4), (3, 2))

        self.assertIs(joes_game.get_checker_details((2, 3)), None)
        self.assertEqual(joe.get_captured_pieces_count(), 1)

class TestKingMove(unittest.TestCase):
    """Test to make sure kings for both colors work"""

    def test_1(self):
        """Test to make sure both pieces are kinged when they move to the appropriate space"""
        joes_game = Checkers()

        joe = joes_game.create_player("Joe", "White")
        bob = joes_game.create_player("Bob", "Black")

        joes_game.play_game("Bob", (7, 0), (0, 0))
        joes_game.play_game("Joe", (0, 1), (7, 1))
        joes_game.print_board()
        self.assertEqual(joes_game.get_checker_details((0, 0)), "Black_king")
        self.assertEqual(joes_game.get_checker_details((7, 1)), "White_king")

    def test_2(self):
        """Test to make sure triple kings for both colors work"""
        joes_game = Checkers()

        joe = joes_game.create_player("Joe", "White")
        bob = joes_game.create_player("Bob", "Black")
        joes_game.print_board()

        joes_game.play_game("Bob", (7, 0), (0, 0))
        print(joes_game.get_black_turn())
        joes_game.play_game("Joe", (0, 1), (7, 1))
        print(joes_game.get_white_turn())
        joes_game.play_game("Bob", (0, 0), (7, 0))
        print(joes_game.get_black_turn())
        joes_game.print_board()
        joes_game.play_game("Joe", (7, 1), (0, 1))
        print(joes_game.get_white_turn())

        self.assertEqual(joes_game.get_checker_details((7, 0)), "Black_Triple_King")
        self.assertEqual(joes_game.get_checker_details((0, 1)), "White_Triple_King")


if __name__ == "__main__":
    unittest.main()
