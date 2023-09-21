# Author: Christopher Partin
# GitHub username: Korachof
# Date: 3/7/2023
# Description: Pseudocode/outlining code for Checkers portfolio project. Will declare each class and method that I
#   believe I will use, and will provide a docstring for each detailing what those sections do. Afterward, it will
#   answer a variety of scenario questions to prepare our thinking and push us to outline our approach.


class Checkers:
    """Will allow for two players to play a traditional game of checkers. Will create the game, the board, and
        players using composition and the Player class."""
    def create_player(self, player_name, piece_color):
        """Use composition to create a player object using the Player class"""
        pass


    def play_game(self, player_name, starting_square_location, destination_square_location):
        """Using tuple format, a player will use this function to make a move in the checkers game.
            Uses exceptions to make sure a player does not play out of turn or move to an invalid square.
            Will also promote pieces to kings/triple kings when relevant and returns the number of captured pieces after
            a move has been made."""
        pass

    def get_checker_details(self, square_location):
        """Returns details of a checker at the specified location. If no checker is present, return None. If black is
            present, return “Black,” if white, return “White.” If kinged, returns format: “Black_king.” If
            triple kinged, returns 'Black_Triple_King.'"""
        pass

    def print_board(self):
        """Print the current board, with current piece locations, in the form of an array."""

    def game_winner(self):
        """Returns the name of the player who won. If it hasn’t ended, returns “Game has not ended.” It will
            not check outcomes based on obscure victory conditions, like blocking all opponent pieces."""
        pass

class Player:
    """Creates a player object through composition and the Checkers class"""

    def get_king_count(self):
        """Returns the number of kings the specified player has."""
        pass

    def get_triple_king_count(self):
        """Returns the number of triple king pieces the player has."""
        pass

    def get_captured_pieces_count(self):
        """Returns the number of pieces the specified player has captured from the opponent."""
        pass


# DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS

# 1) Initializing the Checkers and Player classes
#   I will use composition to initalize the player class/create player objects.
#   The Checkers class will be initalized as classes usually are, at the end and declared as a specific checkers game.
#
# 2) Determining how to implement create_player method
#   Already discussed this, but I will be using composition, because composition uses a "has a" relationship,
#   and while Checkers has players, it is not a player (and a player is not Checkers).
#
# 3) Determining how to implement print_board method
#   This one is particularly interesting, and I will likely change my mind as a I start to do it. My first thought
#   is to use a series of dictionaries for each position inside of a list, but what I'll likely do is just a list
#   of rows (each of which will be its own list). Once I start getting deeper into it, though, I may find a method I
#   like more.
#
# 4) Determining how to implement game_winner method and how to check the winning condition
#   In theory, game_winner could be called as soon as a player actually wins the game in a traditional way, which is
#   to say, when all of the pieces of the opponent's side == 0, call game_winner. This could either use opponent's game
#   pieces == 0, or get_captured_pieces_count = 12. I may try to do the latter first, and go from there.
#
# 5) Determining how to implement play_game method; how to validate a move. Determine how to identify the promotion to
#       king or triple king. Determine how to handle pieces being captured.
#   play_game will be implemented by having players type in their moves in the form of a tuple, as described. A move
#   will be validated by writing out the positions on a physical board of checkers, and then using conditional
#   statements to make sure that only moves forward that move one square (space) are legal if all spaces around the
#   piece are empty. If they are not, the spaces that are not empty will allow for a "hop" to the adjacent space. This
#   will likely be determined using those conditionals, and allowing for a jump to a position + 1 row/ +1 column. But
#   this will require a proper visual for me to use patterns so I can create a validation that works every time. Once
#   a piece moves to the opposite row of where it started (if piece is in these specific locations, do this), likely
#   by placing white and black on two permanent sides of the board, so if white reaches, say, row 8, then it will be
#   kinged, at which point it's validations will change to allow it to move backwards, etc. If black reaches, say, row
#   1, then it will also be kinged, etc.
#
# 6) Determine how to implement get_checker_details method
#   So this will likely involve me replacing the "piece color" with, say, Black_king, or Black_Triple_King. Then I will
#   use conditionals, like "if piece_color == black_king" would allow for a a piece to move to forbidden spots that
#   normal pieces cannot go.
# 7) Initializing exception classes
#   We need at least these exceptions:  OutofTurn, InvalidSquare exception, and InvalidPlayer. I will use try/except,
#   along with conditional statements, to determine if the exceptions need to be raised. For OutofTurn, I want to
#   check who last made a move. If black made a move, and there are no valid pieces for them to take at the new location,
#   and they try to go again, they'll get an OutofTurn error. If they try to move to a square that's either behind them,
#   or in a position where another piece already is (aka, the position is not None), it should raise InvalidSquare. If
#   someone tries to make a move, and their name does not == player_name in the game,then InvalidPlayer will be raised.
