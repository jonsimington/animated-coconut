# This is where you build your AI for the Chess game.

from joueur.base_ai import BaseAI #
import random
from .rtanq9_chess import *
from random import shuffle
from copy import deepcopy
from time import sleep
import time
import math

class AI(BaseAI):
    """ The basic AI functions that are the same between games. """
    chessBoard = []
    enemyBoard = []

    AVERAGE_MOVES = 40 # Average number of moves in a game of chess

    color = 1 # 1 for White, -1 for Black

    piece_types = ["Bishop", "Rook", "Knight", "Queen"]
    # File -> x (a-h)
    # Rank -> y (0-7)

    def find_check_piece(self, _chessBoard, MinimaxTurn):
        if (MinimaxTurn > 0):
            kingPos = point(self.fileToInt(_chessBoard.king[0].file), _chessBoard.king[0].rank - 1)
        else:
            kingPos = point(self.fileToInt(_chessBoard.enemyKing[0].file), _chessBoard.enemyKing[0].rank - 1)
        if (_chessBoard.currentMove.actionObj.type == "King"):
            kingPos = point(self.fileToInt(_chessBoard.currentMove.newFile), _chessBoard.currentMove.newRank - 1)
            if (self.fileToInt(_chessBoard.currentMove.actionObj.file) == kingPos.x + 2 or self.fileToInt(_chessBoard.currentMove.actionObj.file) == kingPos.x - 2):
                return False, point(0, 0) # Can't castle while in check!

        foundPiece = False
        _piece = point(0, 0)
        MinimaxColor = MinimaxTurn * self.color

        myPieces = ["P", "B", "R", "N", "Q", "K"] if MinimaxTurn > 0 else ["p", "b", "r", "n", "q", "K"]
        diagonal_checks = ["q", "b"] if MinimaxTurn > 0 else ["Q", "B"]
        straight_checks = ["q", "r"] if MinimaxTurn > 0 else ["Q", "R"]
        straight_blocks_nonadjacent = ["p", "k"] if MinimaxTurn > 0 else ["P", "K"]
        diagonal_blocks_nonadjacent = ["p", "k"] if MinimaxTurn > 0 else ["P", "K"]
        diagonal_blocks = ["n", "r"] if MinimaxTurn > 0 else ["N", "R"]
        straight_blocks = ["n", "b", "p"] if MinimaxTurn > 0 else ["N", "B", "P"]
        pawn = "p" if MinimaxTurn > 0 else "P"
        knight = "n" if MinimaxTurn > 0 else "N"
        king = "k" if MinimaxTurn > 0 else "K"
        topLeft = False
        above = False
        topRight = False
        right = False
        bottomRight = False
        below = False
        bottomLeft = False
        left = False

        distance = 1
        #Start looking in a 3x3 grid around the king, and expand outward until
        #a piece is found that is putting the king in check
        while (not foundPiece and distance < 8):
            for f in range(distance * 2 + 1):
                for r in range(distance * 2 + 1):
                    if (foundPiece):
                        return True, _piece
                    # Top Row
                    if (not topLeft and f == 0 and r == 0 and kingPos.x - distance >= 0 and kingPos.y + distance < 8 and not foundPiece):
                        if (_chessBoard.board.location[kingPos.x - distance][kingPos.y + distance] in myPieces or
                            _chessBoard.board.location[kingPos.x - distance][kingPos.y + distance] in diagonal_blocks or
                            (_chessBoard.board.location[kingPos.x - distance][kingPos.y + distance] in diagonal_blocks_nonadjacent and distance > 1)):
                            topLeft = True
                        elif ((_chessBoard.board.location[kingPos.x - 1][kingPos.y + 1] == pawn and distance == 1 and MinimaxColor > 0) or
                              (_chessBoard.board.location[kingPos.x - 1][kingPos.y + 1] == king and distance == 1) or
                              _chessBoard.board.location[kingPos.x - distance][kingPos.y + distance] in diagonal_checks):
                            _piece.set(kingPos.x - distance, kingPos.y + distance)
                            foundPiece = True
                            break
                    elif (not above and f == distance and r == 0 and kingPos.y + distance < 8 and not foundPiece):
                        if (_chessBoard.board.location[kingPos.x][kingPos.y + distance] in myPieces or
                            _chessBoard.board.location[kingPos.x][kingPos.y + distance] in straight_blocks or
                            (_chessBoard.board.location[kingPos.x][kingPos.y + distance] in straight_blocks_nonadjacent and distance > 1)):
                            above = True
                        elif (_chessBoard.board.location[kingPos.x][kingPos.y + distance] in straight_checks or
                              (_chessBoard.board.location[kingPos.x][kingPos.y + 1] == king and distance == 1)):
                            _piece.set(kingPos.x, kingPos.y + distance)
                            foundPiece = True
                            break
                    elif (not topRight and f == distance * 2 and r == 0 and kingPos.x + distance < 8 and kingPos.y + distance < 8 and not foundPiece):
                        if (_chessBoard.board.location[kingPos.x + distance][kingPos.y + distance] in myPieces or
                            _chessBoard.board.location[kingPos.x + distance][kingPos.y + distance] in diagonal_blocks or
                            (_chessBoard.board.location[kingPos.x + distance][kingPos.y + distance] in diagonal_blocks_nonadjacent and distance > 1)):
                            topRight = True
                        elif ((_chessBoard.board.location[kingPos.x + 1][kingPos.y + 1] == pawn and distance == 1 and MinimaxColor > 0) or
                              (_chessBoard.board.location[kingPos.x + 1][kingPos.y + 1] == king and distance == 1) or
                              _chessBoard.board.location[kingPos.x + distance][kingPos.y + distance] in diagonal_checks):
                            _piece.set(kingPos.x + distance, kingPos.y + distance)
                            foundPiece = True
                            break
                    # Middle Row
                    elif (not left and f == 0 and r == distance and kingPos.x - distance >= 0 and not foundPiece):
                        if (_chessBoard.board.location[kingPos.x - distance][kingPos.y] in myPieces or
                            _chessBoard.board.location[kingPos.x - distance][kingPos.y] in straight_blocks or
                            (_chessBoard.board.location[kingPos.x - distance][kingPos.y] in straight_blocks_nonadjacent and distance > 1)):
                            left = True
                        elif (_chessBoard.board.location[kingPos.x - distance][kingPos.y] in straight_checks or
                              (_chessBoard.board.location[kingPos.x - 1][kingPos.y] == king and distance == 1)):
                            _piece.set(kingPos.x - distance, kingPos.y)
                            foundPiece = True
                            break
                    elif (f == distance and r == distance and not foundPiece):
                        pass # nothing to do!  Since this our kings position...
                    elif (not right and f == distance * 2 and r == distance and kingPos.x + distance < 8 and not foundPiece):
                        if (_chessBoard.board.location[kingPos.x + distance][kingPos.y] in myPieces or
                            _chessBoard.board.location[kingPos.x + distance][kingPos.y] in straight_blocks or
                            (_chessBoard.board.location[kingPos.x + distance][kingPos.y] in straight_blocks_nonadjacent and distance > 1)):
                            right = True
                        elif (_chessBoard.board.location[kingPos.x + distance][kingPos.y] in straight_checks or
                              (_chessBoard.board.location[kingPos.x + 1][kingPos.y] == king and distance == 1)):
                            _piece.set(kingPos.x + distance, kingPos.y)
                            foundPiece = True
                            break
                    # Bottom Row
                    elif (not bottomLeft and f == 0 and r == distance * 2 and kingPos.x - distance >= 0 and kingPos.y - distance >= 0 and not foundPiece):
                        if (_chessBoard.board.location[kingPos.x - distance][kingPos.y - distance] in myPieces or
                            _chessBoard.board.location[kingPos.x - distance][kingPos.y - distance] in diagonal_blocks or
                            (_chessBoard.board.location[kingPos.x - distance][kingPos.y - distance] in diagonal_blocks_nonadjacent and distance > 1)):
                            bottomLeft = True
                        elif ((_chessBoard.board.location[kingPos.x - 1][kingPos.y - 1] == pawn and distance == 1 and MinimaxColor < 0) or
                              (_chessBoard.board.location[kingPos.x - 1][kingPos.y - 1] == king and distance == 1) or
                              _chessBoard.board.location[kingPos.x - distance][kingPos.y - distance] in diagonal_checks):
                            _piece.set(kingPos.x - distance, kingPos.y - distance)
                            foundPiece = True
                            break
                    elif (not below and f == distance and r == distance * 2 and kingPos.y - distance >= 0 and not foundPiece):
                        if (_chessBoard.board.location[kingPos.x][kingPos.y - distance] in myPieces or
                            _chessBoard.board.location[kingPos.x][kingPos.y - distance] in straight_blocks or
                            (_chessBoard.board.location[kingPos.x][kingPos.y - distance] in straight_blocks_nonadjacent and distance > 1)):
                            below = True
                        elif (_chessBoard.board.location[kingPos.x][kingPos.y - distance] in straight_checks or
                              (_chessBoard.board.location[kingPos.x][kingPos.y - 1] == king and distance == 1)):
                            _piece.set(kingPos.x, kingPos.y - distance)
                            foundPiece = True
                            break
                    elif (not bottomRight and f == distance * 2 and r == distance * 2 and kingPos.x + distance < 8 and kingPos.y - distance >= 0 and not foundPiece):
                        if (_chessBoard.board.location[kingPos.x + distance][kingPos.y - distance] in myPieces or
                            _chessBoard.board.location[kingPos.x + distance][kingPos.y - distance] in diagonal_blocks or
                            (_chessBoard.board.location[kingPos.x + distance][kingPos.y - distance] in diagonal_blocks_nonadjacent and distance > 1)):
                            bottomRight = True
                        elif ((_chessBoard.board.location[kingPos.x + 1][kingPos.y - 1] == pawn and distance == 1 and MinimaxColor < 0) or
                              (_chessBoard.board.location[kingPos.x + 1][kingPos.y - 1] == king and distance == 1) or
                              _chessBoard.board.location[kingPos.x + distance][kingPos.y - distance] in diagonal_checks):
                            _piece.set(kingPos.x + distance, kingPos.y - distance)
                            foundPiece = True
                            break
                    # Check For Knights
                    if (distance == 2 and not foundPiece):
                        # Top Row
                        if (f == 1 and r == 0 and kingPos.x - 1 >= 0 and kingPos.y + 2 < 8):
                            if (_chessBoard.board.location[kingPos.x - 1][kingPos.y + 2] == knight):
                                _piece.set(kingPos.x - 1, kingPos.y + 2)
                                foundPiece = True
                                break
                        elif (f == 3 and r == 0 and kingPos.x + 1 < 8 and kingPos.y + 2 < 8):
                            if (_chessBoard.board.location[kingPos.x + 1][kingPos.y + 2] == knight):
                                _piece.set(kingPos.x + 1, kingPos.y + 2)
                                foundPiece = True
                                break
                        # 2nd Row
                        elif (f == 0 and r == 1 and kingPos.x - 2 >= 0 and kingPos.y + 1 < 8):
                            if (_chessBoard.board.location[kingPos.x - 2][kingPos.y + 1] == knight):
                                _piece.set(kingPos.x - 2, kingPos.y + 1)
                                foundPiece = True
                                break
                        elif (f == 4 and r == 1 and kingPos.x + 2 < 8 and kingPos.y + 1 < 8):
                            if (_chessBoard.board.location[kingPos.x + 2][kingPos.y + 1] == knight):
                                _piece.set(kingPos.x + 2, kingPos.y + 1)
                                foundPiece = True
                                break
                        # 4th Row
                        elif (f == 0 and r == 3 and kingPos.x - 2 >= 0 and kingPos.y - 1 >= 0):
                            if (_chessBoard.board.location[kingPos.x - 2][kingPos.y - 1] == knight):
                                _piece.set(kingPos.x - 2, kingPos.y - 1)
                                foundPiece = True
                                break
                        elif (f == 4 and r == 3 and kingPos.x + 2 < 8 and kingPos.y - 1 >= 0):
                            if (_chessBoard.board.location[kingPos.x + 2][kingPos.y - 1] == knight):
                                _piece.set(kingPos.x + 2, kingPos.y - 1)
                                foundPiece = True
                                break
                        # Bottom Row
                        elif (f == 1 and r == 4 and kingPos.x - 1 >= 0 and kingPos.y - 2 >= 0):
                            if (_chessBoard.board.location[kingPos.x - 1][kingPos.y - 2] == knight):
                                _piece.set(kingPos.x - 1, kingPos.y - 2)
                                foundPiece = True
                                break
                        elif (f == 3 and r == 4 and kingPos.x + 1 < 8 and kingPos.y - 2 >= 0):
                            if (_chessBoard.board.location[kingPos.x + 1][kingPos.y - 2] == knight):
                                _piece.set(kingPos.x + 1, kingPos.y - 2)
                                foundPiece = True
                                break
                # END FOR
                if (foundPiece):
                    return True, _piece
            # END FOR
            if (foundPiece):
                return True, _piece
            distance += 1
        # END WHILE

        return foundPiece, _piece

    def check_diagonal(self, _chessBoard, oldLocation, newLocation, x_dir, y_dir): #
        # x_dir / y_dir / direction
        #   1 / 1 / Up-Right
                                                                                          #   1 / -1 / Down-Right
        #  -1 / 1 / Up Left
                                                                                          #  -1 / -1 / Down Left
        x_distance = abs(newLocation.x - oldLocation.x)
        validPiecesToCapture = ["p", "b", "r", "n", "q", "k"]

        for i in range(1, x_distance):
            if (not _chessBoard.board.location[oldLocation.x + i * x_dir][oldLocation.y + i * y_dir] == ""):
                return False
        if (_chessBoard.board.location[newLocation.x][newLocation.y] in validPiecesToCapture or _chessBoard.board.location[newLocation.x][newLocation.y] == ""):
            return True

    def check_horizontal(self, _chessBoard, oldLocation, newLocation, x_dir):
        # x_dir / y_dir / direction
        #   1 / 1 / Up-Right
        #   1 / -1 / Down-Right
        #  -1 / 1 / Up Left
        #  -1 / -1 / Down Left
        x_distance = abs(newLocation.x - oldLocation.x)
        validPiecesToCapture = ["p", "b", "r", "n", "q", "k"]
        for i in range(1, x_distance):
            if (not _chessBoard.board.location[oldLocation.x + i * x_dir][oldLocation.y] == ""):
                return False
        if (_chessBoard.board.location[newLocation.x][newLocation.y] in validPiecesToCapture or _chessBoard.board.location[newLocation.x][newLocation.y] == ""):
            return True

    def check_vertical(self, _chessBoard, oldLocation, newLocation, y_dir):
        # x_dir / y_dir / direction
        #   1 / 1 / Up-Right
        #   1 / -1 / Down-Right
        #  -1 / 1 / Up Left
        #  -1 / -1 / Down Left
        y_distance = abs(newLocation.y - oldLocation.y)
        validPiecesToCapture = ["p", "b", "r", "n", "q", "k"]
        for i in range(1, y_distance):
            if (not _chessBoard.board.location[oldLocation.x][oldLocation.y + i * y_dir] == ""):
                return False
        if (_chessBoard.board.location[newLocation.x][newLocation.y] in validPiecesToCapture or _chessBoard.board.location[newLocation.x][newLocation.y] == ""):
            return True

    def valid_move(self, piece, newFile, newRank, _chessBoard, MinimaxTurn):
        validPiecesToCapture = ["p", "b", "r", "n", "q", "k"] if MinimaxTurn > 0 else ["P", "B", "R", "N", "Q", "K"]
        myPieces = ["P", "B", "R", "N", "Q", "K"] if MinimaxTurn > 0 else ["p", "b", "r", "n", "q", "k"]

        myMoveDirection = MinimaxTurn * self.player.rank_direction
        inCheck = False
        checkPosition = point(0, 0)

        type = piece.type
        oldLocation = point(self.fileToInt(piece.file), piece.rank - 1)
        newLocation = point(self.fileToInt(newFile), newRank - 1)
        if (oldLocation.x == newLocation.x and oldLocation.y == newLocation.y):
            return False

        y_range = (abs(oldLocation.y - newLocation.y) + 1)
        x_range = (abs(oldLocation.x - newLocation.x) + 1)
        x_distance = (newLocation.x - oldLocation.x)
        y_distance = (newLocation.y - oldLocation.y)

        if (newLocation.x < 0 or newLocation.x > 7 or newLocation.y < 0 or newLocation.y > 7):
            return False

        currentMove = move(piece, 0, newFile, newRank)
        newBoard = chessBoard(_chessBoard, currentMove, False if MinimaxTurn > 0 else True)

        oldLocation = point(self.fileToInt(piece.file), piece.rank - 1)
        newLocation = point(self.fileToInt(newFile), newRank - 1)

        capturedPiece = newBoard.board.location[newLocation.x][newLocation.y]
        newBoard.board.location[newLocation.x][newLocation.y] = newBoard.board.location[oldLocation.x][oldLocation.y]
        newBoard.board.location[oldLocation.x][oldLocation.y] = ""

        foundPiece, _piecePoint = self.find_check_piece(newBoard, MinimaxTurn)
        if (foundPiece == True):
            #print("Found Piece", _chessBoard.board.location[_piecePoint.x][_piecePoint.y],"at:", _piecePoint.x, _piecePoint.y, ". Moving", piece.type, "to", newFile, newRank)
            return False

        if (not piece.actual_piece.captured):
            if (type == "Pawn"):
                if (piece.file == newFile and newLocation.y >= 0 and newLocation.y < 8): # Moving Forward 2 Spaces
                    if (y_range == 3 and not ((oldLocation.y == 1 and self.color == MinimaxTurn) or (oldLocation.y == 6 and self.color == -MinimaxTurn))):
                        return False
                    elif (_chessBoard.board.location[newLocation.x][newLocation.y] == ""):
                        return True
                if (piece.file == newFile and newLocation.y >= 0 and newLocation.y < 8): # Moving Forward 1 Space
                    if (not y_range == 2):
                        return False
                    elif (_chessBoard.board.location[newLocation.x][newLocation.y] == ""):
                        return True
                elif (not piece.file == "h" and self.add_file(piece.file, 1) == newFile and piece.rank + myMoveDirection == newRank): # Capturing a piece to the right
                    if (_chessBoard.board.location[newLocation.x][newLocation.y] in validPiecesToCapture):
                        return True
                    else: #En Passant
                        _FEN = self.game.fen.split(" ")
                        if (not _FEN[3] == "-"):
                           for i in range(int(len(_FEN[3]) / 2)):
                               _f = self.fileToInt(_FEN[3][i * 2])
                               _r = int(_FEN[3][i * 2 + 1])
                               if (oldLocation.x == _f + 1 or oldLocation.x == _f - 1):
                                   if (oldLocation.y == _r):
                                       return True
                        else:
                            return False
                elif (not piece.file == "a" and self.add_file(piece.file, -1) == newFile and piece.rank + myMoveDirection == newRank): # Capturing a piece to the left
                    if (_chessBoard.board.location[newLocation.x][newLocation.y] in validPiecesToCapture):
                        return True
                    else: #En Passant
                        _FEN = self.game.fen.split(" ")
                        if (not _FEN[3] == "-"):
                           for i in range(int(len(_FEN[3]) / 2)):
                               _f = self.fileToInt(_FEN[3][i * 2])
                               _r = int(_FEN[3][i * 2 + 1])
                               if (oldLocation.x == _f + 1 or oldLocation.x == _f - 1):
                                   if (oldLocation.y == _r):
                                       return True
                        else:
                            return False
            elif (type == "Knight"):
                if (not _chessBoard.board.location[newLocation.x][newLocation.y] in myPieces and (_chessBoard.board.location[newLocation.x][newLocation.y] in validPiecesToCapture or _chessBoard.board.location[newLocation.x][newLocation.y] == "")):
                    return True
            elif (type == "Bishop"):
                if (newLocation.x >= 0 and newLocation.x < 8 and newLocation.y >= 0 and newLocation.y < 8):
                    if (x_distance > 0 and y_distance < 0): # Bottom Right Move
                        return self.check_diagonal(_chessBoard, oldLocation, newLocation, 1, -1)
                    elif (x_distance < 0 and y_distance < 0): # Bottom Left Move
                        return self.check_diagonal(_chessBoard, oldLocation, newLocation, -1, -1)
                    elif (x_distance < 0 and y_distance > 0): # Top Left Move
                        return self.check_diagonal(_chessBoard, oldLocation, newLocation, -1, 1)
                    elif (x_distance > 0 and y_distance > 0): # Top Right Move
                        return self.check_diagonal(_chessBoard, oldLocation, newLocation, 1, 1)
            elif (type == "Rook"):
                if (newLocation.x >= 0 and newLocation.x < 8 and newLocation.y >= 0 and newLocation.y < 8):
                    if (x_distance > 0 and y_distance == 0): # Right Move
                        return self.check_horizontal(_chessBoard, oldLocation, newLocation, 1)
                    elif (x_distance < 0 and y_distance == 0): # Left Move
                        return self.check_horizontal(_chessBoard, oldLocation, newLocation, -1)
                    elif (y_distance > 0 and x_distance == 0): # Upwards Move
                        return self.check_vertical(_chessBoard, oldLocation, newLocation, 1)
                    elif (y_distance < 0 and x_distance == 0): # Downwards Move
                        return self.check_vertical(_chessBoard, oldLocation, newLocation, -1)
            elif (type == "Queen"):
                if (newLocation.x >= 0 and newLocation.x < 8 and newLocation.y >= 0 and newLocation.y < 8):
                    x_distance = (newLocation.x - oldLocation.x)
                    y_distance = (newLocation.y - oldLocation.y)
                    if (x_distance > 0 and newLocation.y == oldLocation.y): # Right Move
                        return self.check_horizontal(_chessBoard, oldLocation, newLocation, 1)
                    elif (x_distance < 0 and newLocation.y == oldLocation.y): # Left Move
                        return self.check_horizontal(_chessBoard, oldLocation, newLocation, -1)
                    elif (y_distance > 0 and newLocation.x == oldLocation.x): # Upwards Move
                        return self.check_vertical(_chessBoard, oldLocation, newLocation, 1)
                    elif (y_distance < 0 and newLocation.x == oldLocation.x): # Downwards Move
                        return self.check_vertical(_chessBoard, oldLocation, newLocation, -1)
                    elif (x_distance > 0 and y_distance < 0): # Bottom Right Move
                        return self.check_diagonal(_chessBoard, oldLocation, newLocation, 1, -1)
                    elif (x_distance < 0 and y_distance < 0): # Bottom Left Move
                        return self.check_diagonal(_chessBoard, oldLocation, newLocation, -1, -1)
                    elif (x_distance < 0 and y_distance > 0): # Top Left Move
                        return self.check_diagonal(_chessBoard, oldLocation, newLocation, -1, 1)
                    elif (x_distance > 0 and y_distance > 0): # Top Left Move
                        return self.check_diagonal(_chessBoard, oldLocation, newLocation, 1, 1)
            elif (type == "King"):
                if (newLocation.x >= 0 and newLocation.x < 8 and newLocation.y >= 0 and newLocation.y < 8):
                    x_distance = (newLocation.x - oldLocation.x)
                    y_distance = (newLocation.y - oldLocation.y)
                    if (newLocation.y == oldLocation.y and x_distance == 1): # Right Move
                        return self.check_horizontal(_chessBoard, oldLocation, newLocation, 1)
                    elif (newLocation.y == oldLocation.y and x_distance == -1): # Left Move
                        return self.check_horizontal(_chessBoard, oldLocation, newLocation, -1)
                    elif (newLocation.x == oldLocation.x and y_distance == 1): # Upwards Move
                        return self.check_vertical(_chessBoard, oldLocation, newLocation, 1)
                    elif (newLocation.x == oldLocation.x and y_distance == -1): # Downwards Move
                        return self.check_vertical(_chessBoard, oldLocation, newLocation, -1)
                    elif (x_distance == 1 and y_distance == -1): # Bottom Right Move
                        return self.check_diagonal(_chessBoard, oldLocation, newLocation, 1, -1)
                    elif (x_distance == -1 and y_distance == -1): # Bottom Left Move
                        return self.check_diagonal(_chessBoard, oldLocation, newLocation, -1, -1)
                    elif (x_distance == -1 and y_distance == 1): # Top Left Move
                        return self.check_diagonal(_chessBoard, oldLocation, newLocation, -1, 1)
                    elif (x_distance == 1 and y_distance == 1): # Top Right Move
                        return self.check_diagonal(_chessBoard, oldLocation, newLocation, 1, 1)
                    elif (x_distance == 2 and y_distance == 0 and ((piece.rank == 0 and self.color == MinimaxTurn) or (piece.rank == 8 and self.color == -MinimaxTurn)) and _chessBoard.board.location[7][newLocation.y] == "R"): # Castling Right
                        for i in range(1, 3):
                            if (not _chessBoard.board.location[oldLocation.x + i][oldLocation.y] == ""):
                                return False
                        return True
                    elif (x_distance == -2 and y_distance == 0 and ((piece.rank == 0 and self.color == MinimaxTurn) or (piece.rank == 8 and self.color == -MinimaxTurn)) and _chessBoard.board.location[0][newLocation.y] == "R"): # Castling Left
                        for i in range(1, 4):
                            if (not _chessBoard.board.location[oldLocation.x - i][oldLocation.y] == ""):
                                return False
                        return True
        return False

    def fileToInt(self, file="a"):
        files = ["a", "b", "c", "d", "e", "f", "g", "h"]
        return files.index(file)
    def intToFile(self, file="a"):
        files = ["a", "b", "c", "d", "e", "f", "g", "h"]
        return files[file]
    def add_file(self, file, amount):
        files = ["a", "b", "c", "d", "e", "f", "g", "h"]
        _f = files.index(file)
        if (_f + amount > 7):
            return "h"
        elif (_f + amount < 0):
            return "a"
        else:
            return files[_f + amount]

    def create_move(self, actionObj, actionNum, newFile, newRank, _chessBoard, MinimaxTurn):
        enemyPoints = 0
        myPoints = 0

        pawn = "p" if MinimaxTurn > 0 else "P"
        bishop = "b" if MinimaxTurn > 0 else "B"
        rook = "r" if MinimaxTurn > 0 else "R"
        knight = "n" if MinimaxTurn > 0 else "N"
        queen = "q" if MinimaxTurn > 0 else "Q"
        king = "k" if MinimaxTurn > 0 else "K"

        myPawn = "P" if MinimaxTurn > 0 else "p"
        myBishop = "B" if MinimaxTurn > 0 else "b"
        myRook = "R" if MinimaxTurn > 0 else "r"
        myKnight = "N" if MinimaxTurn > 0 else "n"
        myQueen = "Q" if MinimaxTurn > 0 else "q"
        myKing = "K" if MinimaxTurn > 0 else "k"

        myMoveDirection = MinimaxTurn * self.player.rank_direction
        currentMove = move(actionObj, actionNum, newFile, newRank)
        newBoard = chessBoard(_chessBoard, currentMove, True)
        newBoard.currentMove.actionObj.has_moved = True

        oldLocation = point(self.fileToInt(actionObj.file), actionObj.rank - 1)
        newLocation = point(self.fileToInt(newFile), newRank - 1)

        capturedPiece = newBoard.board.location[newLocation.x][newLocation.y]
        newBoard.board.location[newLocation.x][newLocation.y] = newBoard.board.location[oldLocation.x][oldLocation.y]
        newBoard.board.location[oldLocation.x][oldLocation.y] = ""

        enemyPoints = 100 * len(newBoard.enemyPawn) + 300 * len(newBoard.enemyBishop) + 300 * len(newBoard.enemyKnight) + 500 * len(newBoard.enemyRook) + 900 * len(newBoard.enemyQueen)
        myPoints = 100 * len(newBoard.pawn) + 300 * len(newBoard.bishop) + 300 * len(newBoard.knight) + 500 * len(newBoard.rook) + 900 * len(newBoard.queen)

        if (capturedPiece == pawn):
            enemyPoints -= 100
            myPoints += 100
        elif (capturedPiece == bishop or capturedPiece == knight):
            enemyPoints -= 300
            myPoints += 3000
        elif (capturedPiece == rook):
            enemyPoints -= 500
            myPoints += 5000
        elif (capturedPiece == queen):
            enemyPoints -= 900
            myPoints += 9000

        if (oldLocation.y < 7 and oldLocation.y > 0 and newBoard.board.location[oldLocation.x][oldLocation.y - myMoveDirection] == myQueen):
            myPoints -= 1200
        if (oldLocation.y < 7 and oldLocation.y > 0 and newBoard.board.location[oldLocation.x][oldLocation.y - myMoveDirection] == myKing):
            myPoints -= 1200
        if (oldLocation.y < 7 and oldLocation.y > 0 and oldLocation.x > 0 and newBoard.board.location[oldLocation.x - 1][oldLocation.y - myMoveDirection] == myKing):
            myPoints -= 1200
        if (oldLocation.y < 7 and oldLocation.y > 0 and oldLocation.x < 7 and newBoard.board.location[oldLocation.x + 1][oldLocation.y - myMoveDirection] == myQueen):
            myPoints -= 1200
        if (oldLocation.y < 7 and oldLocation.y > 0 and oldLocation.x > 0 and oldLocation.x < 7 and
            (newBoard.board.location[oldLocation.x + 1][oldLocation.y - myMoveDirection] == myBishop or newBoard.board.location[oldLocation.x - 1][oldLocation.y - myMoveDirection] == myBishop)):
            myPoints += 300

        #if (len(self.myMoves) > 0 and
        #self.myMoves[len(self.myMoves)-1].actionObj.id == actionObj.id):
        #    myPoints -= 200

        #if (self.numMoves < 12):
        if (actionObj.type == "Pawn"):
            myPoints += random.randrange(200, 500)
            if (abs(oldLocation.x - newLocation.x) == 2):
                myPoints += 200
            if ((myMoveDirection < 0 and actionObj.rank == 2) or (myMoveDirection > 0 and actionObj.rank == 7)):
                myPoints += 10000
        elif (actionObj.type == "King" and capturedPiece == ""):
            myPoints -= 5000
        elif (actionObj.type == "King" and not capturedPiece == ""):
            myPoints -= 900
        elif (actionObj.type == "Queen"):
            myPoints -= 300

        if ((actionObj.type == "Rook" or actionObj.type == "Queen") and newLocation.y < 6 and newLocation.y > 1 and newLocation.x < 6 and newLocation.x > 1):
            if (newLocation.y + 2 == newBoard.enemyKing[0].rank or newLocation.y - 2 == newBoard.enemyKing[0].rank or
                self.intToFile(newLocation.x + 2) == newBoard.enemyKing[0].file or self.intToFile(newLocation.x - 2) == newBoard.enemyKing[0].file):
                myPoints += 800
        if (actionObj.type == "Bishop" or actionObj.type == "Queen"):
            for i in range(2, 8):
                if (newLocation.x + i < 8 and newLocation.y + i < 8):
                    if ((newLocation.y + 1 + i == newBoard.enemyKing[0].rank) and (self.intToFile(newLocation.x + i) == newBoard.enemyKing[0].file)):
                        myPoints += 600 + 200 if actionObj.type == "Bishop" else 0
                if (newLocation.x + i < 8 and newLocation.y - i >= 0):
                    if ((newLocation.y + 1 - i == newBoard.enemyKing[0].rank) and (self.intToFile(newLocation.x + i) == newBoard.enemyKing[0].file)):
                        myPoints += 600 + 200 if actionObj.type == "Bishop" else 0
                if (newLocation.x - i >= 0 and newLocation.y - i >= 0):
                    if ((newLocation.y + 1 - i == newBoard.enemyKing[0].rank) and (self.intToFile(newLocation.x - i) == newBoard.enemyKing[0].file)):
                        myPoints += 600 + 200 if actionObj.type == "Bishop" else 0
                if (newLocation.x - i >= 0 and newLocation.y + i < 8):
                    if ((newLocation.y + 1 + i == newBoard.enemyKing[0].rank) and (self.intToFile(newLocation.x - i) == newBoard.enemyKing[0].file)):
                        myPoints += 600 + 200 if actionObj.type == "Bishop" else 0

        foundPiece, _piecePoint = self.find_check_piece(newBoard, -MinimaxTurn) # If the other play would be in check
        if (foundPiece):
            myPoints += 8000


        #if (MinimaxTurn > 0):
        heuristicValue = myPoints - enemyPoints# + random.randrange(10, 220)
        #else:
        #    heuristicValue = enemyPoints - myPoints
        return newBoard, heuristicValue * MinimaxTurn

    def makeLastMove(self):
        numPieces = len(self.game.pieces)

        newBoard = chessBoard(None, None)
        if (len(self.chessBoard) > 0):
            newBoard.parent = self.chessBoard[-1]

        self.chessBoard.append(newBoard)

        for i in range(numPieces):
            if (not self.game.pieces[i].owner.id == self.player.id): # If piece doesn't belong to me
                if (self.game.pieces[i].type == "Pawn"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank - 1] = "p"
                elif (self.game.pieces[i].type == "Bishop"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank - 1] = "b"
                elif (self.game.pieces[i].type == "Rook"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank - 1] = "r"
                elif (self.game.pieces[i].type == "Knight"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank - 1] = "n"
                elif (self.game.pieces[i].type == "Queen"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank - 1] = "q"
                elif (self.game.pieces[i].type == "King"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank - 1] = "k"
            elif (self.game.pieces[i].owner.id == self.player.id): # If piece belongs to me
                if (self.game.pieces[i].type == "Pawn"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank - 1] = "P"
                elif (self.game.pieces[i].type == "Bishop"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank - 1] = "B"
                elif (self.game.pieces[i].type == "Rook"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank - 1] = "R"
                elif (self.game.pieces[i].type == "Knight"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank - 1] = "N"
                elif (self.game.pieces[i].type == "Queen"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank - 1] = "Q"
                elif (self.game.pieces[i].type == "King"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank - 1] = "K"
        #_chessBoard.board.location.reverse()

    def getPromotionType(self, _chessBoard):
        #promotionPoint = point(self.fileToInt(_chessBoard.currentMove.newFile), _chessBoard.currentMove.newRank - 1)

        if (len(_chessBoard.queen) == 0):
            return "Queen"
        #elif (self.player.rank_direction > 0): # White Player
        #    if (promotionPoint.x > 0 and _chessBoard.board.location[promotionPoint.x - 1][promotionPoint.y - 2] == "k"):
        #        return "Knight"
        #    elif (promotionPoint.x < 7 and _chessBoard.board.location[promotionPoint.x + 1][promotionPoint.y - 2] == "k"):
        #        return "Knight"
        return "Queen"

    def getMoves(self, _chessBoard, currentDepth, maxDepth, MinimaxTurn, alpha, beta, startTime):
        currentPossibleMoves = pQueue()
        myMoveDirection = MinimaxTurn * self.player.rank_direction
        for i in range(len(_chessBoard.myPieces)):
            _piece = _chessBoard.myPieces[i]
            if (not _piece.captured):
                if (_piece.type == "Pawn"):
                    if (not _piece.has_moved):
                        if (_chessBoard.board.location[self.fileToInt(_piece.file)][_piece.rank + 2*myMoveDirection - 1] == "" and
                            self.valid_move(_piece, _piece.file, _piece.rank + 2 * myMoveDirection, _chessBoard, MinimaxTurn)):
                            thisMove, h = self.create_move(_piece, i, _piece.file, _piece.rank + 2 * myMoveDirection, _chessBoard, MinimaxTurn)
                            if (currentDepth < maxDepth):
                                h = self.getMoves(thisMove, currentDepth + 1, maxDepth, -MinimaxTurn, alpha, beta, startTime)
                            currentPossibleMoves.put(thisMove, h)
                            if (MinimaxTurn > 0): # Max turn
                                if (h > beta): # PRUNE, Fail High
                                    item, weight = currentPossibleMoves.pop_back()
                                    return weight
                                elif (h > alpha):
                                    alpha = h
                                else:
                                    pass # Fail Low
                            elif (MinimaxTurn < 0): # Min turn
                                if (h < alpha): # PRUNE, Fail Low
                                    item, weight = currentPossibleMoves.pop()
                                    return weight
                                elif (h < beta):
                                    beta = h
                                else:
                                    pass # Fail High
                    if (_chessBoard.board.location[self.fileToInt(_piece.file)][_piece.rank + 1*myMoveDirection - 1] == "" and
                            self.valid_move(_piece, _piece.file, _piece.rank + 1 * myMoveDirection, _chessBoard, MinimaxTurn)):
                        thisMove, h = self.create_move(_piece, i, _piece.file, _piece.rank + 1 * myMoveDirection, _chessBoard, MinimaxTurn)
                        if (currentDepth < maxDepth):
                            h = self.getMoves(thisMove, currentDepth + 1, maxDepth, -MinimaxTurn, alpha, beta, startTime)
                        currentPossibleMoves.put(thisMove, h)
                        if (MinimaxTurn > 0): # Max turn
                            if (h > beta): # PRUNE, Fail High
                                item, weight = currentPossibleMoves.pop_back()
                                return weight
                            elif (h > alpha):
                                alpha = h
                            else:
                                pass # Fail Low
                        elif (MinimaxTurn < 0): # Min turn
                            if (h < alpha): # PRUNE, Fail Low
                                item, weight = currentPossibleMoves.pop()
                                return weight
                            elif (h < beta):
                                beta = h
                            else:
                                pass # Fail High
                    if (_chessBoard.board.location[self.fileToInt(self.add_file(_piece.file, 1))][_piece.rank + 1*myMoveDirection - 1] == "" and
                        not _piece.file == "h" and self.valid_move(_piece, self.add_file(_piece.file, 1), _piece.rank + 1 * myMoveDirection, _chessBoard, MinimaxTurn)):
                        thisMove, h = self.create_move(_piece, i, self.add_file(_piece.file, 1), _piece.rank + 1 * myMoveDirection, _chessBoard, MinimaxTurn)
                        if (currentDepth < maxDepth):
                            h = self.getMoves(thisMove, currentDepth + 1, maxDepth, -MinimaxTurn, alpha, beta, startTime)
                        currentPossibleMoves.put(thisMove, h)
                        if (MinimaxTurn > 0): # Max turn
                            if (h > beta): # PRUNE, Fail High
                                item, weight = currentPossibleMoves.pop_back()
                                return weight
                            elif (h > alpha):
                                alpha = h
                            else:
                                pass # Fail Low
                        elif (MinimaxTurn < 0): # Min turn
                            if (h < alpha): # PRUNE, Fail Low
                                item, weight = currentPossibleMoves.pop()
                                return weight
                            elif (h < beta):
                                beta = h
                            else:
                                pass # Fail High
                    if (_chessBoard.board.location[self.fileToInt(self.add_file(_piece.file, -1))][_piece.rank + 1*myMoveDirection - 1] == "" and
                        not _piece.file == "a" and self.valid_move(_piece, self.add_file(_piece.file, -1), _piece.rank + 1 * myMoveDirection, _chessBoard, MinimaxTurn)):
                        thisMove, h = self.create_move(_piece, i, self.add_file(_piece.file, -1), _piece.rank + 1 * myMoveDirection, _chessBoard, MinimaxTurn)
                        if (currentDepth < maxDepth):
                            h = self.getMoves(thisMove, currentDepth + 1, maxDepth, -MinimaxTurn, alpha, beta, startTime)
                        currentPossibleMoves.put(thisMove, h)
                        if (MinimaxTurn > 0): # Max turn
                            if (h > beta): # PRUNE, Fail High
                                item, weight = currentPossibleMoves.pop_back()
                                return weight
                            elif (h > alpha):
                                alpha = h
                            else:
                                pass # Fail Low
                        elif (MinimaxTurn < 0): # Min turn
                            if (h < alpha): # PRUNE, Fail Low
                                item, weight = currentPossibleMoves.pop()
                                return weight
                            elif (h < beta):
                                beta = h
                            else:
                                pass # Fail High
                if (_piece.type == "Knight"):
                    fileDirection = 1
                    fileAmount = 1
                    rankDirection = 1
                    rankAmount = 2
                    for k in range(8):
                        if (self.fileToInt(_piece.file) + fileAmount * fileDirection < 8 and self.fileToInt(_piece.file) + fileAmount * fileDirection >= 0 and _piece.rank + rankAmount * rankDirection < 8 and _piece.rank + rankAmount * rankDirection >= 0):
                            if (self.valid_move(_piece, self.add_file(_piece.file, fileAmount * fileDirection), _piece.rank + rankAmount * rankDirection, _chessBoard, MinimaxTurn)):
                                thisMove, h = self.create_move(_piece, i, self.add_file(_piece.file, fileAmount * fileDirection), _piece.rank + rankAmount * rankDirection, _chessBoard, MinimaxTurn)
                                if (currentDepth < maxDepth):
                                    h = self.getMoves(thisMove, currentDepth + 1, maxDepth, -MinimaxTurn, alpha, beta, startTime)
                                currentPossibleMoves.put(thisMove, h)
                                if (MinimaxTurn > 0): # Max turn
                                    if (h > beta): # PRUNE, Fail High
                                        item, weight = currentPossibleMoves.pop_back()
                                        return weight
                                    elif (h > alpha):
                                        alpha = h
                                    else:
                                        pass # Fail Low
                                elif (MinimaxTurn < 0): # Min turn
                                    if (h < alpha): # PRUNE, Fail Low
                                        item, weight = currentPossibleMoves.pop()
                                        return weight
                                    elif (h < beta):
                                        beta = h
                                    else:
                                        pass # Fail High
                        fileDirection *= -1
                        if (k % 2 == 1):
                            rankDirection *= -1
                        if (k == 3):
                            temp = fileAmount
                            fileAmount = rankAmount
                            rankAmount = temp
                if (_piece.type == "Bishop" or _piece.type == "Queen" or _piece.type == "King"):
                    for k in range(1, 8):
                        fileDirection = 1
                        rankDirection = 1
                        # fileDirection | rankDirection |
                        #       1 | 1 | Top Right
                        #      -1 | 1 | Top Left
                        #       1 | -1 | Bottom Right
                        #      -1 | -1 | Bottom Left
                        for t in range(4):
                            if (self.fileToInt(_piece.file) + k * fileDirection < 8 and self.fileToInt(_piece.file) + k * fileDirection >= 0 and
                                _piece.rank + k * rankDirection < 8 and _piece.rank + k * rankDirection >= 0 and
                                _chessBoard.board.location[self.fileToInt(self.add_file(_piece.file, k * fileDirection))][_piece.rank + k * rankDirection - 1] == ""):
                                if (k == 1 or (k > 1 and not _piece.type == "King")):
                                    if (self.valid_move(_piece, self.add_file(_piece.file, k * fileDirection), _piece.rank + k * rankDirection, _chessBoard, MinimaxTurn)):
                                        thisMove, h = self.create_move(_piece, i, self.add_file(_piece.file, k * fileDirection), _piece.rank + k * rankDirection, _chessBoard, MinimaxTurn)
                                        if (currentDepth < maxDepth):
                                            h = self.getMoves(thisMove, currentDepth + 1, maxDepth, -MinimaxTurn, alpha, beta, startTime)
                                        currentPossibleMoves.put(thisMove, h)
                                        if (MinimaxTurn > 0): # Max turn
                                            if (h > beta): # PRUNE, Fail High
                                                item, weight = currentPossibleMoves.pop_back()
                                                return weight
                                            elif (h > alpha):
                                                alpha = h
                                            else:
                                                pass # Fail Low
                                        elif (MinimaxTurn < 0): # Min turn
                                            if (h < alpha): # PRUNE, Fail Low
                                                item, weight = currentPossibleMoves.pop()
                                                return weight
                                            elif (h < beta):
                                                beta = h
                                            else:
                                                pass # Fail High
                            fileDirection *= -1
                            if (t == 1):
                                rankDirection *= -1
                if (_piece.type == "Rook" or _piece.type == "Queen" or _piece.type == "King"):
                    for k in range(1, 8):
                        fileDirection = 1
                        rankDirection = 0
                        # fileDirection | rankDirection |
                        #       1       |       0       | Right
                        #      -1       |       0       | Left
                        #       0       |       1       | Top
                        #       0       |      -1       | Bottom
                        for t in range(4):
                            if (self.fileToInt(_piece.file) + k * fileDirection < 8 and self.fileToInt(_piece.file) + k * fileDirection >= 0 and
                                _piece.rank + k * rankDirection < 8 and _piece.rank + k * rankDirection >= 0 and
                                _chessBoard.board.location[self.fileToInt(self.add_file(_piece.file, k * fileDirection))][_piece.rank + k * rankDirection - 1] == ""):
                                if (k == 1 or (k > 1 and not _piece.type == "King")):
                                    if (self.valid_move(_piece, self.add_file(_piece.file, k * fileDirection), _piece.rank + k * rankDirection, _chessBoard, MinimaxTurn)):
                                        thisMove, h = self.create_move(_piece, i, self.add_file(_piece.file, k * fileDirection), _piece.rank + k * rankDirection, _chessBoard, MinimaxTurn)
                                        if (currentDepth < maxDepth):
                                            h = self.getMoves(thisMove, currentDepth + 1, maxDepth, -MinimaxTurn, alpha, beta, startTime)
                                        currentPossibleMoves.put(thisMove, h)
                                        if (MinimaxTurn > 0): # Max turn
                                            if (h > beta): # PRUNE, Fail High
                                                item, weight = currentPossibleMoves.pop_back()
                                                return weight
                                            elif (h > alpha):
                                                alpha = h
                                            else:
                                                pass # Fail Low
                                        elif (MinimaxTurn < 0): # Min turn
                                            if (h < alpha): # PRUNE, Fail Low
                                                item, weight = currentPossibleMoves.pop()
                                                return weight
                                            elif (h < beta):
                                                beta = h
                                            else:
                                                pass # Fail High
                            fileDirection *= -1
                            rankDirection *= -1
                            if (t == 1):
                                temp = rankDirection
                                rankDirection = fileDirection
                                fileDirection = temp

        if (currentDepth > 1):
            if (MinimaxTurn > 0): # MAX's turn
                if (currentPossibleMoves.qsize() > 0):
                    item, weight = currentPossibleMoves.pop_back()
                    return weight
                else: # Stalemate or Checkmate
                    return -100000
            elif (MinimaxTurn < 0): # MIN's turn
                if (currentPossibleMoves.qsize() > 0):
                    item, weight = currentPossibleMoves.pop()
                    return weight
                else: # Stalemate or Checkmate
                    return 100000
        else:
            return currentPossibleMoves

    def get_name(self):
        """ This is the name you send to the server so your AI will control the
        player named this string.

        Returns
            str: The name of your Player.
        """

        return "Animated Coconut"  # REPLACE THIS WITH YOUR TEAM NAME

    def start(self):
        """ This is called once the game starts and your AI knows its playerID
        and game. You can initialize your AI here.
        """
        numPieces = len(self.game.pieces)
        self.makeLastMove()
        for i in range(numPieces):
            curPiece = chessPiece(self.game.pieces[i])
            if (curPiece.actual_piece.owner.id == self.player.id): # If piece belongs to me
                if (curPiece.type == "Pawn"):
                    self.chessBoard[-1].pawn.append(curPiece)
                elif (curPiece.type == "Bishop"):
                    self.chessBoard[-1].bishop.append(curPiece)
                elif (curPiece.type == "Rook"):
                    self.chessBoard[-1].rook.append(curPiece)
                elif (curPiece.type == "Knight"):
                    self.chessBoard[-1].knight.append(curPiece)
                elif (curPiece.type == "Queen"):
                    self.chessBoard[-1].queen.append(curPiece)
                elif (curPiece.type == "King"):
                    self.chessBoard[-1].king.append(curPiece)
                self.chessBoard[-1].myPieces.append(curPiece)
            else: # If piece doesn't belong to me
                if (curPiece.type == "Pawn"):
                    self.chessBoard[-1].enemyPawn.append(chessPiece(curPiece))
                elif (curPiece.type == "Bishop"):
                    self.chessBoard[-1].enemyBishop.append(chessPiece(curPiece))
                elif (curPiece.type == "Rook"):
                    self.chessBoard[-1].enemyRook.append(chessPiece(curPiece))
                elif (curPiece.type == "Knight"):
                    self.chessBoard[-1].enemyKnight.append(chessPiece(curPiece))
                elif (curPiece.type == "Queen"):
                    self.chessBoard[-1].enemyQueen.append(chessPiece(curPiece))
                elif (curPiece.type == "King"):
                    self.chessBoard[-1].enemyKing.append(chessPiece(curPiece))
                self.chessBoard[-1].enemyPieces.append(curPiece)

            self.color = self.player.rank_direction

    def game_updated(self):
        """ This is called every time the game's state updates, so if you are
        tracking anything you can update it here.
        """
        #self.makeLastMove()

        if (len(self.game.moves) > 0):
            prevMove = self.game.moves[-1]
            if (prevMove.piece.owner.id == self.player.id):
                if (not prevMove.piece.type == "Knight"):
                    self.chessBoard[-1].board.location[self.fileToInt(prevMove.to_file)][prevMove.to_rank - 1] = prevMove.piece.type[0]
                else:
                    self.chessBoard[-1].board.location[self.fileToInt(prevMove.to_file)][prevMove.to_rank - 1] = "N"

                if (prevMove.piece.type == "Pawn"):
                    for i in range(len(self.chessBoard[-1].pawn)):
                        if (prevMove.piece.id == self.chessBoard[-1].pawn[i].id):
                            self.chessBoard[-1].pawn[i] = chessPiece(prevMove.piece)
                            break
                elif (prevMove.piece.type == "Bishop"):
                    for i in range(len(self.chessBoard[-1].bishop)):
                        if (prevMove.piece.id == self.chessBoard[-1].bishop[i].id):
                            self.chessBoard[-1].bishop[i] = chessPiece(prevMove.piece)
                            break
                elif (prevMove.piece.type == "Rook"):
                    for i in range(len(self.chessBoard[-1].rook)):
                        if (prevMove.piece.id == self.chessBoard[-1].rook[i].id):
                            self.chessBoard[-1].rook[i] = chessPiece(prevMove.piece)
                            break
                elif (prevMove.piece.type == "Knight"):
                    for i in range(len(self.chessBoard[-1].knight)):
                        if (prevMove.piece.id == self.chessBoard[-1].knight[i].id):
                            self.chessBoard[-1].knight[i] = chessPiece(prevMove.piece)
                            break
                elif (prevMove.piece.type == "Queen"):
                    for i in range(len(self.chessBoard[-1].queen)):
                        if (prevMove.piece.id == self.chessBoard[-1].queen[i].id):
                            self.chessBoard[-1].queen[i] = chessPiece(prevMove.piece)
                            break
                elif (prevMove.piece.type == "King"):
                    for i in range(len(self.chessBoard[-1].king)):
                        if (prevMove.piece.id == self.chessBoard[-1].king[i].id):
                            self.chessBoard[-1].king[i] = chessPiece(prevMove.piece)
                            break
                    #In case the king castled
                    if ((prevMove.to_file == "c" or prevMove.to_file == "g") and (prevMove.to_rank == 8 or prevMove.to_rank == 1)):
                        self.chessBoard[-1].rook = []
                        for i in range(len(self.game.pieces)):
                            curPiece = self.game.pieces[i]
                            if (curPiece.owner.id == self.player.id and curPiece.type == "Rook"):
                                self.chessBoard[-1].rook.append(chessPiece(curPiece))
                                break
                self.chessBoard[-1].myPieces = self.chessBoard[-1].pawn + self.chessBoard[-1].rook + self.chessBoard[-1].bishop + self.chessBoard[-1].knight + self.chessBoard[-1].queen + self.chessBoard[-1].king
            else:
                if (not prevMove.piece.type == "Knight"):
                    self.chessBoard[-1].board.location[self.fileToInt(prevMove.to_file)][prevMove.to_rank - 1] = prevMove.piece.type[0].lower()
                else:
                    self.chessBoard[-1].board.location[self.fileToInt(prevMove.to_file)][prevMove.to_rank - 1] = "n"
                if (prevMove.piece.type == "Pawn"):
                    for i in range(len(self.chessBoard[-1].enemyPawn)):
                        if (prevMove.piece.id == self.chessBoard[-1].enemyPawn[i].id):
                            self.chessBoard[-1].enemyPawn[i] = chessPiece(prevMove.piece)
                            break
                elif (prevMove.piece.type == "Bishop"):
                    for i in range(len(self.chessBoard[-1].enemyBishop)):
                        if (prevMove.piece.id == self.chessBoard[-1].enemyBishop[i].id):
                            self.chessBoard[-1].enemyBishop[i] = chessPiece(prevMove.piece)
                            break
                elif (prevMove.piece.type == "Rook"):
                    for i in range(len(self.chessBoard[-1].enemyRook)):
                        if (prevMove.piece.id == self.chessBoard[-1].enemyRook[i].id):
                            self.chessBoard[-1].enemyRook[i] = chessPiece(prevMove.piece)
                            break
                elif (prevMove.piece.type == "Knight"):
                    for i in range(len(self.chessBoard[-1].enemyKnight)):
                        if (prevMove.piece.id == self.chessBoard[-1].enemyKnight[i].id):
                            self.chessBoard[-1].enemyKnight[i] = chessPiece(prevMove.piece)
                            break
                elif (prevMove.piece.type == "Queen"):
                    for i in range(len(self.chessBoard[-1].enemyQueen)):
                        if (prevMove.piece.id == self.chessBoard[-1].enemyQueen[i].id):
                            self.chessBoard[-1].enemyQueen[i] = chessPiece(prevMove.piece)
                            break
                elif (prevMove.piece.type == "King"):
                    for i in range(len(self.chessBoard[-1].enemyKing)):
                        if (prevMove.piece.id == self.chessBoard[-1].enemyKing[i].id):
                            self.chessBoard[-1].enemyKing[i] = chessPiece(prevMove.piece)
                            break
                    #In case the king castled
                    if ((prevMove.to_file == "c" or prevMove.to_file == "g") and (prevMove.to_rank == 8 or prevMove.to_rank == 1)):
                        self.chessBoard[-1].rook = []
                        for i in range(len(self.game.pieces)):
                            curPiece = self.game.pieces[i]
                            if (not curPiece.owner.id == self.player.id and curPiece.type == "Rook"):
                                self.chessBoard[-1].enemyRook.append(chessPiece(curPiece))
                                break
                self.chessBoard[-1].enemyPieces = self.chessBoard[-1].enemyPawn + self.chessBoard[-1].enemyRook + self.chessBoard[-1].enemyBishop + self.chessBoard[-1].enemyKnight + self.chessBoard[-1].enemyQueen + self.chessBoard[-1].enemyKing
            self.chessBoard[-1].board.location[self.fileToInt(prevMove.from_file)][prevMove.from_rank - 1] = ""

            capturedPiece = False

            if (not prevMove.captured == None):
                if (prevMove.captured.type == "Pawn"):
                    for i in range(len(self.chessBoard[-1].pawn)):
                        if (prevMove.captured.id == self.chessBoard[-1].pawn[i].actual_piece.id):
                            del self.chessBoard[-1].pawn[i]
                            capturedPiece = True
                            break
                elif (prevMove.captured.type == "Bishop"):
                    for i in range(len(self.chessBoard[-1].bishop)):
                        if (prevMove.captured.id == self.chessBoard[-1].bishop[i].actual_piece.id):
                            del self.chessBoard[-1].bishop[i]
                            capturedPiece = True
                            break
                elif (prevMove.captured.type == "Rook"):
                    for i in range(len(self.chessBoard[-1].rook)):
                        if (prevMove.captured.id == self.chessBoard[-1].rook[i].actual_piece.id):
                            del self.chessBoard[-1].rook[i]
                            capturedPiece = True
                            break
                elif (prevMove.captured.type == "Knight"):
                    for i in range(len(self.chessBoard[-1].knight)):
                        if (prevMove.captured.id == self.chessBoard[-1].knight[i].actual_piece.id):
                            del self.chessBoard[-1].knight[i]
                            capturedPiece = True
                            break
                elif (prevMove.captured.type == "Queen"):
                    for i in range(len(self.chessBoard[-1].queen)):
                        if (prevMove.captured.id == self.chessBoard[-1].queen[i].actual_piece.id):
                            del self.chessBoard[-1].queen[i]
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
        # Here is where you'll want to code your AI.

        # 1) print the board to the console
        self.print_current_board()

        currentPossibleMoves = pQueue()

        startTime = time.time()
        timeRemaining = self.player.time_remaining / math.pow(10, 9)
        print("Time Remaining:", timeRemaining, "seconds")
        numMovesLeft = (self.AVERAGE_MOVES * 4) - len(self.game.moves)
        maxTime = timeRemaining / numMovesLeft
        timeTaken = 0
        maxDepth = 1

        while (timeTaken < maxTime):
            print("Depth:", maxDepth)
            print("-------------------------------------------------------------")
            currentPossibleMoves = self.getMoves(self.chessBoard[-1], 1, maxDepth, 1, -float("inf"), float("inf"), startTime) # Look at all moves based on Minimax
                                            #   Current Board, Starting Depth,
                                            #   Max Depth, 1=Max Players Turn,
                                            #   alpha, beta, Start Time
            maxTime = timeRemaining / numMovesLeft
            timeTaken = time.time() - startTime
            maxDepth += 1

        if (self.player.in_check):
            print("In Check...")

        bestMove, bestPriority = currentPossibleMoves.pop_back() # Get the best possible move using Minimax

        #while (self.find_check_piece(bestMove, 1)):
        #    bestMove, bestPriority = currentPossibleMoves.pop_back()

        promotion = self.getPromotionType(bestMove)
        _move = bestMove.currentMove.actionObj.actual_piece.move(bestMove.currentMove.newFile, bestMove.currentMove.newRank, promotion)

        bestMove.currentMove.actionObj.move(bestMove.currentMove.newFile, bestMove.currentMove.newRank)

        #bestMove.flip()
        #self.chessBoard.append(bestMove)

        print("Moving", bestMove.currentMove.actionObj.type, "#" + str(bestMove.currentMove.actionObj.id), "to '" + str(bestMove.currentMove.newFile) + str(bestMove.currentMove.newRank) + "', with priority", bestPriority)

        if (not _move.promotion == ""):
            if (_move.promotion == "Bishop"):
                self.chessBoard[-1].bishop.append(chessPiece(_move.piece))
            if (_move.promotion == "Rook"):
                self.chessBoard[-1].rook.append(chessPiece(_move.piece))
            if (_move.promotion == "Knight"):
                self.chessBoard[-1].knight.append(chessPiece(_move.piece))
            if (_move.promotion == "Queen"):
                self.chessBoard[-1].queen.append(chessPiece(_move.piece))
            for i in range(len(self.chessBoard[-1].pawn)):
                if (self.chessBoard[-1].pawn[i].id == _move.piece.id):
                    del self.chessBoard[-1].pawn[i]
                    break
        print("-------------------->")
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
            print(f + 1, "|", end="")
            for r in range(8):
                if (not self.chessBoard[-1].board.location[r][f] == ""):
                    print("", self.chessBoard[-1].board.location[r][f], end=" ")
                else:
                    print(" . ", end="")
            print("|")
        print("  +------------------------+")
        print("    a  b  c  d  e  f  g  h <- FILES")
