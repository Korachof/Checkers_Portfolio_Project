# Author: Christopher Partin
# GitHub username: Korachof
# Date: 3/19/2023
# Description: A checkers game that allows players to move pieces around a board, capture pieces, king and triple
#   king pieces, and check who won. Can also return how many kings and triple kings each player has, as well as their
#   color. Has exceptions for OutofTurn, InvalidSquare, and InvalidPlayer.
#   Just like in regular checkers, black goes first and is enforced to go first.



class OutofTurn(Exception):
    """Player tries to make a play when it isn't their turn"""
    pass


class InvalidSquare(Exception):
    """Player tries to move a piece that doesn't belong to them or to a square that is invalid."""
    pass


class InvalidPlayer(Exception):
    """Error if someone tries to make a move with a player_name not in the game"""
    pass


class CheckersBoard:
    """Class that sets up a generic checkers board"""
    def __init__(self):
        """For reference: tuple_board = [
            [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)]
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)]
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)]
            [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7)]
            [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7)]
            [(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7)]
            [(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7)]
            [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
            ]"""
        self._game_board = [
            [None, "White", None, "White", None, "White", None, "White"],
            ["White", None, "White", None, "White", None, "White", None],
            [None, "White", None, "White", None, "White", None, "White"],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None,  None, None, None, None],
            ["Black", None, "Black", None, "Black", None, "Black", None],
            [None, "Black", None, "Black", None, "Black", None, "Black"],
            ["Black", None, "Black", None, "Black", None, "Black", None]
            ]

    def get_game_board(self):
        """Get the game board"""
        return self._game_board


class Checkers:
    """Will allow for two players to play a traditional game of checkers. Will create the game, the board, and
        players using composition and the Player class."""

    def __init__(self):
        self._board = CheckersBoard().get_game_board()
        self._player_1 = None
        self._player_2 = None
        self._black_turn = 0
        self._white_turn = 0
        self._black_capture = 0
        self._white_capture = 0

    def get_black_turn(self):
        """Get how many turns black has played"""
        return self._black_turn

    def get_white_turn(self):
        """Get how many turns white has played"""
        return self._white_turn

    def create_player(self, player_name, piece_color):
        """create a player object using the Player class"""
        if self._player_1 is None:
            self._player_1 = Player(player_name, piece_color, self)
            return self._player_1

        if self._player_2 is None:
            self._player_2 = Player(player_name, piece_color, self)
            return self._player_2


    def play_game(self, player_name, starting_square_location, destination_square_location):
        """Using tuple format, a player will use this function to make a move in the checkers game.
            Uses exceptions to make sure a player does not play out of turn or move to an invalid square.
            Will also promote pieces to kings/triple kings when relevant and returns the number of captured pieces after
            a move has been made. Will also have a counter for player turns and will enforce jumps after a move"""
        start = self._board[starting_square_location[0]][starting_square_location[1]]

        end = self._board[destination_square_location[0]][destination_square_location[1]]

        def in_bounds():
            """Check if the player's move is in-bounds or not"""
            # If the destination square is off the table, raise exception.
            if destination_square_location[0] > 7 or destination_square_location[1] > 7:
                raise InvalidSquare

            # if the destination square is off the table, raise exception.
            elif destination_square_location[0] < 0 or destination_square_location[1] < 0:
                raise InvalidSquare

            # if the destination square is not None, then it cannot move to that location.
            if self._board[destination_square_location[0]][destination_square_location[1]] is not None:
                raise InvalidSquare

        def validate_turn():
            """Validate whose turn it is"""
            # Figure out whose turn it is
            if self._player_1.get_player_name() == player_name:
                player = self._player_1

            elif self._player_2.get_player_name() == player_name:
                player = self._player_2
            # if player_name is not the name of player_1 or player_2, raise InvalidPlayer
            else:
                raise InvalidPlayer

            # if it's black's turn, make sure the current player is playing black (black goes first)
            if self._black_turn <= self._white_turn:
                if player.get_checker_color() == "Black":
                    # Because it's black's turn, the piece being moved must be black
                    if self.get_checker_details(starting_square_location) != "Black" and \
                        self.get_checker_details(starting_square_location) != "Black_king" and \
                            self.get_checker_details(starting_square_location) != "Black_Triple_King":
                        raise InvalidSquare
                else:
                    raise OutofTurn

            # if it's white's turn, make sure the current player is playing white
            elif self._white_turn < self._black_turn:
                if player.get_checker_color() == "White":
                    # Because it's white's turn, the piece being moved must be white
                    if self.get_checker_details(starting_square_location) != "White" and \
                        self.get_checker_details(starting_square_location) != "White_king" and \
                            self.get_checker_details(starting_square_location) != "White_Triple_King":
                        raise InvalidSquare
                else:
                    raise OutofTurn

            # Now that we have verified player color, we need to verify if a piece is captured by the move
        def black_standard_capture():
            """If the piece is black, check if it needs to capture a piece"""
            # if the piece is a standard black piece, proceed
            if self.get_checker_details(starting_square_location) == "Black":

                # Check first legal position, then proceed
                if starting_square_location[0] - 1 >= 0 and starting_square_location[1] - 1 >= 0:
                    if self._board[starting_square_location[0] - 1][starting_square_location[1] - 1] == "White" or \
                            self._board[starting_square_location[0] - 1][
                                starting_square_location[1] - 1] == "White_king" or \
                            self._board[starting_square_location[0] - 1][
                                starting_square_location[1] - 1] == "White_Triple_King":
                        # if the space after enemy square is the destination, capture piece
                        if destination_square_location[0] == starting_square_location[0] - 2 and \
                                destination_square_location[1] == starting_square_location[1] - 2:
                            self._board[starting_square_location[0] - 1][starting_square_location[1] - 1] = None
                            self._black_capture += 1

                            # check if another capture needs to happen. If not, turn + 1
                            if destination_square_location[0] - 2 >= 0 and destination_square_location[1] - 2 >= 0:
                                if self._board[destination_square_location[0] - 1][
                                    destination_square_location[1] - 1] is None or \
                                        self._board[destination_square_location[0] - 1][
                                            destination_square_location[1] - 1] != "White" and \
                                        self._board[destination_square_location[0] - 1][
                                            destination_square_location[1] - 1] != "White_king" and \
                                        self._board[destination_square_location[0] - 1][
                                            destination_square_location[1] - 1] != "White_Triple_King" or \
                                        self._board[destination_square_location[0] - 2][
                                            destination_square_location[1] - 2] is not None:
                                    self._black_turn += 1
                                    return

                            if destination_square_location[0] - 2 >= 0:
                                if self._board[destination_square_location[0] - 1][
                                    destination_square_location[1]] is None or \
                                        self._board[destination_square_location[0] - 1][
                                            destination_square_location[1]] != "White" and \
                                        self._board[destination_square_location[0] - 1][
                                            destination_square_location[1]] != "White_king" and \
                                        self._board[destination_square_location[0] - 1][
                                            destination_square_location[1]] != "White_Triple_King" or \
                                        self._board[destination_square_location[0] - 2][
                                            destination_square_location[1]] is not None:
                                    self._black_turn += 1
                                    return

                            if destination_square_location[0] - 2 >= 0 and destination_square_location[1] + 2 <= 7:
                                if self._board[destination_square_location[0] - 1][
                                    destination_square_location[1] + 1] is None or \
                                        self._board[destination_square_location[0] - 1][
                                            destination_square_location[1] + 1] != "White" and \
                                        self._board[destination_square_location[0] - 1][
                                            destination_square_location[1] + 1] != "White_king" and \
                                        self._board[destination_square_location[0] - 1][
                                            destination_square_location[1] + 1] != "White_Triple_King" or \
                                        self._board[destination_square_location[0] - 2][
                                            destination_square_location[1] + 2] is not None:
                                    self._black_turn += 1
                                    return

                            else:
                                self._black_turn += 1
                                return


                #check second legal position, then proceed
                if starting_square_location[0] - 1 >= 0:
                    if self._board[starting_square_location[0] - 1][starting_square_location[1]] == "White" or \
                         self._board[starting_square_location[0] - 1][starting_square_location[1]] == "White_king" or \
                         self._board[starting_square_location[0] - 1][
                             starting_square_location[1]] == "White_Triple_King":
                        # if the space after enemy square is the destination, capture piece
                        if destination_square_location[0] == starting_square_location[0] - 2 and \
                                destination_square_location[1] == starting_square_location[1]:
                            self._board[starting_square_location[0] - 1][starting_square_location[1]] = None
                            self._black_capture += 1

                        # check if another capture needs to happen. If not, turn +1
                        if destination_square_location[0] - 2 >= 0 and destination_square_location[1] - 2 >= 0:
                            if self._board[destination_square_location[0] - 1][
                                destination_square_location[1] - 1] is None or \
                                    self._board[destination_square_location[0] - 1][
                                        destination_square_location[1] - 1] != "White" and \
                                    self._board[destination_square_location[0] - 1][
                                        destination_square_location[1] - 1] != "White_king" and \
                                    self._board[destination_square_location[0] - 1][
                                        destination_square_location[1] - 1] != "White_Triple_King" or \
                                    self._board[destination_square_location[0] - 2][
                                        destination_square_location[1] - 2] is not None:
                                self._black_turn += 1
                                return

                        if destination_square_location[0] - 2 >= 0:
                            if self._board[destination_square_location[0] - 1][
                                destination_square_location[1]] is None or \
                                    self._board[destination_square_location[0] - 1][
                                        destination_square_location[1]] != "White" and \
                                    self._board[destination_square_location[0] - 1][
                                        destination_square_location[1]] != "White_king" and \
                                    self._board[destination_square_location[0] - 1][
                                        destination_square_location[1]] != "White_Triple_King" or \
                                    self._board[destination_square_location[0] - 2][
                                        destination_square_location[1]] is not None:
                                self._black_turn += 1
                                return

                        if destination_square_location[0] - 2 >= 0 and destination_square_location[1] + 2 <= 7:
                            if self._board[destination_square_location[0] - 1][
                                destination_square_location[1] + 1] is None or \
                                    self._board[destination_square_location[0] - 1][
                                        destination_square_location[1] + 1] != "White" and \
                                    self._board[destination_square_location[0] - 1][
                                        destination_square_location[1] + 1] != "White_king" and \
                                    self._board[destination_square_location[0] - 1][
                                        destination_square_location[1] + 1] != "White_Triple_King" or \
                                    self._board[destination_square_location[0] - 2][
                                        destination_square_location[1] + 2] is not None:
                                self._black_turn += 1
                                return

                        else:
                            self._black_turn += 1
                            return


                # check last legal position, then proceed
                if starting_square_location[0] - 1 >= 0 and starting_square_location[1] + 1 <= 7:
                    if self._board[starting_square_location[0] - 1][starting_square_location[1] + 1] == "White" or \
                         self._board[starting_square_location[0] - 1][starting_square_location[1] + 1] == "White_king" or \
                         self._board[starting_square_location[0] - 1][starting_square_location[1] + 1] == "White_Triple_King":
                        # if the space after enemy square is the destination, capture piece
                        if destination_square_location[0] == starting_square_location[0] - 2 and \
                                destination_square_location[1] == starting_square_location[1] + 2:
                            self._board[starting_square_location[0] - 1][starting_square_location[1] + 1] = None
                            self._black_capture += 1

                        # check if another capture needs to happen. If not, turn +1
                        if destination_square_location[0] - 2 >= 0 and destination_square_location[1] - 2 >= 0:
                            if self._board[destination_square_location[0] - 1][
                                destination_square_location[1] - 1] is None or \
                                    self._board[destination_square_location[0] - 1][
                                        destination_square_location[1] - 1] != "White" and \
                                    self._board[destination_square_location[0] - 1][
                                        destination_square_location[1] - 1] != "White_king" and \
                                    self._board[destination_square_location[0] - 1][
                                        destination_square_location[1] - 1] != "White_Triple_King" or \
                                    self._board[destination_square_location[0] - 2][
                                        destination_square_location[1] - 2] is not None:
                                self._black_turn += 1
                                return

                        if destination_square_location[0] - 2 >= 0:
                            if self._board[destination_square_location[0] - 1][
                                destination_square_location[1]] is None or \
                                    self._board[destination_square_location[0] - 1][
                                        destination_square_location[1]] != "White" and \
                                    self._board[destination_square_location[0] - 1][
                                        destination_square_location[1]] != "White_king" and \
                                    self._board[destination_square_location[0] - 1][
                                        destination_square_location[1]] != "White_Triple_King" or \
                                    self._board[destination_square_location[0] - 2][
                                        destination_square_location[1]] is not None:
                                self._black_turn += 1
                                return

                        if destination_square_location[0] - 2 >= 0 and destination_square_location[1] + 2 <= 7:
                            if self._board[destination_square_location[0] - 1][
                                destination_square_location[1] + 1] is None or \
                                    self._board[destination_square_location[0] - 1][
                                        destination_square_location[1] + 1] != "White" and \
                                    self._board[destination_square_location[0] - 1][
                                        destination_square_location[1] + 1] != "White_king" and \
                                    self._board[destination_square_location[0] - 1][
                                        destination_square_location[1] + 1] != "White_Triple_King" or \
                                    self._board[destination_square_location[0] - 2][
                                        destination_square_location[1] + 2] is not None:
                                self._black_turn += 1
                                return

                        else:
                            self._black_turn += 1
                            return

                    else:
                        self._black_turn += 1

                else:
                    #if there's no capture, + 1 turn
                    self._black_turn += 1

        def white_standard_capture():
            """If the piece is white, check if it needs to capture a piece"""
            # if the piece is a standard white piece, proceed
            if self.get_checker_details(starting_square_location) == "White":

                # Check first legal position, then proceed
                if starting_square_location[0] + 1 <= 7 and starting_square_location[1] + 1 <= 7:
                    if self._board[starting_square_location[0] + 1][starting_square_location[1] + 1] == "Black" or \
                            self._board[starting_square_location[0] + 1][
                                starting_square_location[1] + 1] == "Black_king" or \
                            self._board[starting_square_location[0] + 1][
                                starting_square_location[1] + 1] == "Black_Triple_King":
                        # if the space after enemy square is the destination, capture piece
                        if destination_square_location[0] == starting_square_location[0] + 2 and \
                                destination_square_location[1] == starting_square_location[1] + 2:
                            self._board[starting_square_location[0] + 1][starting_square_location[1] + 1] = None
                            self._white_capture += 1

                            # check if another capture needs to happen. If not, turn +1
                            if destination_square_location[0] + 2 <= 7 and destination_square_location[1] + 2 <= 7:
                                if self._board[destination_square_location[0] + 1][
                                    destination_square_location[1] + 1] is None or \
                                        self._board[destination_square_location[0] + 1][
                                            destination_square_location[1] + 1] != "Black" and \
                                        self._board[destination_square_location[0] + 1][
                                            destination_square_location[1] + 1] != "Black_king" and \
                                        self._board[destination_square_location[0] + 1][
                                            destination_square_location[1] + 1] != "Black_Triple_King" or \
                                        self._board[destination_square_location[0] + 2][
                                            destination_square_location[1] + 2] is not None:
                                    self._white_turn += 1
                                    return

                            if destination_square_location[0] + 2 <= 7:
                                if self._board[destination_square_location[0] + 1][destination_square_location[1]] \
                                        is None or \
                                        self._board[destination_square_location[0] + 1][destination_square_location[1]] \
                                        != "Black" and \
                                        self._board[destination_square_location[0] + 1][destination_square_location[1]] \
                                        != "Black_king" and \
                                        self._board[destination_square_location[0] + 1][
                                            destination_square_location[1]] != \
                                        "Black_Triple_King" or \
                                        self._board[destination_square_location[0] + 2][destination_square_location[1]] \
                                        is not None:
                                    self._white_turn += 1
                                    return

                            if destination_square_location[0] + 2 <= 7 and destination_square_location[1] - 2 >= 0:
                                if self._board[destination_square_location[0] + 1][
                                    destination_square_location[1] - 1] is None or \
                                        self._board[destination_square_location[0] + 1][
                                            destination_square_location[1] - 1] != "Black" and \
                                        self._board[destination_square_location[0] + 1][
                                            destination_square_location[1] - 1] != "Black_king" and \
                                        self._board[destination_square_location[0] + 1][
                                            destination_square_location[1] - 1] != "Black_Triple_King" or \
                                        self._board[destination_square_location[0] + 2][
                                            destination_square_location[1] - 2] is not None:
                                    self._white_turn += 1
                                    return

                            else:
                                self._white_turn += 1
                                return

                # check second legal position, then proceed
                if starting_square_location[0] + 1 <= 7:
                    if self._board[starting_square_location[0] + 1][starting_square_location[1]] \
                            == "Black" or \
                            self._board[starting_square_location[0] + 1][starting_square_location[1]] \
                            == "Black_king" or \
                            self._board[starting_square_location[0] + 1][starting_square_location[1]] \
                            == "Black_Triple_King":
                        # if the space after enemy square is the destination, capture piece
                        if destination_square_location[0] == starting_square_location[0] + 2 and \
                                destination_square_location[1] == starting_square_location[1]:
                            self._board[starting_square_location[0] + 1][starting_square_location[1]] = None
                            self._white_capture += 1

                            # check if another capture needs to happen. If not,turn +1
                            if destination_square_location[0] + 2 <= 7 and destination_square_location[1] + 2 <= 7:
                                if self._board[destination_square_location[0] + 1][
                                    destination_square_location[1] + 1] is None or \
                                        self._board[destination_square_location[0] + 1][
                                            destination_square_location[1] + 1] != "Black" and \
                                        self._board[destination_square_location[0] + 1][
                                            destination_square_location[1] + 1] != "Black_king" and \
                                        self._board[destination_square_location[0] + 1][
                                            destination_square_location[1] + 1] != "Black_Triple_King" or \
                                        self._board[destination_square_location[0] + 2][
                                            destination_square_location[1] + 2] is not None:
                                    self._white_turn += 1
                                    return

                            if destination_square_location[0] + 2 <= 7:
                                if self._board[destination_square_location[0] + 1][destination_square_location[1]] \
                                        is None or \
                                        self._board[destination_square_location[0] + 1][destination_square_location[1]] \
                                        != "Black" and \
                                        self._board[destination_square_location[0] + 1][destination_square_location[1]] \
                                        != "Black_king" and \
                                        self._board[destination_square_location[0] + 1][
                                            destination_square_location[1]] != \
                                        "Black_Triple_King" or \
                                        self._board[destination_square_location[0] + 2][destination_square_location[1]] \
                                        is not None:
                                    self._white_turn += 1
                                    return

                            if destination_square_location[0] + 2 <= 7 and destination_square_location[1] - 2 >= 0:
                                if self._board[destination_square_location[0] + 1][
                                    destination_square_location[1] - 1] is None or \
                                        self._board[destination_square_location[0] + 1][
                                            destination_square_location[1] - 1] != "Black" and \
                                        self._board[destination_square_location[0] + 1][
                                            destination_square_location[1] - 1] != "Black_king" and \
                                        self._board[destination_square_location[0] + 1][
                                            destination_square_location[1] - 1] != "Black_Triple_King" or \
                                        self._board[destination_square_location[0] + 2][
                                            destination_square_location[1] - 2] is not None:
                                    self._white_turn += 1
                                    return

                            else:
                                self._white_turn += 1
                                return

                # check last legal position, then proceed
                if starting_square_location[0] + 1 <= 7 and starting_square_location[1] - 1 >= 0:
                    if self._board[starting_square_location[0] + 1][starting_square_location[1] - 1] \
                            == "Black" or \
                            self._board[starting_square_location[0] + 1][starting_square_location[1] - 1] \
                            == "Black_king" or \
                            self._board[starting_square_location[0] + 1][starting_square_location[1] - 1] \
                            == "Black_Triple_King":
                        # if the space after enemy square is the destination, capture piece
                        if destination_square_location[0] == starting_square_location[0] + 2 and \
                                destination_square_location[1] == starting_square_location[1] - 2:
                            self._board[starting_square_location[0] + 1][starting_square_location[1] - 1] = None
                            self._white_capture += 1

                        # check if another capture needs to happen. If not, turn +1
                        if destination_square_location[0] + 2 <= 7 and destination_square_location[1] + 2 <= 7:
                            if self._board[destination_square_location[0] + 1][
                                destination_square_location[1] + 1] is None or \
                                    self._board[destination_square_location[0] + 1][
                                        destination_square_location[1] + 1] != "Black" and \
                                    self._board[destination_square_location[0] + 1][
                                        destination_square_location[1] + 1] != "Black_king" and \
                                    self._board[destination_square_location[0] + 1][
                                        destination_square_location[1] + 1] != "Black_Triple_King" or \
                                    self._board[destination_square_location[0] + 2][
                                        destination_square_location[1] + 2] is not None:
                                self._white_turn += 1
                                return

                        if destination_square_location[0] + 2 <= 7:
                            if self._board[destination_square_location[0] + 1][destination_square_location[1]] \
                                    is None or \
                                    self._board[destination_square_location[0] + 1][destination_square_location[1]] \
                                    != "Black" and \
                                    self._board[destination_square_location[0] + 1][destination_square_location[1]] \
                                    != "Black_king" and \
                                    self._board[destination_square_location[0] + 1][
                                        destination_square_location[1]] != \
                                    "Black_Triple_King" or \
                                    self._board[destination_square_location[0] + 2][destination_square_location[1]] \
                                    is not None:
                                self._white_turn += 1
                                return

                        if destination_square_location[0] + 2 <= 7 and destination_square_location[1] - 2 >= 0:
                            if self._board[destination_square_location[0] + 1][
                                destination_square_location[1] - 1] is None or \
                                    self._board[destination_square_location[0] + 1][
                                        destination_square_location[1] - 1] != "Black" and \
                                    self._board[destination_square_location[0] + 1][
                                        destination_square_location[1] - 1] != "Black_king" and \
                                    self._board[destination_square_location[0] + 1][
                                        destination_square_location[1] - 1] != "Black_Triple_King" or \
                                    self._board[destination_square_location[0] + 2][
                                        destination_square_location[1] - 2] is not None:
                                self._white_turn += 1
                                return

                        else:
                            self._white_turn += 1
                            return
                    else:
                        self._white_turn += 1
                        return

                else:
                    # if there's no capture, + 1 turn
                    self._white_turn += 1


        def king_capture():
            """If a king or triple king is the piece moving, check if it needs to make a capture"""
            # Figure out whose turn it is
            if self._player_1.get_player_name() == player_name:
                player = self._player_1

            elif self._player_2.get_player_name() == player_name:
                player = self._player_2

            def king_check_turn():
                """If a king or triple king is moving, check for potential single capturing move"""
                # check first potential move
                if destination_square_location[0] - 2 >= 0 and destination_square_location[1] - 2 >= 0:
                    if self._board[destination_square_location[0] - 1][destination_square_location[1] - 1] \
                            is None or \
                            self._board[destination_square_location[0] - 1][
                                destination_square_location[1] - 1] == f"{player.get_checker_color()}" or \
                            self._board[destination_square_location[0] - 1][
                                destination_square_location[1] - 1] == f"{player.get_checker_color()}_king" or \
                            self._board[destination_square_location[0] - 1][
                                destination_square_location[1] - 1] == f"{player.get_checker_color()}_Triple_King" or \
                            self._board[destination_square_location[0] - 2][
                                destination_square_location[1] - 2] is not None:
                        if player.get_checker_color() == "Black":
                            self._black_turn += 1
                            return
                        elif player.get_checker_color() == "White":
                            self._white_turn += 1
                            return

                # check second potential move
                if destination_square_location[0] - 2 >= 0:
                    if self._board[destination_square_location[0] - 1][
                        destination_square_location[1]] is None or \
                            self._board[destination_square_location[0] - 1][
                                destination_square_location[1]] == f"{player.get_checker_color()}" or \
                            self._board[destination_square_location[0] - 1][
                                destination_square_location[1]] == f"{player.get_checker_color()}_king" or \
                            self._board[destination_square_location[0] - 1][destination_square_location[
                                1]] == f"{player.get_checker_color()}_Triple_King" or \
                            self._board[destination_square_location[0] - 2][
                                destination_square_location[1]] is not None:
                        if player.get_checker_color() == "Black":
                            self._black_turn += 1
                            return
                        elif player.get_checker_color() == "White":
                            self._white_turn += 1
                            return

                # check third potential move
                if destination_square_location[0] - 2 >= 0 and destination_square_location[1] + 2 <= 7:
                    if self._board[destination_square_location[0] - 1][
                        destination_square_location[1] - 1] is None or \
                            self._board[destination_square_location[0] - 1][
                                destination_square_location[1] - 1] == f"{player.get_checker_color()}" or \
                            self._board[destination_square_location[0] - 1][
                                destination_square_location[1] - 1] == f"{player.get_checker_color()}_king" or \
                            self._board[destination_square_location[0] - 1][
                                destination_square_location[1] - 1] == f"{player.get_checker_color()}_Triple_King" or \
                            self._board[destination_square_location[0] - 2][
                                destination_square_location[1] - 2] is not None:
                        if player.get_checker_color() == "Black":
                            self._black_turn += 1
                            return
                        elif player.get_checker_color() == "White":
                            self._white_turn += 1
                            return

                # check fourth potential move
                if destination_square_location[0] + 2 <= 7 and destination_square_location[1] + 2 <= 7:
                    if self._board[destination_square_location[0] + 1][
                        destination_square_location[1] + 1] is None or \
                            self._board[destination_square_location[0] + 1][
                                destination_square_location[1] + 1] == f"{player.get_checker_color()}" or \
                            self._board[destination_square_location[0] + 1][
                                destination_square_location[1] + 1] == f"{player.get_checker_color()}_king" or \
                            self._board[destination_square_location[0] + 1][
                                destination_square_location[1] + 1] == f"{player.get_checker_color()}_Triple_King" or \
                            self._board[destination_square_location[0] + 2][
                                destination_square_location[1] + 2] is not None:
                        if player.get_checker_color() == "Black":
                            self._black_turn += 1
                            return
                        elif player.get_checker_color() == "White":
                            self._white_turn += 1
                            return

                # check fifth potential move
                if destination_square_location[0] + 2 <= 7:
                    if self._board[destination_square_location[0] + 1][
                        destination_square_location[1]] is None or \
                            self._board[destination_square_location[0] + 1][
                                destination_square_location[1]] == f"{player.get_checker_color()}" or \
                            self._board[destination_square_location[0] + 1][
                                destination_square_location[1]] == f"{player.get_checker_color()}_king" or \
                            self._board[destination_square_location[0] + 1][destination_square_location[
                                1]] == f"{player.get_checker_color()}_Triple_King" or \
                            self._board[destination_square_location[0] + 2][
                                destination_square_location[1]] is not None:
                        if player.get_checker_color() == "Black":
                            self._black_turn += 1
                            return
                        elif player.get_checker_color() == "White":
                            self._white_turn += 1
                            return

                    else:
                        if player.get_checker_color() == "Black":
                            return "Additional capture"
                        elif player.get_checker_color() == "White":
                            return "Additional capture"

                #check sixth potential move
                if destination_square_location[0] + 2 <= 7 and destination_square_location[1] - 2 >= 0:
                    if self._board[destination_square_location[0] + 1][
                        destination_square_location[1] - 1] is None or \
                            self._board[destination_square_location[0] + 1][
                                destination_square_location[1] - 1] == f"{player.get_checker_color()}" or \
                            self._board[destination_square_location[0] + 1][
                                destination_square_location[1] - 1] == f"{player.get_checker_color()}_king" or \
                            self._board[destination_square_location[0] + 1][
                                destination_square_location[1] - 1] == f"{player.get_checker_color()}_Triple_King" or \
                            self._board[destination_square_location[0] + 2][
                                destination_square_location[1] - 2] is not None:
                        if player.get_checker_color() == "Black":
                            self._black_turn += 1
                            return
                        elif player.get_checker_color() == "White":
                            self._white_turn += 1
                            return

                    else:
                        if player.get_checker_color() == "Black":
                            return "Additional capture"
                        elif player.get_checker_color() == "White":
                            return "Additional capture"
                # if none are true, + 1 turn
                else:
                    if player.get_checker_color() == "Black":
                        self._black_turn += 1

                    elif player.get_checker_color() == "White":
                        self._white_turn += 1


            # king_check_turn() ends here

            # if the piece is a king or triple king, proceed
            if self.get_checker_details(starting_square_location) == f"{player.get_checker_color()}_king" or \
                    self.get_checker_details(starting_square_location) == f"{player.get_checker_color()}_Triple_King":

                # Check first legal position, then proceed
                if starting_square_location[0] - 1 >= 0 and starting_square_location[1] - 1 >= 0:
                    if self._board[starting_square_location[0] - 1][starting_square_location[1] - 1] is not None and \
                            self._board[starting_square_location[0] - 1][starting_square_location[1] - 1] \
                            != f"{player.get_checker_color()}" and \
                            self._board[starting_square_location[0] - 1][starting_square_location[1] - 1] \
                            != f"{player.get_checker_color()}_king" and \
                            self._board[starting_square_location[0] - 1][starting_square_location[1] - 1] \
                            != f"{player.get_checker_color()}_Triple_King":
                        # if the space after enemy square is the destination, capture piece
                        if destination_square_location[0] == starting_square_location[0] - 2 \
                                and destination_square_location[1] == starting_square_location[1] - 2:
                            self._board[starting_square_location[0] - 1][starting_square_location[1] - 1] = None
                            if player.get_checker_color() == "Black":
                                self._black_capture += 1
                            elif player.get_checker_color() == "White":
                                self._white_capture += 1

                            # check if another capture needs to happen. If not, turn +1
                            first_check = king_check_turn()
                            if first_check == "Additional capture":
                                return

                # check second legal position, then proceed
                if starting_square_location[0] - 1 >= 0:
                    if self._board[starting_square_location[0] - 1][starting_square_location[1]] is not None and \
                            self._board[starting_square_location[0] - 1][
                                starting_square_location[1]] != f"{player.get_checker_color()}" and \
                            self._board[starting_square_location[0] - 1][
                                starting_square_location[1]] != f"{player.get_checker_color()}_king" and \
                            self._board[starting_square_location[0] - 1][
                                starting_square_location[1]] != f"{player.get_checker_color()}_Triple_King":
                        # if the space after enemy square is the destination, capture piece
                        if destination_square_location[0] == starting_square_location[0] - 2 and \
                                destination_square_location[1] == starting_square_location[1]:
                            self._board[starting_square_location[0] - 1][starting_square_location[1]] = None
                            if player.get_checker_color() == "Black":
                                self._black_capture += 1
                            elif player.get_checker_color() == "White":
                                self._white_capture += 1

                            # check if another capture needs to happen. If not, turn +1
                            second_check = king_check_turn()
                            if second_check == "Additional capture":
                                return

                            else:
                                if player.get_checker_color() == "Black":
                                    self._black_turn += 1
                                    return
                                elif player.get_checker_color() == "White":
                                    self._white_turn += 1
                                    return

                # check third legal position, then proceed
                if starting_square_location[0] - 1 >= 0 and starting_square_location[1] + 1 <= 7:
                    if self._board[starting_square_location[0] - 1][starting_square_location[1] + 1] is not None and \
                            self._board[starting_square_location[0] - 1][
                                starting_square_location[1] + 1] != f"{player.get_checker_color()}" and \
                            self._board[starting_square_location[0] - 1][
                                starting_square_location[1] + 1] != f"{player.get_checker_color()}_king" and \
                            self._board[starting_square_location[0] - 1][
                                starting_square_location[1] + 1] != f"{player.get_checker_color()}_Triple_King":
                        # if the space after enemy square is the destination, capture piece
                        if destination_square_location[0] == starting_square_location[0] - 2 and \
                                destination_square_location[1] == starting_square_location[1] + 2:
                            self._board[starting_square_location[0] - 1][starting_square_location[1] + 1] = None
                            if player.get_checker_color() == "Black":
                                self._black_capture += 1
                            elif player.get_checker_color() == "White":
                                self._white_capture += 1

                            # check if another capture needs to happen. If not, turn +1
                            third_check = king_check_turn()
                            if third_check == "Additional capture":
                                return

                            else:
                                if player.get_checker_color() == "Black":
                                    self._black_turn += 1
                                    return
                                elif player.get_checker_color() == "White":
                                    self._white_turn += 1
                                    return

                # check fourth legal position, then proceed
                if starting_square_location[0] + 1 <= 7 and starting_square_location[1] + 1 <= 7:
                    if self._board[starting_square_location[0] + 1][starting_square_location[1] + 1] is not None and \
                            self._board[starting_square_location[0] + 1][
                                starting_square_location[1] + 1] != f"{player.get_checker_color()}" and \
                            self._board[starting_square_location[0] + 1][
                                starting_square_location[1] + 1] != f"{player.get_checker_color()}_king" and \
                            self._board[starting_square_location[0] + 1][
                                starting_square_location[1] + 1] != f"{player.get_checker_color()}_Triple_King":
                        # if the space after enemy square is the destination, capture piece
                        if destination_square_location[0] == starting_square_location[0] + 2 and \
                                destination_square_location[1] == starting_square_location[1] + 2:
                            self._board[starting_square_location[0] + 1][starting_square_location[1] + 1] = None
                            if player.get_checker_color() == "Black":
                                self._black_capture += 1

                            elif player.get_checker_color() == "White":
                                self._white_capture += 1

                            # check if another capture needs to happen. If not, turn +1
                            fourth_check = king_check_turn()
                            if fourth_check == "Additional capture":
                                return

                            else:
                                if player.get_checker_color() == "Black":
                                    self._black_turn += 1
                                    return
                                elif player.get_checker_color() == "White":
                                    self._white_turn += 1
                                    return

                # check fifth legal position, then proceed
                if starting_square_location[0] + 1 <= 7:
                    if self._board[starting_square_location[0] + 1][starting_square_location[1]] is not None and \
                            self._board[starting_square_location[0] + 1][
                                starting_square_location[1]] != f"{player.get_checker_color()}" and \
                            self._board[starting_square_location[0] + 1][
                                starting_square_location[1]] != f"{player.get_checker_color()}_king" and \
                            self._board[starting_square_location[0] + 1][
                                starting_square_location[1]] != f"{player.get_checker_color()}_Triple_King":
                        # if the space after enemy square is the destination, capture piece
                        if destination_square_location[0] == starting_square_location[0] + 2 and \
                                destination_square_location[1] == starting_square_location[1]:
                            self._board[starting_square_location[0] + 1][starting_square_location[1]] = None
                            if player.get_checker_color() == "Black":
                                self._black_capture += 1
                            elif player.get_checker_color() == "White":
                                self._white_capture += 1

                            # check if another capture needs to happen. If not, turn +1
                            fifth_check = king_check_turn()
                            if fifth_check == "Additional capture":
                                return

                            else:
                                if player.get_checker_color() == "Black":
                                    self._black_turn += 1
                                    return
                                elif player.get_checker_color() == "White":
                                    self._white_turn += 1
                                    return

                # check last legal position, then proceed
                if starting_square_location[0] + 1 <= 7 and starting_square_location[1] - 1 >= 0:
                    if self._board[starting_square_location[0] + 1][starting_square_location[1] - 1] is not None and \
                            self._board[starting_square_location[0] + 1][
                                starting_square_location[1] - 1] != f"{player.get_checker_color()}" and \
                            self._board[starting_square_location[0] + 1][
                                starting_square_location[1] - 1] != f"{player.get_checker_color()}_king" and \
                            self._board[starting_square_location[0] + 1][
                                starting_square_location[1] - 1] != f"{player.get_checker_color()}_Triple_King":
                        # if the space after enemy square is the destination, capture piece
                        if destination_square_location[0] == starting_square_location[0] + 2 and \
                                destination_square_location[1] == starting_square_location[1] - 2:
                            self._board[starting_square_location[0] + 1][starting_square_location[1] - 1] = None
                            if player.get_checker_color() == "Black":
                                self._black_capture += 1
                            elif player.get_checker_color() == "White":
                                self._white_capture += 1

                            # check if another capture needs to happen. If not, turn +1
                            sixth_check = king_check_turn()
                            if sixth_check == "Additional capture":
                                return

                            else:
                                if player.get_checker_color() == "Black":
                                    self._black_turn += 1
                                    return
                                elif player.get_checker_color() == "White":
                                    self._white_turn += 1
                                    return

                    else:
                        if player.get_checker_color() == "Black":
                            self._black_turn += 1
                            return
                        elif player.get_checker_color() == "White":
                            self._white_turn += 1
                            return

                else:
                    #if there's no capture, + 1 turn
                    if player.get_checker_color() == "Black":
                        self._black_turn += 1
                    elif player.get_checker_color() == "White":
                        self._white_turn += 1


        def triple_king_leap():
            """If the piece is a triple king, it can jump 2 spaces to kill enemies"""
            # Figure out whose turn it is
            if self._player_1.get_player_name() == player_name:
                player = self._player_1

            elif self._player_2.get_player_name() == player_name:
                player = self._player_2

            if self.get_checker_details(starting_square_location) == f"{player.get_checker_color()}_Triple_King":
                pass


        def piece_move():
            """Finally, swap the position of the piece moving and its destination location"""

           # Validate if piece needs to be turned into a King or Triple King
            if destination_square_location[0] == 0:
                if self.get_checker_details(starting_square_location) == "Black":
                    self._board[destination_square_location[0]][destination_square_location[1]] = "Black_king"
                    self._board[starting_square_location[0]][starting_square_location[1]] = None
                elif self.get_checker_details(starting_square_location) == "White_king":
                        self._board[destination_square_location[0]][destination_square_location[1]] = "White_Triple_King"
                        self._board[starting_square_location[0]][starting_square_location[1]] = None

            elif destination_square_location[0] == 7:
                if self.get_checker_details(starting_square_location) == "White":
                    self._board[destination_square_location[0]][destination_square_location[1]] = "White_king"
                    self._board[starting_square_location[0]][starting_square_location[1]] = None
                elif self.get_checker_details(starting_square_location) == "Black_king":
                        self._board[destination_square_location[0]][destination_square_location[1]] = "Black_Triple_King"
                        self._board[starting_square_location[0]][starting_square_location[1]] = None

            else:
                # If it passes the above, swap piece location with destination location.
                self._board[starting_square_location[0]][starting_square_location[1]], \
                    self._board[destination_square_location[0]][destination_square_location[1]] =\
                    self._board[destination_square_location[0]][destination_square_location[1]], \
                    self._board[starting_square_location[0]][starting_square_location[1]]

        in_bounds()
        validate_turn()
        black_standard_capture()
        white_standard_capture()
        king_capture()
        triple_king_leap()
        piece_move()


    def get_checker_details(self, square_location):
        """Returns details of a checker at the specified location. If no checker is present, return None. If black is
            present, return “Black,” if white, return “White.” If kinged, returns format: “Black_king.” If
            triple kinged, returns 'Black_Triple_King.'"""
        location = self._board[square_location[0]][square_location[1]]
        return location

    def get_board(self):
        """Get the board"""
        return self._board


    def print_board(self):
        """Print the current board, with current piece locations, in the form of an array."""
        print(self._board)

    def game_winner(self):
        """Returns the name of the player who won. If it hasn’t ended, returns “Game has not ended.” It will
            not check outcomes based on obscure victory conditions, like blocking all opponent pieces."""
        if self._black_capture == 12:
            if self._player_1.get_checker_color == "Black":
                return self._player_1.get_player_name()

            elif self._player_2.get_checker_color == "Black":
                return self._player._2.get_player_name()

        elif self._white_capture == 12:
            if self._player_1.get_checker_color == "White":
                return self._player_1.get_player_name()

            elif self._player_2.get_checker_color == "White":
                return self._player_2.get_player_name()

        else:
            return "Game has not ended"


class Player:
    """Creates a player object through the Checkers class"""

    def __init__(self, player_name, checker_color, entered_game):
        self._player_name = player_name
        self._checker_color = checker_color
        self._entered_game = entered_game


    def get_checker_color(self):
        """Get the color of the player's pieces"""
        return self._checker_color

    def get_player_name(self):
        """Get the name of the player"""
        return self._player_name


    def get_king_count(self):
        """Returns the number of kings the specified player has."""
        count = 0
        for list in self._entered_game.get_board():
            for element in list:
                if element == f"{self._checker_color}_king":
                    count += 1
        return count

    def get_triple_king_count(self):
        """Returns the number of triple king pieces the player has."""
        count = 0
        for list in self._entered_game.get_board():
            for element in list:
                if element == f"{self._checker_color}_Triple_King":
                    count += 1
        return count


    def get_captured_pieces_count(self):
        """Returns the number of pieces the specified player has captured from the opponent."""
        enemy_pieces_remaining = 0
        if self._checker_color == "Black":
            for list in self._entered_game.get_board():
                for element in list:
                    if element == "White":
                        enemy_pieces_remaining += 1

                    elif element == "White_king":
                        enemy_pieces_remaining += 1

                    elif element == "White_Triple_King":
                        enemy_pieces_remaining += 1

        elif self._checker_color == "White":
            for list in self._entered_game.get_board():
                for element in list:
                    if element == "Black":
                        enemy_pieces_remaining += 1

                    elif element == "Black_king":
                        enemy_pieces_remaining += 1

                    elif element == "Black_Triple_King":
                        enemy_pieces_remaining += 1

        captured_count = (12 - enemy_pieces_remaining)
        return captured_count


def main():
    """Main code that runs when the program is run as a script, but ignored during unit testing"""
    joes_game = Checkers()

    joe = joes_game.create_player("Joe", "White")
    bob = joes_game.create_player("Bob", "Black")
    joes_game.print_board()

    try:
        joes_game.play_game("Bob", (7, 0), (0, 0))
        print(joes_game.get_black_turn())
        joes_game.play_game("Joe", (0, 1), (7, 1))
        print(joes_game.get_white_turn())
        joes_game.play_game("Bob", (0, 0), (7, 0))
        print(joes_game.get_black_turn())
        joes_game.print_board()
        joes_game.play_game("Joe", (7, 1), (0, 1))
        print(joes_game.get_white_turn())

    except OutofTurn:
        print("Error: It is not your turn!")

    except InvalidPlayer:
        print("Error: That player does not exist!")

    except InvalidSquare:
        print("Error: You can't move there!")

    joes_game.print_board()

    print(bob.get_captured_pieces_count())


if __name__ == "__main__":
    main()
