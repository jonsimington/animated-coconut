# This is where you build your AI for the Chess game.

from joueur.base_ai import BaseAI
import random
from .rtanq9_chess import *


class AI(BaseAI):
    """ The basic AI functions that are the same between games. """
    pawn = []
    knight = []
    bishop = []
    rook = []
    queen = []
    king = []
    color = 1 # 1 for White, -1 for Black
    moves = []
    numMoves = 0
    piece_types = [ "Bishop", "Rook", "Knight", "Queen" ]
    # File -> x (a-h)
    # Rank -> y (0-7)

    def valid_move(self, piece, newFile, newRank):
        validPiecesToCapture = [ "p", "b", "r", "n", "q", "k" ]

        type = piece.type
        oldLocation = point(self.fileToInt(piece.file), piece.rank-1)
        newLocation = point(self.fileToInt(newFile), newRank-1)
        _range = (abs(oldLocation.y - newLocation.y) + 1)

        #print("---", piece.id)
        if (not piece.captured):
            #print("Checking (", piece.file, ",", piece.rank, ") -> (", newFile, ",", newRank, "): ", self.moves[self.numMoves].location[newLocation.x][newLocation.y])
            if (type == "Pawn"):
                if (oldLocation == newLocation):
                    return False
                if (piece.file == newFile): # Moving Forward
                    for i in range(1, _range):
                        if (not self.moves[self.numMoves].location[newLocation.x][oldLocation.y + i*self.color] == ""):
                            return False
                    return True
                elif (not piece.file == "h" and self.add_file(piece.file, 1) == newFile): # Capturing a piece
                    #print("Checking jumps... numMoves:", self.numMoves, ", rank:", piece.rank, ", color:", self.color)
                    if (self.moves[self.numMoves].location[newLocation.x][newLocation.y] in validPiecesToCapture or  # Normal Capture
                        (self.numMoves > 0 and ((piece.rank == 4 and self.color == -1) or (piece.rank == 3 and self.color == 1)) and # En Passant
                         self.moves[self.numMoves].location[oldLocation.x + 1][oldLocation.y] == "p" and self.moves[self.numMoves - 1].location[oldLocation.x + 1][oldLocation.y + self.color] == "" and
                         self.moves[self.numMoves - 1].location[oldLocation.x + 1][oldLocation.y] == "" and self.moves[self.numMoves].location[oldLocation.x + 1][oldLocation.y + self.color] == "")):
                        #print("EN PASSANT/Capture")
                        return True
                    else:
                        return False
                elif (not piece.file == "a" and self.add_file(piece.file, -1) == newFile): # Capturing a piece
                    #print("Checking jumps... numMoves:", self.numMoves, ", rank:", piece.rank, ", color:", self.color)
                    if (self.moves[self.numMoves].location[newLocation.x][newLocation.y] in validPiecesToCapture or  # Normal Capture
                        (self.numMoves > 0 and ((piece.rank == 4 and self.color == -1) or (piece.rank == 3 and self.color == 1)) and # En Passant
                         self.moves[self.numMoves].location[oldLocation.x - 1][oldLocation.y] == "p" and self.moves[self.numMoves - 1].location[oldLocation.x - 1][oldLocation.y + self.color] == "" and
                         self.moves[self.numMoves - 1].location[oldLocation.x - 1][oldLocation.y] == "" and self.moves[self.numMoves].location[oldLocation.x - 1][oldLocation.y + self.color] == "")):
                        #print("EN PASSANT/Capture")
                        return True
                    else:
                        return False
        print("False")
        return False

    def fileToInt(self, file = "a"):
        files = [ "a", "b", "c", "d", "e", "f", "g", "h" ]
        return files.index(file)
    def add_file(self, file, amount):
        files = [ "a", "b", "c", "d", "e", "f", "g", "h" ]
        return files[files.index(file) + amount]

    def makeLastMove(self):
        numPieces = len(self.game.pieces)
        self.moves.append(MAP(8, 8)) # The chess board is always always always 8x8
        self.numMoves = len(self.moves) - 1
        for i in range(numPieces):
            if (not self.game.pieces[i].owner.id == self.player.id): # If piece doesn't belong to me
                if (self.game.pieces[i].type == "Pawn"):
                    self.moves[self.numMoves].location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "p"
                elif (self.game.pieces[i].type == "Bishop"):
                    self.moves[self.numMoves].location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "b"
                elif (self.game.pieces[i].type == "Rook"):
                    self.moves[self.numMoves].location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "r"
                elif (self.game.pieces[i].type == "Knight"):
                    self.moves[self.numMoves].location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "n"
                elif (self.game.pieces[i].type == "Queen"):
                    self.moves[self.numMoves].location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "q"
                elif (self.game.pieces[i].type == "King"):
                    self.moves[self.numMoves].location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "k"
            elif (self.game.pieces[i].owner.id == self.player.id): # If piece belongs to me
                if (self.game.pieces[i].type == "Pawn"):
                    self.moves[self.numMoves].location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "P"
                elif (self.game.pieces[i].type == "Bishop"):
                    self.moves[self.numMoves].location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "B"
                elif (self.game.pieces[i].type == "Rook"):
                    self.moves[self.numMoves].location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "R"
                elif (self.game.pieces[i].type == "Knight"):
                    self.moves[self.numMoves].location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "N"
                elif (self.game.pieces[i].type == "Queen"):
                    self.moves[self.numMoves].location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "Q"
                elif (self.game.pieces[i].type == "King"):
                    self.moves[self.numMoves].location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "K"
        #self.moves[self.numMoves].location.reverse()
        print(self.moves[self.numMoves].location)
    def get_name(self):
        """ This is the name you send to the server so your AI will control the
        player named this string.

        Returns
            str: The name of your Player.
        """

        return "RyanAndrews"  # REPLACE THIS WITH YOUR TEAM NAME

    def start(self):
        """ This is called once the game starts and your AI knows its playerID
        and game. You can initialize your AI here.
        """
        numPieces = len(self.game.pieces)
        self.makeLastMove()
        for i in range(numPieces):
            if (self.game.pieces[i].owner.id == self.player.id): # If piece belongs to me
                if (self.game.pieces[i].type == "Pawn"):
                    self.pawn.append(self.game.pieces[i])
                elif (self.game.pieces[i].type == "Bishop"):
                    self.bishop.append(self.game.pieces[i])
                elif (self.game.pieces[i].type == "Rook"):
                    self.rook.append(self.game.pieces[i])
                elif (self.game.pieces[i].type == "Knight"):
                    self.knight.append(self.game.pieces[i])
                elif (self.game.pieces[i].type == "Queen"):
                    self.queen.append(self.game.pieces[i])
                elif (self.game.pieces[i].type == "King"):
                    self.king.append(self.game.pieces[i])
        self.color = self.player.rank_direction

    def game_updated(self):
        """ This is called every time the game's state updates, so if you are
        tracking anything you can update it here.
        """

        # replace with your game updated logic

    def end(self, won, reason):
        """ This is called when the game ends, you can clean up your data and
        dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why you won or
                          lost.
        """

        # replace with your end logic

    def run_turn(self):
        """ This is called every time it is this AI.player's turn.

        Returns:
            bool: Represents if you want to end your turn. True means end your
                  turn, False means to keep your turn going and re-call this
                  function.
        """
        self.makeLastMove()
        # Here is where you'll want to code your AI.

        # We've provided sample code that:
        #    1) prints the board to the console
        #    2) prints the opponent's last move to the console
        #    3) prints how much time remaining this AI has to calculate moves
        #    4) makes a random (and probably invalid) move.

        # 1) print the board to the console
        self.print_current_board()

        # 2) print the opponent's last move to the console
        if len(self.game.moves) > 0:
            print("Opponent's Last Move: '" + self.game.moves[-1].san + "'")

        # 3) print how much time remaining this AI has to calculate moves
        print("Time Remaining: " + str(self.player.time_remaining) + " ns")

        # 4) make a random (and probably invalid) move.
        #random_piece = random.choice(self.player.pieces)
        #random_file = chr(ord("a") + random.randrange(8))
        #random_rank = random.randrange(8) + 1
        #random_piece.move(random_file, random_rank)
        currentPossibleMoves = []

        for i in range(len(self.pawn)): # Check PAWN moves
            if (not self.pawn[i].captured): # If not captured
                if (not self.pawn[i].has_moved): # If hasn't moved from starting position
                    if (self.valid_move(self.pawn[i], self.pawn[i].file, self.pawn[i].rank + 2*self.color)):
                        currentPossibleMoves.append(move(self.moves[self.numMoves], self.pawn[i], i, self.pawn[i].file, self.pawn[i].rank + 2*self.color))
                if (self.valid_move(self.pawn[i], self.pawn[i].file, self.pawn[i].rank + 1*self.color)):
                    currentPossibleMoves.append(move(self.moves[self.numMoves], self.pawn[i], i, self.pawn[i].file, self.pawn[i].rank + 1*self.color))
                if (not self.pawn[i].file == "h" and self.valid_move(self.pawn[i], self.add_file(self.pawn[i].file, 1), self.pawn[i].rank + 1*self.color)):
                    currentPossibleMoves.append(move(self.moves[self.numMoves], self.pawn[i], i, self.add_file(self.pawn[i].file, 1), self.pawn[i].rank + 1*self.color))
                if (not self.pawn[i].file == "a" and self.valid_move(self.pawn[i], self.add_file(self.pawn[i].file, -1), self.pawn[i].rank + 1*self.color)):
                    currentPossibleMoves.append(move(self.moves[self.numMoves], self.pawn[i], i, self.add_file(self.pawn[i].file, -1), self.pawn[i].rank + 1*self.color))

        randomMove = currentPossibleMoves[random.randrange(len(currentPossibleMoves))]
        _move = randomMove.actionObj.move(randomMove.newFile, randomMove.newRank, self.piece_types[random.randrange(len(self.piece_types))])
        if (not _move.promotion == ""):
            if (_move.promotion == "Bishop"):
                self.bishop.append(_move.piece)
            if (_move.promotion == "Rook"):
                self.rook.append(_move.piece)
            if (_move.promotion == "Knight"):
                self.knight.append(_move.piece)
            if (_move.promotion == "Queen"):
                self.queen.append(_move.piece)
            for i in range(len(self.pawn)):
                if (self.pawn[i].id == _move.piece.id):
                    del self.pawn[i]
                    break

        return True  # to signify we are done with our turn.

    def print_current_board(self):
        """Prints the current board using pretty ASCII art
        Note: you can delete this function if you wish
        """

        # iterate through the range in reverse order
        for r in range(9, -2, -1):
            output = ""
            if r == 9 or r == 0:
                # then the top or bottom of the board
                output = "   +------------------------+"
            elif r == -1:
                # then show the ranks
                output = "     a  b  c  d  e  f  g  h"
            else:  # board
                output = " " + str(r) + " |"
                # fill in all the files with pieces at the current rank
                for file_offset in range(0, 8):
                    # start at a, with with file offset increasing the char
                    f = chr(ord("a") + file_offset)
                    current_piece = None
                    for piece in self.game.pieces:
                        if piece.file == f and piece.rank == r:
                            # then we found the piece at (file, rank)
                            current_piece = piece
                            break

                    code = "."  # default "no piece"
                    if current_piece:
                        # the code will be the first character of their type
                        # e.g.  'Q' for "Queen"
                        code = current_piece.type[0]

                        if current_piece.type == "Knight":
                            # 'K' is for "King", we use 'N' for "Knights"
                            code = "N"

                        if current_piece.owner.id == "1":
                            # the second player (black) is lower case.
                            # Otherwise it's uppercase already
                            code = code.lower()

                    output += " " + code + " "

                output += "|"
            print(output)
