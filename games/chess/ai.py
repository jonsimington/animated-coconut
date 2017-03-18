# This is where you build your AI for the Chess game.

from joueur.base_ai import BaseAI #
import random
from .rtanq9_chess import *
from random import shuffle
from copy import deepcopy
from time import sleep

class AI(BaseAI):
    """ The basic AI functions that are the same between games. """
    pawn = []
    enemyPawn = []
    knight = []
    enemyKnight = []
    bishop = []
    enemyBishop = []
    rook = []
    enemyRook = []
    queen = []
    enemyQueen = []
    king = []
    enemyKing = []
    color = 1 # 1 for White, -1 for Black
    moves = []
    myMoves = []
    numMoves = 0
    piece_types = [ "Bishop", "Rook", "Knight", "Queen" ]
    # File -> x (a-h)
    # Rank -> y (0-7)

    def find_check_piece(self, _move):
        kingPos = point(self.fileToInt(self.king[0].file), self.king[0].rank-1)
        if (_move.actionObj.type == "King"):
            kingPos = point(self.fileToInt(_move.newFile), _move.newRank-1)
            if (self.fileToInt(_move.actionObj.file) == kingPos.x + 2 or self.fileToInt(_move.actionObj.file) == kingPos.x - 2):
                return False # Can't castle while in check!

        foundPiece = False
        _piece = point(0, 0)
        myPieces = [ "P", "B", "R", "N", "Q" ]
        diagonal_checks = [ "q", "b" ]
        straight_checks = [ "q", "r" ]
        straight_blocks_nonadjacent = [ "p", "k" ]
        diagonal_blocks_nonadjacent = [ "p", "k" ]
        diagonal_blocks = [ "n", "r" ]
        straight_blocks = [ "n", "b", "p" ]
        topLeft = False
        above = False
        topRight = False
        right = False
        bottomRight = False
        below = False
        bottomLeft = False
        left = False

        distance = 1
        #Start looking in a 3x3 grid around the king, and expand outward until a piece is found that is putting the king in check
        while (not foundPiece and distance < 8):
            for f in range(distance*2 + 1):
                for r in range(distance*2 + 1):
                    if (foundPiece):
                        return True
                    # Top Row
                    if (f == 0 and r == 0 and not topLeft and kingPos.x - distance >= 0 and kingPos.y + distance < 8 and not foundPiece):
                        if (_move.board.location[kingPos.x - distance][kingPos.y + distance] in myPieces or
                            _move.board.location[kingPos.x - distance][kingPos.y + distance] in diagonal_blocks or
                            (_move.board.location[kingPos.x - distance][kingPos.y + distance] in diagonal_blocks_nonadjacent and distance > 1)):
                            topLeft = True
                        elif ((_move.board.location[kingPos.x - 1][kingPos.y + 1] == "p" and distance == 1 and self.color == 1) or
                              (_move.board.location[kingPos.x - 1][kingPos.y + 1] == "k" and distance == 1) or
                                _move.board.location[kingPos.x - distance][kingPos.y + distance] in diagonal_checks):
                            _piece.set(kingPos.x - distance, kingPos.y + distance)
                            foundPiece = True
                            break
                    elif (f == distance and r == 0 and not above and kingPos.y + distance < 8 and not foundPiece):
                        if (_move.board.location[kingPos.x][kingPos.y + distance] in myPieces or
                            _move.board.location[kingPos.x][kingPos.y + distance] in straight_blocks or
                            (_move.board.location[kingPos.x][kingPos.y + distance] in straight_blocks_nonadjacent and distance > 1)):
                            above = True
                        elif ((_move.board.location[kingPos.x][kingPos.y + 1] == "k" and distance == 1) or
                                _move.board.location[kingPos.x][kingPos.y + distance] in straight_checks):
                            _piece.set(kingPos.x, kingPos.y + distance)
                            foundPiece = True
                            break
                    elif (f == distance*2 and r == 0 and not topRight and kingPos.x + distance < 8 and kingPos.y + distance < 8 and not foundPiece):
                        if (_move.board.location[kingPos.x + distance][kingPos.y + distance] in myPieces or
                            _move.board.location[kingPos.x + distance][kingPos.y + distance] in diagonal_blocks or
                            (_move.board.location[kingPos.x + distance][kingPos.y + distance] in diagonal_blocks_nonadjacent and distance > 1)):
                            topRight = True
                        elif ((_move.board.location[kingPos.x + 1][kingPos.y + 1] == "p" and distance == 1 and self.color == 1) or
                              (_move.board.location[kingPos.x + 1][kingPos.y + 1] == "k" and distance == 1) or
                                _move.board.location[kingPos.x + distance][kingPos.y + distance] in diagonal_checks):
                            _piece.set(kingPos.x + distance, kingPos.y + distance)
                            foundPiece = True
                            break
                    # Middle Row
                    elif (f == 0 and r == distance and not left and kingPos.x - distance >= 0 and not foundPiece):
                        if (_move.board.location[kingPos.x - distance][kingPos.y] in myPieces or
                            _move.board.location[kingPos.x - distance][kingPos.y] in straight_blocks or
                            (_move.board.location[kingPos.x - distance][kingPos.y] in straight_blocks_nonadjacent and distance > 1)):
                            left = True
                        elif ((_move.board.location[kingPos.x - 1][kingPos.y] == "k" and distance == 1) or
                                _move.board.location[kingPos.x - distance][kingPos.y] in straight_checks):
                            _piece.set(kingPos.x - distance, kingPos.y - distance)
                            foundPiece = True
                            break
                    elif (f == distance and r == distance and not foundPiece):
                        pass # nothing to do! Since this our kings position...
                    elif (f == distance*2 and r == distance and not right and kingPos.x + distance < 8 and not foundPiece):
                        if (_move.board.location[kingPos.x + distance][kingPos.y] in myPieces or
                            _move.board.location[kingPos.x + distance][kingPos.y] in straight_blocks or
                            (_move.board.location[kingPos.x + distance][kingPos.y] in straight_blocks_nonadjacent and distance > 1)):
                            right = True
                        elif ((_move.board.location[kingPos.x + 1][kingPos.y] == "k" and distance == 1) or
                                _move.board.location[kingPos.x + distance][kingPos.y] in straight_checks):
                            _piece.set(kingPos.x + distance, kingPos.y - distance)
                            foundPiece = True
                            break
                    # Bottom Row
                    elif (f == 0 and r == distance*2 and not bottomLeft and kingPos.x - distance >= 0 and kingPos.y - distance >= 0 and not foundPiece):
                        if (_move.board.location[kingPos.x - distance][kingPos.y - distance] in myPieces or
                            _move.board.location[kingPos.x - distance][kingPos.y - distance] in diagonal_blocks or
                            (_move.board.location[kingPos.x - distance][kingPos.y - distance] in diagonal_blocks_nonadjacent and distance > 1)):
                            bottomLeft = True
                        elif ((_move.board.location[kingPos.x - 1][kingPos.y - 1] == "p" and distance == 1 and self.color == -1) or
                              (_move.board.location[kingPos.x - 1][kingPos.y - 1] == "k" and distance == 1) or
                                _move.board.location[kingPos.x - distance][kingPos.y - distance] in diagonal_checks):
                            _piece.set(kingPos.x - distance, kingPos.y - distance)
                            foundPiece = True
                            break
                    elif (f == distance and r == distance*2 and not below and kingPos.y - distance >= 0 and not foundPiece):
                        if (_move.board.location[kingPos.x][kingPos.y - distance] in myPieces or
                            _move.board.location[kingPos.x][kingPos.y - distance] in straight_blocks or
                            (_move.board.location[kingPos.x][kingPos.y - distance] in straight_blocks_nonadjacent and distance > 1)):
                            below = True
                        elif ((_move.board.location[kingPos.x][kingPos.y - 1] == "k" and distance == 1) or
                                _move.board.location[kingPos.x][kingPos.y - distance] in straight_checks):
                            _piece.set(kingPos.x, kingPos.y - distance)
                            foundPiece = True
                            break
                    elif (f == distance*2 and r == distance*2 and not bottomRight and kingPos.x + distance < 8 and kingPos.y - distance >= 0 and not foundPiece):
                        if (_move.board.location[kingPos.x + distance][kingPos.y - distance] in myPieces or
                            _move.board.location[kingPos.x + distance][kingPos.y - distance] in diagonal_blocks or
                            (_move.board.location[kingPos.x + distance][kingPos.y - distance] in diagonal_blocks_nonadjacent and distance > 1)):
                            bottomRight = True
                        elif ((_move.board.location[kingPos.x + 1][kingPos.y - 1] == "p" and distance == 1 and self.color == -1) or
                              (_move.board.location[kingPos.x + 1][kingPos.y - 1] == "k" and distance == 1) or
                                _move.board.location[kingPos.x + distance][kingPos.y - distance] in diagonal_checks):
                            _piece.set(kingPos.x + distance, kingPos.y - distance)
                            foundPiece = True
                            break
                    # Check For Knights
                    if (distance == 2 and not foundPiece):
                        # Top Row
                        if (f == 1 and r == 0 and kingPos.x - 1 >= 0 and kingPos.y + 2 < 8):
                            if (_move.board.location[kingPos.x - 1][kingPos.y + 2] == "n"):
                                _piece.set(kingPos.x - 1, kingPos.y + 2)
                                foundPiece = True
                                break
                        elif (f == 3 and r == 0 and kingPos.x + 1 < 8 and kingPos.y + 2 < 8):
                            if (_move.board.location[kingPos.x + 1][kingPos.y + 2] == "n"):
                                _piece.set(kingPos.x + 1, kingPos.y + 2)
                                foundPiece = True
                                break
                        # 2nd Row
                        elif (f == 0 and r == 1 and kingPos.x - 2 >= 0 and kingPos.y + 1 < 8):
                            if (_move.board.location[kingPos.x - 2][kingPos.y + 1] == "n"):
                                _piece.set(kingPos.x - 2, kingPos.y + 1)
                                foundPiece = True
                                break
                        elif (f == 4 and r == 1 and kingPos.x + 2 < 8 and kingPos.y + 1 < 8):
                            if (_move.board.location[kingPos.x + 2][kingPos.y + 1] == "n"):
                                _piece.set(kingPos.x + 2, kingPos.y + 1)
                                foundPiece = True
                                break
                        # 4th Row
                        elif (f == 0 and r == 3 and kingPos.x - 2 >= 0 and kingPos.y - 1 >= 0):
                            if (_move.board.location[kingPos.x - 2][kingPos.y - 1] == "n"):
                                _piece.set(kingPos.x - 2, kingPos.y - 1)
                                foundPiece = True
                                break
                        elif (f == 4 and r == 3 and kingPos.x + 2 < 8 and kingPos.y - 1 >= 0):
                            if (_move.board.location[kingPos.x + 2][kingPos.y - 1] == "n"):
                                _piece.set(kingPos.x + 2, kingPos.y - 1)
                                foundPiece = True
                                break
                        # Bottom Row
                        elif (f == 1 and r == 4 and kingPos.x - 1 >= 0 and kingPos.y - 2 >= 0):
                            if (_move.board.location[kingPos.x - 1][kingPos.y - 2] == "n"):
                                _piece.set(kingPos.x - 1, kingPos.y - 2)
                                foundPiece = True
                                break
                        elif (f == 3 and r == 4 and kingPos.x + 1 < 8 and kingPos.y - 2 >= 0):
                            if (_move.board.location[kingPos.x + 1][kingPos.y - 2] == "n"):
                                _piece.set(kingPos.x + 1, kingPos.y - 2)
                                foundPiece = True
                                break
                # END FOR
                if (foundPiece):
                    return True
            # END FOR
            if (foundPiece):
                return True
            distance += 1
        # END WHILE
        
        return foundPiece

    def check_diagonal(self, oldLocation, newLocation, x_dir, y_dir): #
        # x_dir / y_dir / direction
        #   1   /   1   / Up-Right
        #   1   /  -1   / Down-Right
        #  -1   /   1   / Up Left
        #  -1   /  -1   / Down Left
        x_distance = abs(newLocation.x - oldLocation.x)
        validPiecesToCapture = [ "p", "b", "r", "n", "q", "k" ]

        for i in range(1, x_distance):
            if (not self.moves[self.numMoves].location[oldLocation.x + i*x_dir][oldLocation.y + i*y_dir] == ""):
                return False
        if (self.moves[self.numMoves].location[newLocation.x][newLocation.y] in validPiecesToCapture or
            self.moves[self.numMoves].location[newLocation.x][newLocation.y] == ""):
            return True

    def check_horizontal(self, oldLocation, newLocation, x_dir):
        # x_dir / y_dir / direction
        #   1   /   1   / Up-Right
        #   1   /  -1   / Down-Right
        #  -1   /   1   / Up Left
        #  -1   /  -1   / Down Left
        x_distance = abs(newLocation.x - oldLocation.x)
        validPiecesToCapture = [ "p", "b", "r", "n", "q", "k" ]
        for i in range(1, x_distance):
            if (not self.moves[self.numMoves].location[oldLocation.x + i*x_dir][oldLocation.y] == ""):
                return False
        if (self.moves[self.numMoves].location[newLocation.x][newLocation.y] in validPiecesToCapture or
            self.moves[self.numMoves].location[newLocation.x][newLocation.y] == ""):
            return True

    def check_vertical(self, oldLocation, newLocation, y_dir):
        # x_dir / y_dir / direction
        #   1   /   1   / Up-Right
        #   1   /  -1   / Down-Right
        #  -1   /   1   / Up Left
        #  -1   /  -1   / Down Left
        y_distance = abs(newLocation.y - oldLocation.y)
        validPiecesToCapture = [ "p", "b", "r", "n", "q", "k" ]
        for i in range(1, y_distance):
            if (not self.moves[self.numMoves].location[oldLocation.x][oldLocation.y + i*y_dir] == ""):
                return False
        if (self.moves[self.numMoves].location[newLocation.x][newLocation.y] in validPiecesToCapture or
            self.moves[self.numMoves].location[newLocation.x][newLocation.y] == ""):
            return True

    def valid_move(self, piece, newFile, newRank):
        validPiecesToCapture = [ "p", "b", "r", "n", "q", "k" ]
        myPieces = [ "P", "B", "R", "N", "Q", "K" ]

        inCheck = False
        checkPosition = point(0, 0)

        type = piece.type
        oldLocation = point(self.fileToInt(piece.file), piece.rank-1)
        newLocation = point(self.fileToInt(newFile), newRank-1)
        if (oldLocation.x == newLocation.x and oldLocation.y == newLocation.y):
            return False

        y_range = (abs(oldLocation.y - newLocation.y) + 1)
        x_range = (abs(oldLocation.x - newLocation.x) + 1)
        x_distance = (newLocation.x - oldLocation.x)
        y_distance = (newLocation.y - oldLocation.y)

        if (newLocation.x < 0 or newLocation.x > 7 or newLocation.y < 0 or newLocation.y > 7):
            return False

        #print("---", piece.id)
        if (not piece.captured):
            if (type == "Pawn"):
                if (piece.file == newFile and newLocation.y >= 0 and newLocation.y < 8): # Moving Forward
                    if (y_range == 3 and not ((oldLocation.x == 1 and self.color == 1) or (oldLocation.x == 6 and self.color == -1))):
                        return False
                    elif (self.moves[self.numMoves].location[newLocation.x][newLocation.y] == ""):
                        return True
                elif (not piece.file == "h" and self.add_file(piece.file, 1) == newFile): # Capturing a piece
                    if (self.numMoves > 0 and (self.moves[self.numMoves].location[newLocation.x][newLocation.y] in validPiecesToCapture or  # Normal Capture
                        (((piece.rank == 4 and self.color == -1) or (piece.rank == 3 and self.color == 1)) and # En Passant
                         self.moves[self.numMoves].location[oldLocation.x + 1][oldLocation.y] == "p" and self.moves[self.numMoves - 1].location[oldLocation.x + 1][oldLocation.y + self.color] == "" and
                         self.moves[self.numMoves - 1].location[oldLocation.x + 1][oldLocation.y] == "" and self.moves[self.numMoves].location[oldLocation.x + 1][oldLocation.y + self.color] == ""))):
                        return True
                    elif (self.numMoves == 0):
                        _FEN =  self.game.fen.split(" ")
                        if (not _FEN[3] == "-"):
                           # and ((piece.rank == 4 and self.color == -1) or (piece.rank == 3 and self.color == 1)) and # En Passant
                           for i in range(len(_FEN[3])/2):
                               _f = self.fileToInt(_FEN[3][i*2])
                               _r = int(_FEN[3][i*2+1])
                               if (oldLocation.x == _f + 1 or oldLocation.x == _f - 1):
                                   if (oldLocation.y == _r):
                                       print("En Passant Right")
                                       return True
                        else:
                            return False
                elif (not piece.file == "a" and self.add_file(piece.file, -1) == newFile): # Capturing a piece
                    if (self.numMoves > 0 and (self.moves[self.numMoves].location[newLocation.x][newLocation.y] in validPiecesToCapture or  # Normal Capture
                        (((piece.rank == 4 and self.color == -1) or (piece.rank == 3 and self.color == 1)) and # En Passant
                         self.moves[self.numMoves].location[oldLocation.x - 1][oldLocation.y] == "p" and self.moves[self.numMoves - 1].location[oldLocation.x - 1][oldLocation.y + self.color] == "" and
                         self.moves[self.numMoves - 1].location[oldLocation.x - 1][oldLocation.y] == "" and self.moves[self.numMoves].location[oldLocation.x - 1][oldLocation.y + self.color] == ""))):
                        return True
                    elif (self.numMoves == 0):
                        _FEN =  self.game.fen.split(" ")
                        if (not _FEN[3] == "-"):
                           # and ((piece.rank == 4 and self.color == -1) or (piece.rank == 3 and self.color == 1)) and # En Passant
                           for i in range(len(_FEN[3])/2):
                               _f = self.fileToInt(_FEN[3][i*2])
                               _r = int(_FEN[3][i*2+1])
                               if (oldLocation.x == _f + 1 or oldLocation.x == _f - 1):
                                   if (oldLocation.y == _r):
                                       print("En Passant Left")
                                       return True
                        else:
                            return False
            elif (type == "Knight"):
                if (not self.moves[self.numMoves].location[newLocation.x][newLocation.y] in myPieces and 
                    (self.moves[self.numMoves].location[newLocation.x][newLocation.y] in validPiecesToCapture or self.moves[self.numMoves].location[newLocation.x][newLocation.y] == "")):
                    return True
            elif (type == "Bishop"):
                if (newLocation.x >= 0 and newLocation.x < 8 and newLocation.y >= 0 and newLocation.y < 8):
                    if (x_distance > 0 and y_distance < 0): # Bottom Right Move
                        return self.check_diagonal(oldLocation, newLocation, 1, -1)
                    elif (x_distance < 0 and y_distance < 0): # Bottom Left Move
                        return self.check_diagonal(oldLocation, newLocation, -1, -1)
                    elif (x_distance < 0 and y_distance > 0): # Top Left Move
                        return self.check_diagonal(oldLocation, newLocation, -1, 1)
                    elif (x_distance > 0 and y_distance > 0): # Top Right Move
                        return self.check_diagonal(oldLocation, newLocation, 1, 1)
            elif (type == "Rook"):
                if (newLocation.x >= 0 and newLocation.x < 8 and newLocation.y >= 0 and newLocation.y < 8):
                    if (x_distance > 0 and y_distance == 0): # Right Move
                        return self.check_horizontal(oldLocation, newLocation, 1)
                    elif (x_distance < 0 and y_distance == 0): # Left Move
                        return self.check_horizontal(oldLocation, newLocation, -1)
                    elif (y_distance > 0 and x_distance == 0): # Upwards Move
                        return self.check_vertical(oldLocation, newLocation, 1)
                    elif (y_distance < 0 and x_distance == 0): # Downwards Move
                        return self.check_vertical(oldLocation, newLocation, -1)
            elif (type == "Queen"):
                if (newLocation.x >= 0 and newLocation.x < 8 and newLocation.y >= 0 and newLocation.y < 8):
                    x_distance = (newLocation.x - oldLocation.x)
                    y_distance = (newLocation.y - oldLocation.y)
                    if (x_distance > 0 and newLocation.y == oldLocation.y): # Right Move
                        return self.check_horizontal(oldLocation, newLocation, 1)
                    elif (x_distance < 0 and newLocation.y == oldLocation.y): # Left Move
                        return self.check_horizontal(oldLocation, newLocation, -1)
                    elif (y_distance > 0 and newLocation.x == oldLocation.x): # Upwards Move
                        return self.check_vertical(oldLocation, newLocation, 1)
                    elif (y_distance < 0 and newLocation.x == oldLocation.x): # Downwards Move
                        return self.check_vertical(oldLocation, newLocation, -1)
                    elif (x_distance > 0 and y_distance < 0): # Bottom Right Move
                        return self.check_diagonal(oldLocation, newLocation, 1, -1)
                    elif (x_distance < 0 and y_distance < 0): # Bottom Left Move
                        return self.check_diagonal(oldLocation, newLocation, -1, -1)
                    elif (x_distance < 0 and y_distance > 0): # Top Left Move
                        return self.check_diagonal(oldLocation, newLocation, -1, 1)
                    elif (x_distance > 0 and y_distance > 0): # Top Left Move
                        return self.check_diagonal(oldLocation, newLocation, 1, 1)
            elif (type == "King"):
                if (newLocation.x >= 0 and newLocation.x < 8 and newLocation.y >= 0 and newLocation.y < 8):
                    x_distance = (newLocation.x - oldLocation.x)
                    y_distance = (newLocation.y - oldLocation.y)
                    if (newLocation.y == oldLocation.y and  x_distance == 1): # Right Move
                        return self.check_horizontal(oldLocation, newLocation, 1)
                    elif (newLocation.y == oldLocation.y and  x_distance == -1): # Left Move
                        return self.check_horizontal(oldLocation, newLocation, -1)
                    elif (newLocation.x == oldLocation.x and y_distance == 1): # Upwards Move
                        return self.check_vertical(oldLocation, newLocation, 1)
                    elif (newLocation.x == oldLocation.x and y_distance == -1): # Downwards Move
                        return self.check_vertical(oldLocation, newLocation, -1)
                    elif (x_distance == 1 and y_distance == -1): # Bottom Right Move
                        return self.check_diagonal(oldLocation, newLocation, 1, -1)
                    elif (x_distance == -1 and y_distance == -1): # Bottom Left Move
                        return self.check_diagonal(oldLocation, newLocation, -1, -1)
                    elif (x_distance == -1 and y_distance == 1): # Top Left Move
                        return self.check_diagonal(oldLocation, newLocation, -1, 1)
                    elif (x_distance == 1 and y_distance == 1): # Top Right Move
                        return self.check_diagonal(oldLocation, newLocation, 1, 1)
                    elif (x_distance == 2 and y_distance == 0 and ((piece.rank == 0 and self.color == 1) or (piece.rank == 8 and self.color == -1)) and 
                          self.moves[self.numMoves].location[7][newLocation.y] == "R"): # Castling Right
                        for i in range(1, 3):
                            if (not self.moves[self.numMoves].location[oldLocation.x + i][oldLocation.y] == ""):
                                return False
                        return True
                    elif (x_distance == -2 and y_distance == 0 and ((piece.rank == 0 and self.color == 1) or (piece.rank == 8 and self.color == -1)) and 
                          self.moves[self.numMoves].location[0][newLocation.y] == "R"): # Castling Left
                        for i in range(1, 4):
                            if (not self.moves[self.numMoves].location[oldLocation.x - i][oldLocation.y] == ""):
                                return False
                        return True
        return False

    def fileToInt(self, file = "a"):
        files = [ "a", "b", "c", "d", "e", "f", "g", "h" ]
        return files.index(file)
    def intToFile(self, file = "a"):
        files = [ "a", "b", "c", "d", "e", "f", "g", "h" ]
        return files[file]
    def add_file(self, file, amount):
        files = [ "a", "b", "c", "d", "e", "f", "g", "h" ]
        _f = files.index(file)
        if (_f + amount > 7):
            return "h"
        elif (_f + amount < 0):
            return "a"
        else:
            return files[_f + amount]

    def create_move(self, actionObj, actionNum, newFile, newRank):
        newBoard = deepcopy(self.moves[self.numMoves])
        
        enemyPoints = 0
        myPoints = 0

        oldLocation = point(self.fileToInt(actionObj.file), actionObj.rank - 1)
        newLocation = point(self.fileToInt(newFile), newRank - 1)
        capturedPiece = newBoard.location[newLocation.x][newLocation.y]
        newBoard.location[newLocation.x][newLocation.y] = newBoard.location[oldLocation.x][oldLocation.y]
        newBoard.location[oldLocation.x][oldLocation.y] = ""

        enemyPoints = 100*len(self.enemyPawn) + 300*len(self.enemyBishop) + 300*len(self.enemyKnight) + 500*len(self.enemyRook) + 900*len(self.enemyQueen)
        myPoints = 100*len(self.pawn) + 300*len(self.bishop) + 300*len(self.knight) + 500*len(self.rook) + 900*len(self.queen)

        if (capturedPiece == ""):
            myPoints -= 250
        elif (capturedPiece == "P"):
            enemyPoints -= 100
            myPoints += 50
        elif (capturedPiece == "B" or capturedPiece == "N"):
            enemyPoints -= 300
        elif (capturedPiece == "R"):
            enemyPoints -= 500
            myPoints += 250
        elif (capturedPiece == "Q"):
            enemyPoints -= 900
            myPoints += 1000

        if (actionObj.type == "Pawn"):
            if (abs(oldLocation.x - newLocation.x) == 2):
                myPoints += 75
            if ((self.player.rank_direction == -1 and actionObj.rank == 2) or
                (self.player.rank_direction == 1 and actionObj.rank == 7)):
                myPoints += 500
        if (oldLocation.y < 7 and oldLocation.y > 0 and
            newBoard.location[oldLocation.x][oldLocation.y - self.player.rank_direction] == "Q"):
            myPoints -= 350
        if (oldLocation.y < 7 and oldLocation.y > 0 and
            newBoard.location[oldLocation.x][oldLocation.y - self.player.rank_direction] == "K"):
            myPoints -= 800

        #if (len(self.myMoves) > 0 and self.myMoves[len(self.myMoves)-1].actionObj.id == actionObj.id):
        #    myPoints -= 200

        #if (self.numMoves < 12):
        if (actionObj.type == "Pawn"):
            myPoints += random.randrange(20, 50)
            #if (actionObj.type != "Pawn" and (abs(oldLocation.x - newLocation.x) == 1 or abs(oldLocation.y - newLocation.y) == 1)):
            #    myPoints -= 350
        if (actionObj.type == "King"):
            myPoints -= 300
        if (actionObj.type == "Queen"):
            myPoints -= 50

        if (actionObj.type == "Rook" or actionObj.type == "Queen"):
            if (newLocation.y+1 == self.enemyKing[0].rank or self.intToFile(newLocation.x) == self.enemyKing[0].file):
                print(actionObj.type, str(self.intToFile(oldLocation.x)) + str(oldLocation.y+1), "->", str(self.intToFile(newLocation.x)) + str(newLocation.y+1), "in same rank/file as enemy king", ":", self.enemyKing[0].rank, self.enemyKing[0].file)
                myPoints += 300
        if (actionObj.type == "Bishop" or actionObj.type == "Queen"):
            #print(newLocation.x+1, self.enemyKing[0].rank)
            for i in range(8):
                if (newLocation.x+i < 8 and newLocation.y+i < 8):
                    #print(i, actionObj.type, str(self.intToFile(oldLocation.x)) + str(oldLocation.y+1), "->", str(self.intToFile(newLocation.x)) + str(newLocation.y+1), "  ", newLocation.y+1+i, self.enemyKing[0].rank, self.intToFile(newLocation.x+i), self.enemyKing[0].file)
                    if ((newLocation.y+1+i == self.enemyKing[0].rank) and (self.intToFile(newLocation.x+i) == self.enemyKing[0].file)):
                        print(actionObj.type, str(self.intToFile(oldLocation.x)) + str(oldLocation.y+1), "->", str(self.intToFile(newLocation.x)) + str(newLocation.y+1), "possible LOS of enemy king", ":", self.enemyKing[0].rank, self.enemyKing[0].file)
                        myPoints += 100 + 250 if actionObj.type == "Bishop" else 0
                if (newLocation.x+i < 8 and newLocation.y-i >= 0):
                    #print(i, actionObj.type, str(self.intToFile(oldLocation.x)) + str(oldLocation.y+1), "->", str(self.intToFile(newLocation.x)) + str(newLocation.y+1), "  ", newLocation.y+1-i, self.enemyKing[0].rank, self.intToFile(newLocation.x+i), self.enemyKing[0].file)
                    if ((newLocation.y+1-i == self.enemyKing[0].rank) and (self.intToFile(newLocation.x+i) == self.enemyKing[0].file)):
                        print(actionObj.type, str(self.intToFile(oldLocation.x)) + str(oldLocation.y+1), "->", str(self.intToFile(newLocation.x)) + str(newLocation.y+1), "possible LOS of enemy king", ":", self.enemyKing[0].rank, self.enemyKing[0].file)
                        myPoints += 200 + 250 if actionObj.type == "Bishop" else 0
                if (newLocation.x-i >= 0 and newLocation.y-i >= 0):
                    #print(i, actionObj.type, str(self.intToFile(oldLocation.x)) + str(oldLocation.y+1), "->", str(self.intToFile(newLocation.x)) + str(newLocation.y+1), "  ", newLocation.y+1-i, self.enemyKing[0].rank, self.intToFile(newLocation.x-i), self.enemyKing[0].file)
                    if ((newLocation.y+1-i == self.enemyKing[0].rank) and (self.intToFile(newLocation.x-i) == self.enemyKing[0].file)):
                        print(actionObj.type, str(self.intToFile(oldLocation.x)) + str(oldLocation.y+1), "->", str(self.intToFile(newLocation.x)) + str(newLocation.y+1), "possible LOS of enemy king", ":", self.enemyKing[0].rank, self.enemyKing[0].file)
                        myPoints += 200 + 250 if actionObj.type == "Bishop" else 0
                if (newLocation.x-i >= 0 and newLocation.y+i < 8):
                    #print(i, actionObj.type, str(self.intToFile(oldLocation.x)) + str(oldLocation.y+1), "->", str(self.intToFile(newLocation.x)) + str(newLocation.y+1), "  ", newLocation.y+1+i, self.enemyKing[0].rank, self.intToFile(newLocation.x-i), self.enemyKing[0].file)
                    if ((newLocation.y+1+i == self.enemyKing[0].rank) and (self.intToFile(newLocation.x-i) == self.enemyKing[0].file)):
                        print(actionObj.type, str(self.intToFile(oldLocation.x)) + str(oldLocation.y+1), "->", str(self.intToFile(newLocation.x)) + str(newLocation.y+1), "possible LOS of enemy king", ":", self.enemyKing[0].rank, self.enemyKing[0].file)
                        myPoints += 200 + 250 if actionObj.type == "Bishop" else 0

        heuristicValue = myPoints - enemyPoints
        #print(heuristicValue)

        return move(newBoard, actionObj, actionNum, newFile, newRank), heuristicValue

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
        #print(self.moves[self.numMoves].location)

    def getMyMoves(self):
        currentPossibleMoves = pQueue()

        for i in range(len(self.pawn)): # Check PAWN moves
            if (not self.pawn[i].captured): # If not captured
                if (not self.pawn[i].has_moved): # If hasn't moved from starting position
                    if (self.valid_move(self.pawn[i], self.pawn[i].file, self.pawn[i].rank + 2*self.color)):
                        currentPossibleMoves.put(*self.create_move(self.pawn[i], i, self.pawn[i].file, self.pawn[i].rank + 2*self.color))
                if (self.valid_move(self.pawn[i], self.pawn[i].file, self.pawn[i].rank + 1*self.color)):
                    currentPossibleMoves.put(*self.create_move(self.pawn[i], i, self.pawn[i].file, self.pawn[i].rank + 1*self.color))
                if (not self.pawn[i].file == "h" and self.valid_move(self.pawn[i], self.add_file(self.pawn[i].file, 1), self.pawn[i].rank + 1*self.color)):
                    currentPossibleMoves.put(*self.create_move(self.pawn[i], i, self.add_file(self.pawn[i].file, 1), self.pawn[i].rank + 1*self.color))
                if (not self.pawn[i].file == "a" and self.valid_move(self.pawn[i], self.add_file(self.pawn[i].file, -1), self.pawn[i].rank + 1*self.color)):
                    currentPossibleMoves.put(*self.create_move(self.pawn[i], i, self.add_file(self.pawn[i].file, -1), self.pawn[i].rank + 1*self.color))
        for i in range(len(self.knight)): # Check KNIGHT moves
            if (not self.knight[i].captured): # If not captured
                if (not self.knight[i].file == "h" and self.knight[i].rank > 2 and
                    self.valid_move(self.knight[i], self.add_file(self.knight[i].file, 1), self.knight[i].rank - 2)):
                    currentPossibleMoves.put(*self.create_move(self.knight[i], i, self.add_file(self.knight[i].file, 1), self.knight[i].rank - 2))
                if (not self.knight[i].file == "a" and self.knight[i].rank > 2 and
                    self.valid_move(self.knight[i], self.add_file(self.knight[i].file, -1), self.knight[i].rank - 2)):
                    currentPossibleMoves.put(*self.create_move(self.knight[i], i, self.add_file(self.knight[i].file, -1), self.knight[i].rank - 2))
                if (not self.knight[i].file == "a" and not self.knight[i].file == "b" and self.knight[i].rank > 1 and
                    self.valid_move(self.knight[i], self.add_file(self.knight[i].file, -2), self.knight[i].rank - 1)):
                    currentPossibleMoves.put(*self.create_move(self.knight[i], i, self.add_file(self.knight[i].file, -2), self.knight[i].rank - 1))
                if (not self.knight[i].file == "g" and not self.knight[i].file == "h" and self.knight[i].rank > 1 and
                    self.valid_move(self.knight[i], self.add_file(self.knight[i].file, 2), self.knight[i].rank - 1)):
                    currentPossibleMoves.put(*self.create_move(self.knight[i], i, self.add_file(self.knight[i].file, 2), self.knight[i].rank - 1))
                if (not self.knight[i].file == "h" and self.knight[i].rank < 7 and
                    self.valid_move(self.knight[i], self.add_file(self.knight[i].file, 1), self.knight[i].rank + 2)):
                    currentPossibleMoves.put(*self.create_move(self.knight[i], i, self.add_file(self.knight[i].file, 1), self.knight[i].rank + 2))
                if (not self.knight[i].file == "a" and self.knight[i].rank < 7 and
                    self.valid_move(self.knight[i], self.add_file(self.knight[i].file, -1), self.knight[i].rank + 2)):
                    currentPossibleMoves.put(*self.create_move(self.knight[i], i, self.add_file(self.knight[i].file, -1), self.knight[i].rank + 2))
                if (not self.knight[i].file == "a" and not self.knight[i].file == "b" and self.knight[i].rank <= 8 and	
                    self.valid_move(self.knight[i], self.add_file(self.knight[i].file, -2), self.knight[i].rank + 1)):
                    currentPossibleMoves.put(*self.create_move(self.knight[i], i, self.add_file(self.knight[i].file, -2), self.knight[i].rank + 1))
                if (not self.knight[i].file == "g" and not self.knight[i].file == "h" and self.knight[i].rank <= 8 and
                    self.valid_move(self.knight[i], self.add_file(self.knight[i].file, 2), self.knight[i].rank + 1)):
                    currentPossibleMoves.put(*self.create_move(self.knight[i], i, self.add_file(self.knight[i].file, 2), self.knight[i].rank + 1))
        for i in range(len(self.bishop)): # Check BISHOP moves
            if (not self.bishop[i].captured): # If not captured
                for k in range(8):
                    if (self.fileToInt(self.bishop[i].file) + k < 8 and self.bishop[i].rank - k >= 0): # Bottom Right move
                        if (self.valid_move(self.bishop[i], self.add_file(self.bishop[i].file, k), self.bishop[i].rank - k)):
                            currentPossibleMoves.put(*self.create_move(self.bishop[i], i, self.add_file(self.bishop[i].file, k), self.bishop[i].rank - k))
                    if (self.fileToInt(self.bishop[i].file) - k >= 0 and self.bishop[i].rank - k >= 0): # Bottom Left move
                        if (self.valid_move(self.bishop[i], self.add_file(self.bishop[i].file, -k), self.bishop[i].rank - k)):
                            currentPossibleMoves.put(*self.create_move(self.bishop[i], i, self.add_file(self.bishop[i].file, -k), self.bishop[i].rank - k))
                    if (self.fileToInt(self.bishop[i].file) - k >= 0 and self.bishop[i].rank + k <= 8): # Top Left move
                        if (self.valid_move(self.bishop[i], self.add_file(self.bishop[i].file, -k), self.bishop[i].rank + k)):
                            currentPossibleMoves.put(*self.create_move(self.bishop[i], i, self.add_file(self.bishop[i].file, -k), self.bishop[i].rank + k))
                    if (self.fileToInt(self.bishop[i].file) + k < 8 and self.bishop[i].rank + k <= 8): # Top Right move
                        if (self.valid_move(self.bishop[i], self.add_file(self.bishop[i].file, k), self.bishop[i].rank + k)):
                            currentPossibleMoves.put(*self.create_move(self.bishop[i], i, self.add_file(self.bishop[i].file, k), self.bishop[i].rank + k))
        for i in range(len(self.rook)): # Check ROOK moves
            if (not self.rook[i].captured): # If not captured
                for k in range(8):
                    if (self.fileToInt(self.rook[i].file) + k < 8): # Right move
                        if (self.valid_move(self.rook[i], self.add_file(self.rook[i].file, k), self.rook[i].rank)):
                            currentPossibleMoves.put(*self.create_move(self.rook[i], i, self.add_file(self.rook[i].file, k), self.rook[i].rank))
                    if (self.fileToInt(self.rook[i].file) + k >= 0): # Left move
                        if (self.valid_move(self.rook[i], self.add_file(self.rook[i].file, -k), self.rook[i].rank)):
                            currentPossibleMoves.put(*self.create_move(self.rook[i], i, self.add_file(self.rook[i].file, -k), self.rook[i].rank))
                    if (self.rook[i].rank + k <= 8): # Upwards move
                        if (self.valid_move(self.rook[i], self.rook[i].file, self.rook[i].rank + k)):
                            currentPossibleMoves.put(*self.create_move(self.rook[i], i, self.rook[i].file, self.rook[i].rank + k))
                    if (self.rook[i].rank - k >= 0): # Downwards move
                        #print("Rook Down?")
                        if (self.valid_move(self.rook[i], self.rook[i].file, self.rook[i].rank - k)):
                            currentPossibleMoves.put(*self.create_move(self.rook[i], i, self.rook[i].file, self.rook[i].rank - k))
        for i in range(len(self.queen)): # Check QUEEN moves
            if (not self.queen[i].captured): # If not captured
                for k in range(8):
                    if (self.fileToInt(self.queen[i].file) + k < 8 and self.queen[i].rank - k >= 0): # Bottom Right move
                        if (self.valid_move(self.queen[i], self.add_file(self.queen[i].file, k), self.queen[i].rank - k)):
                            currentPossibleMoves.put(*self.create_move(self.queen[i], i, self.add_file(self.queen[i].file, k), self.queen[i].rank - k))
                    if (self.fileToInt(self.queen[i].file) - k >= 0 and self.queen[i].rank - k >= 0): # Bottom Left move
                        if (self.valid_move(self.queen[i], self.add_file(self.queen[i].file, -k), self.queen[i].rank - k)):
                            currentPossibleMoves.put(*self.create_move(self.queen[i], i, self.add_file(self.queen[i].file, -k), self.queen[i].rank - k))
                    if (self.fileToInt(self.queen[i].file) - k >= 0 and self.queen[i].rank + k <= 8): # Top Left move
                        if (self.valid_move(self.queen[i], self.add_file(self.queen[i].file, -k), self.queen[i].rank + k)):
                            currentPossibleMoves.put(*self.create_move(self.queen[i], i, self.add_file(self.queen[i].file, -k), self.queen[i].rank + k))
                    if (self.fileToInt(self.queen[i].file) + k < 8 and self.queen[i].rank + k <= 8): # Top Right move
                        if (self.valid_move(self.queen[i], self.add_file(self.queen[i].file, k), self.queen[i].rank + k)):
                            currentPossibleMoves.put(*self.create_move(self.queen[i], i, self.add_file(self.queen[i].file, k), self.queen[i].rank + k))
                    if (self.fileToInt(self.queen[i].file) + k < 8): # Right move
                        if (self.valid_move(self.queen[i], self.add_file(self.queen[i].file, k), self.queen[i].rank)):
                            currentPossibleMoves.put(*self.create_move(self.queen[i], i, self.add_file(self.queen[i].file, k), self.queen[i].rank))
                    if (self.fileToInt(self.queen[i].file) + k >= 0): # Left move
                        if (self.valid_move(self.queen[i], self.add_file(self.queen[i].file, -k), self.queen[i].rank)):
                            currentPossibleMoves.put(*self.create_move(self.queen[i], i, self.add_file(self.queen[i].file, -k), self.queen[i].rank))
                    if (self.queen[i].rank + k <= 8): # Upwards move
                        if (self.valid_move(self.queen[i], self.queen[i].file, self.queen[i].rank + k)):
                            currentPossibleMoves.put(*self.create_move(self.queen[i], i, self.queen[i].file, self.queen[i].rank + k))
                    if (self.queen[i].rank - k >= 0): # Downwards move
                        if (self.valid_move(self.queen[i], self.queen[i].file, self.queen[i].rank - k)):
                            currentPossibleMoves.put(*self.create_move(self.queen[i], i, self.queen[i].file, self.queen[i].rank - k))
        for i in range(len(self.king)): # Check KING moves
            if (not self.king[0].captured): # If not captured
                if (self.fileToInt(self.king[0].file) + 1 < 8 and self.king[0].rank - 1 >= 0): # Bottom Right move
                    if (self.valid_move(self.king[0], self.add_file(self.king[0].file, 1), self.king[0].rank - 1)):
                        currentPossibleMoves.put(*self.create_move(self.king[0], 0, self.add_file(self.king[0].file, 1), self.king[0].rank - 1))
                if (self.fileToInt(self.king[0].file) - 1 >= 0 and self.king[0].rank - 1 >= 0): # Bottom Left move
                    if (self.valid_move(self.king[0], self.add_file(self.king[0].file, -1), self.king[0].rank - 1)):
                        currentPossibleMoves.put(*self.create_move(self.king[0], 0, self.add_file(self.king[0].file, -1), self.king[0].rank - 1))
                if (self.fileToInt(self.king[0].file) - 1 >= 0 and self.king[0].rank + 1 <= 8): # Top Left move
                    if (self.valid_move(self.king[0], self.add_file(self.king[0].file, -1), self.king[0].rank + 1)):
                        currentPossibleMoves.put(*self.create_move(self.king[0], 0, self.add_file(self.king[0].file, -1), self.king[0].rank + 1))
                if (self.fileToInt(self.king[0].file) + 1 < 8 and self.king[0].rank + 1 <= 8): # Top Right move
                    if (self.valid_move(self.king[0], self.add_file(self.king[0].file, 1), self.king[0].rank + 1)):
                        currentPossibleMoves.put(*self.create_move(self.king[0], 0, self.add_file(self.king[0].file, 1), self.king[0].rank + 1))
                if (self.fileToInt(self.king[0].file) + 1 < 8): # Right move
                    if (self.valid_move(self.king[0], self.add_file(self.king[0].file, 1), self.king[0].rank)):
                        currentPossibleMoves.put(*self.create_move(self.king[0], 0, self.add_file(self.king[0].file, 1), self.king[0].rank))
                if (self.fileToInt(self.king[0].file) - 1 >= 0): # Left move
                    if (self.valid_move(self.king[0], self.add_file(self.king[0].file, -1), self.king[0].rank)):
                        currentPossibleMoves.put(*self.create_move(self.king[0], 0, self.add_file(self.king[0].file, -1), self.king[0].rank))
                if (self.king[0].rank + 1 <= 8): # Upwards move
                    if (self.valid_move(self.king[0], self.king[0].file, self.king[0].rank + 1)):
                        currentPossibleMoves.put(*self.create_move(self.king[0], 0, self.king[0].file, self.king[0].rank + 1))
                if (self.king[0].rank - 1 >= 0): # Downwards move
                    if (self.valid_move(self.king[0], self.king[0].file, self.king[0].rank - 1)):
                        currentPossibleMoves.put(*self.create_move(self.king[0], 0, self.king[0].file, self.king[0].rank - 1))
                # CASTLING
                if (not self.king[0].has_moved):
                    for i in range(0, len(self.rook)):
                        if (not self.rook[i].has_moved and not self.rook[i].captured):
                            if (self.fileToInt(self.rook[i].file) > self.fileToInt(self.king[0].file)):
                                if (self.valid_move(self.king[0], self.add_file(self.king[0].file, 2), self.king[0].rank)):
                                    currentPossibleMoves.put(*self.create_move(self.king[0], 0, self.add_file(self.king[0].file, 2), self.king[0].rank))
                            elif (self.fileToInt(self.rook[i].file) < self.fileToInt(self.king[0].file)):
                                if (self.valid_move(self.king[0], self.add_file(self.king[0].file, -2), self.king[0].rank)):
                                    currentPossibleMoves.put(*self.create_move(self.king[0], 0, self.add_file(self.king[0].file, -2), self.king[0].rank))
        return currentPossibleMoves

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
            else: # If piece doesn't belong to me
                if (self.game.pieces[i].type == "Pawn"):
                    self.enemyPawn.append(self.game.pieces[i])
                elif (self.game.pieces[i].type == "Bishop"):
                    self.enemyBishop.append(self.game.pieces[i])
                elif (self.game.pieces[i].type == "Rook"):
                    self.enemyRook.append(self.game.pieces[i])
                elif (self.game.pieces[i].type == "Knight"):
                    self.enemyKnight.append(self.game.pieces[i])
                elif (self.game.pieces[i].type == "Queen"):
                    self.enemyQueen.append(self.game.pieces[i])
                elif (self.game.pieces[i].type == "King"):
                    self.enemyKing.append(self.game.pieces[i])
        self.color = self.player.rank_direction

    def game_updated(self):
        """ This is called every time the game's state updates, so if you are
        tracking anything you can update it here.
        """
        capturedPiece = False

        if (not capturedPiece):
            for i in range(len(self.pawn)):
                if (self.pawn[i].captured):
                    del self.pawn[i]
                    capturedPiece = True
                    break
        if (not capturedPiece):
            for i in range(len(self.bishop)):
                if (self.bishop[i].captured):
                    del self.bishop[i]
                    capturedPiece = True
                    break
        if (not capturedPiece):
            for i in range(len(self.rook)):
                if (self.rook[i].captured):
                    del self.rook[i]
                    capturedPiece = True
                    break
        if (not capturedPiece):
            for i in range(len(self.knight)):
                if (self.knight[i].captured):
                    del self.knight[i]
                    capturedPiece = True
                    break
        if (not capturedPiece):
            for i in range(len(self.queen)):
                if (self.queen[i].captured):
                    del self.queen[i]
                    capturedPiece = True
                    break

        if (not capturedPiece):
            for i in range(len(self.enemyPawn)):
                if (self.enemyPawn[i].captured):
                    del self.enemyPawn[i]
                    capturedPiece = True
                    break
        if (not capturedPiece):
            for i in range(len(self.enemyBishop)):
                if (self.enemyBishop[i].captured):
                    del self.enemyBishop[i]
                    capturedPiece = True
                    break
        if (not capturedPiece):
            for i in range(len(self.enemyRook)):
                if (self.enemyRook[i].captured):
                    del self.enemyRook[i]
                    capturedPiece = True
                    break
        if (not capturedPiece):
            for i in range(len(self.enemyKnight)):
                if (self.enemyKnight[i].captured):
                    del self.enemyKnight[i]
                    capturedPiece = True
                    break
        if (not capturedPiece):
            for i in range(len(self.enemyQueen)):
                if (self.enemyQueen[i].captured):
                    del self.enemyQueen[i]
                    capturedPiece = True
                    break

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
        #if len(self.game.moves) > 0:
            #print("Opponent's Last Move: ", self.game.moves[-1].piece.type, "'", self.game.moves[-1].to_file, self.game.moves[-1].to_rank, "'")

        # 3) print how much time remaining this AI has to calculate moves
        #print("Time Remaining: " + str(self.player.time_remaining) + " ns")

        # 4) make a random (and probably invalid) move.
        #random_piece = random.choice(self.player.pieces)
        #random_file = chr(ord("a") + random.randrange(8))
        #random_rank = random.randrange(8) + 1
        #random_piece.move(random_file, random_rank)
        currentPossibleMoves = pQueue()
        currentPossibleMoves = self.getMyMoves()
        
        if (self.player.in_check):
            print("In Check...")

        bestMove, bestPriority = currentPossibleMoves.pop_back()
        while (self.find_check_piece(bestMove)):
            bestMove, bestPriority = currentPossibleMoves.pop_back()

        #promotion = getPromotionType() # DEFINE THIS!
        _move = bestMove.actionObj.move(bestMove.newFile, bestMove.newRank, self.piece_types[random.randrange(len(self.piece_types))])
        self.myMoves.append(bestMove)
        print("Moving", bestMove.actionObj.type, "#" + str(bestMove.actionObj.id), "to '" + str(bestMove.newFile) + str(bestMove.newRank) + "', with priority", bestPriority)

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
        #_files = [ "1", "b", "c", "d", "e", "f", "g", "h" ] _files[f]
        print("Black" if self.color == -1 else "White")
        print("  +------------------------+")
        # iterate through the range in reverse order
        for f in range(7, -1, -1):
            print(f+1, "|", end="")
            for r in range(8):
                if (not self.moves[self.numMoves].location[r][f] == ""):
                    print("", self.moves[self.numMoves].location[r][f], end=" ")
                else:
                    print(" . ", end="")
            print("|")
        print("  +------------------------+")
        print("    a  b  c  d  e  f  g  h <- FILES")
