# This is where you build your AI for the Chess game.

from joueur.base_ai import BaseAI #
import random
from .rtanq9_chess import *
from random import shuffle
from copy import deepcopy
from time import sleep

class AI(BaseAI):
    """ The basic AI functions that are the same between games. """
    chessBoard = []
    enemyBoard = []
    
    color = 1 # 1 for White, -1 for Black

    piece_types = [ "Bishop", "Rook", "Knight", "Queen" ]
    # File -> x (a-h)
    # Rank -> y (0-7)

    def find_check_piece(self, _chessBoard):
        kingPos = point(self.fileToInt(_chessBoard.king[0].file), _chessBoard.king[0].rank-1)
        if (_chessBoard.currentMove.actionObj.type == "King"):
            kingPos = point(self.fileToInt(_chessBoard.currentMove.newFile), _chessBoard.currentMove.newRank-1)
            if (self.fileToInt(_chessBoard.currentMove.actionObj.file) == kingPos.x + 2 or self.fileToInt(_chessBoard.currentMove.actionObj.file) == kingPos.x - 2):
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
                        if (_chessBoard.board.location[kingPos.x - distance][kingPos.y + distance] in myPieces or
                            _chessBoard.board.location[kingPos.x - distance][kingPos.y + distance] in diagonal_blocks or
                            (_chessBoard.board.location[kingPos.x - distance][kingPos.y + distance] in diagonal_blocks_nonadjacent and distance > 1)):
                            topLeft = True
                        elif ((_chessBoard.board.location[kingPos.x - 1][kingPos.y + 1] == "p" and distance == 1 and self.color == 1) or
                              (_chessBoard.board.location[kingPos.x - 1][kingPos.y + 1] == "k" and distance == 1) or
                                _chessBoard.board.location[kingPos.x - distance][kingPos.y + distance] in diagonal_checks):
                            _piece.set(kingPos.x - distance, kingPos.y + distance)
                            foundPiece = True
                            break
                    elif (f == distance and r == 0 and not above and kingPos.y + distance < 8 and not foundPiece):
                        if (_chessBoard.board.location[kingPos.x][kingPos.y + distance] in myPieces or
                            _chessBoard.board.location[kingPos.x][kingPos.y + distance] in straight_blocks or
                            (_chessBoard.board.location[kingPos.x][kingPos.y + distance] in straight_blocks_nonadjacent and distance > 1)):
                            above = True
                        elif ((_chessBoard.board.location[kingPos.x][kingPos.y + 1] == "k" and distance == 1) or
                                _chessBoard.board.location[kingPos.x][kingPos.y + distance] in straight_checks):
                            _piece.set(kingPos.x, kingPos.y + distance)
                            foundPiece = True
                            break
                    elif (f == distance*2 and r == 0 and not topRight and kingPos.x + distance < 8 and kingPos.y + distance < 8 and not foundPiece):
                        if (_chessBoard.board.location[kingPos.x + distance][kingPos.y + distance] in myPieces or
                            _chessBoard.board.location[kingPos.x + distance][kingPos.y + distance] in diagonal_blocks or
                            (_chessBoard.board.location[kingPos.x + distance][kingPos.y + distance] in diagonal_blocks_nonadjacent and distance > 1)):
                            topRight = True
                        elif ((_chessBoard.board.location[kingPos.x + 1][kingPos.y + 1] == "p" and distance == 1 and self.color == 1) or
                              (_chessBoard.board.location[kingPos.x + 1][kingPos.y + 1] == "k" and distance == 1) or
                                _chessBoard.board.location[kingPos.x + distance][kingPos.y + distance] in diagonal_checks):
                            _piece.set(kingPos.x + distance, kingPos.y + distance)
                            foundPiece = True
                            break
                    # Middle Row
                    elif (f == 0 and r == distance and not left and kingPos.x - distance >= 0 and not foundPiece):
                        if (_chessBoard.board.location[kingPos.x - distance][kingPos.y] in myPieces or
                            _chessBoard.board.location[kingPos.x - distance][kingPos.y] in straight_blocks or
                            (_chessBoard.board.location[kingPos.x - distance][kingPos.y] in straight_blocks_nonadjacent and distance > 1)):
                            left = True
                        elif ((_chessBoard.board.location[kingPos.x - 1][kingPos.y] == "k" and distance == 1) or
                                _chessBoard.board.location[kingPos.x - distance][kingPos.y] in straight_checks):
                            _piece.set(kingPos.x - distance, kingPos.y - distance)
                            foundPiece = True
                            break
                    elif (f == distance and r == distance and not foundPiece):
                        pass # nothing to do! Since this our kings position...
                    elif (f == distance*2 and r == distance and not right and kingPos.x + distance < 8 and not foundPiece):
                        if (_chessBoard.board.location[kingPos.x + distance][kingPos.y] in myPieces or
                            _chessBoard.board.location[kingPos.x + distance][kingPos.y] in straight_blocks or
                            (_chessBoard.board.location[kingPos.x + distance][kingPos.y] in straight_blocks_nonadjacent and distance > 1)):
                            right = True
                        elif ((_chessBoard.board.location[kingPos.x + 1][kingPos.y] == "k" and distance == 1) or
                                _chessBoard.board.location[kingPos.x + distance][kingPos.y] in straight_checks):
                            _piece.set(kingPos.x + distance, kingPos.y - distance)
                            foundPiece = True
                            break
                    # Bottom Row
                    elif (f == 0 and r == distance*2 and not bottomLeft and kingPos.x - distance >= 0 and kingPos.y - distance >= 0 and not foundPiece):
                        if (_chessBoard.board.location[kingPos.x - distance][kingPos.y - distance] in myPieces or
                            _chessBoard.board.location[kingPos.x - distance][kingPos.y - distance] in diagonal_blocks or
                            (_chessBoard.board.location[kingPos.x - distance][kingPos.y - distance] in diagonal_blocks_nonadjacent and distance > 1)):
                            bottomLeft = True
                        elif ((_chessBoard.board.location[kingPos.x - 1][kingPos.y - 1] == "p" and distance == 1 and self.color == -1) or
                              (_chessBoard.board.location[kingPos.x - 1][kingPos.y - 1] == "k" and distance == 1) or
                                _chessBoard.board.location[kingPos.x - distance][kingPos.y - distance] in diagonal_checks):
                            _piece.set(kingPos.x - distance, kingPos.y - distance)
                            foundPiece = True
                            break
                    elif (f == distance and r == distance*2 and not below and kingPos.y - distance >= 0 and not foundPiece):
                        if (_chessBoard.board.location[kingPos.x][kingPos.y - distance] in myPieces or
                            _chessBoard.board.location[kingPos.x][kingPos.y - distance] in straight_blocks or
                            (_chessBoard.board.location[kingPos.x][kingPos.y - distance] in straight_blocks_nonadjacent and distance > 1)):
                            below = True
                        elif ((_chessBoard.board.location[kingPos.x][kingPos.y - 1] == "k" and distance == 1) or
                                _chessBoard.board.location[kingPos.x][kingPos.y - distance] in straight_checks):
                            _piece.set(kingPos.x, kingPos.y - distance)
                            foundPiece = True
                            break
                    elif (f == distance*2 and r == distance*2 and not bottomRight and kingPos.x + distance < 8 and kingPos.y - distance >= 0 and not foundPiece):
                        if (_chessBoard.board.location[kingPos.x + distance][kingPos.y - distance] in myPieces or
                            _chessBoard.board.location[kingPos.x + distance][kingPos.y - distance] in diagonal_blocks or
                            (_chessBoard.board.location[kingPos.x + distance][kingPos.y - distance] in diagonal_blocks_nonadjacent and distance > 1)):
                            bottomRight = True
                        elif ((_chessBoard.board.location[kingPos.x + 1][kingPos.y - 1] == "p" and distance == 1 and self.color == -1) or
                              (_chessBoard.board.location[kingPos.x + 1][kingPos.y - 1] == "k" and distance == 1) or
                                _chessBoard.board.location[kingPos.x + distance][kingPos.y - distance] in diagonal_checks):
                            _piece.set(kingPos.x + distance, kingPos.y - distance)
                            foundPiece = True
                            break
                    # Check For Knights
                    if (distance == 2 and not foundPiece):
                        # Top Row
                        if (f == 1 and r == 0 and kingPos.x - 1 >= 0 and kingPos.y + 2 < 8):
                            if (_chessBoard.board.location[kingPos.x - 1][kingPos.y + 2] == "n"):
                                _piece.set(kingPos.x - 1, kingPos.y + 2)
                                foundPiece = True
                                break
                        elif (f == 3 and r == 0 and kingPos.x + 1 < 8 and kingPos.y + 2 < 8):
                            if (_chessBoard.board.location[kingPos.x + 1][kingPos.y + 2] == "n"):
                                _piece.set(kingPos.x + 1, kingPos.y + 2)
                                foundPiece = True
                                break
                        # 2nd Row
                        elif (f == 0 and r == 1 and kingPos.x - 2 >= 0 and kingPos.y + 1 < 8):
                            if (_chessBoard.board.location[kingPos.x - 2][kingPos.y + 1] == "n"):
                                _piece.set(kingPos.x - 2, kingPos.y + 1)
                                foundPiece = True
                                break
                        elif (f == 4 and r == 1 and kingPos.x + 2 < 8 and kingPos.y + 1 < 8):
                            if (_chessBoard.board.location[kingPos.x + 2][kingPos.y + 1] == "n"):
                                _piece.set(kingPos.x + 2, kingPos.y + 1)
                                foundPiece = True
                                break
                        # 4th Row
                        elif (f == 0 and r == 3 and kingPos.x - 2 >= 0 and kingPos.y - 1 >= 0):
                            if (_chessBoard.board.location[kingPos.x - 2][kingPos.y - 1] == "n"):
                                _piece.set(kingPos.x - 2, kingPos.y - 1)
                                foundPiece = True
                                break
                        elif (f == 4 and r == 3 and kingPos.x + 2 < 8 and kingPos.y - 1 >= 0):
                            if (_chessBoard.board.location[kingPos.x + 2][kingPos.y - 1] == "n"):
                                _piece.set(kingPos.x + 2, kingPos.y - 1)
                                foundPiece = True
                                break
                        # Bottom Row
                        elif (f == 1 and r == 4 and kingPos.x - 1 >= 0 and kingPos.y - 2 >= 0):
                            if (_chessBoard.board.location[kingPos.x - 1][kingPos.y - 2] == "n"):
                                _piece.set(kingPos.x - 1, kingPos.y - 2)
                                foundPiece = True
                                break
                        elif (f == 3 and r == 4 and kingPos.x + 1 < 8 and kingPos.y - 2 >= 0):
                            if (_chessBoard.board.location[kingPos.x + 1][kingPos.y - 2] == "n"):
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

    def check_diagonal(self, _chessBoard, oldLocation, newLocation, x_dir, y_dir): #
        # x_dir / y_dir / direction
        #   1   /   1   / Up-Right
        #   1   /  -1   / Down-Right
        #  -1   /   1   / Up Left
        #  -1   /  -1   / Down Left
        x_distance = abs(newLocation.x - oldLocation.x)
        validPiecesToCapture = [ "p", "b", "r", "n", "q", "k" ]

        for i in range(1, x_distance):
            if (not _chessBoard.board.location[oldLocation.x + i*x_dir][oldLocation.y + i*y_dir] == ""):
                return False
        if (_chessBoard.board.location[newLocation.x][newLocation.y] in validPiecesToCapture or
            _chessBoard.board.location[newLocation.x][newLocation.y] == ""):
            return True

    def check_horizontal(self, _chessBoard, oldLocation, newLocation, x_dir):
        # x_dir / y_dir / direction
        #   1   /   1   / Up-Right
        #   1   /  -1   / Down-Right
        #  -1   /   1   / Up Left
        #  -1   /  -1   / Down Left
        x_distance = abs(newLocation.x - oldLocation.x)
        validPiecesToCapture = [ "p", "b", "r", "n", "q", "k" ]
        for i in range(1, x_distance):
            if (not _chessBoard.board.location[oldLocation.x + i*x_dir][oldLocation.y] == ""):
                return False
        if (_chessBoard.board.location[newLocation.x][newLocation.y] in validPiecesToCapture or
            _chessBoard.board.location[newLocation.x][newLocation.y] == ""):
            return True

    def check_vertical(self, _chessBoard, oldLocation, newLocation, y_dir):
        # x_dir / y_dir / direction
        #   1   /   1   / Up-Right
        #   1   /  -1   / Down-Right
        #  -1   /   1   / Up Left
        #  -1   /  -1   / Down Left
        y_distance = abs(newLocation.y - oldLocation.y)
        validPiecesToCapture = [ "p", "b", "r", "n", "q", "k" ]
        for i in range(1, y_distance):
            if (not _chessBoard.board.location[oldLocation.x][oldLocation.y + i*y_dir] == ""):
                return False
        if (_chessBoard.board.location[newLocation.x][newLocation.y] in validPiecesToCapture or
            _chessBoard.board.location[newLocation.x][newLocation.y] == ""):
            return True

    def valid_move(self, piece, newFile, newRank, _chessBoard):
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
        if (not piece.actual_piece[0].captured):
            if (type == "Pawn"):
                if (piece.file == newFile and newLocation.y >= 0 and newLocation.y < 8): # Moving Forward
                    if (y_range == 3 and not ((oldLocation.x == 1 and self.color == 1) or (oldLocation.x == 6 and self.color == -1))):
                        return False
                    elif (_chessBoard.board.location[newLocation.x][newLocation.y] == ""):
                        return True
                elif (not piece.file == "h" and self.add_file(piece.file, 1) == newFile): # Capturing a piece
                    if (not _chessBoard.parent == None and (_chessBoard.board.location[newLocation.x][newLocation.y] in validPiecesToCapture or  # Normal Capture
                        (((piece.rank == 4 and self.color == -1) or (piece.rank == 3 and self.color == 1)) and # En Passant
                         _chessBoard.board.location[oldLocation.x + 1][oldLocation.y] == "p" and _chessBoard.parent.board.location[oldLocation.x + 1][oldLocation.y + self.color] == "" and
                         _chessBoard.parent.board.location[oldLocation.x + 1][oldLocation.y] == "" and _chessBoard.board.location[oldLocation.x + 1][oldLocation.y + self.color] == ""))):
                        return True
                    elif (self.chessBoard[-1].parent == None):
                        _FEN =  self.game.fen.split(" ")
                        if (not _FEN[3] == "-"):
                           # and ((piece.rank == 4 and self.color == -1) or (piece.rank == 3 and self.color == 1)) and # En Passant
                           print(len(_FEN[3]))
                           for i in range(int(len(_FEN[3])/2)):
                               _f = self.fileToInt(_FEN[3][i*2])
                               _r = int(_FEN[3][i*2+1])
                               if (oldLocation.x == _f + 1 or oldLocation.x == _f - 1):
                                   if (oldLocation.y == _r):
                                       print("En Passant Right")
                                       return True
                        else:
                            return False
                elif (not piece.file == "a" and self.add_file(piece.file, -1) == newFile): # Capturing a piece
                    if (not _chessBoard.parent == None and (_chessBoard.board.location[newLocation.x][newLocation.y] in validPiecesToCapture or  # Normal Capture
                        (((piece.rank == 4 and self.color == -1) or (piece.rank == 3 and self.color == 1)) and # En Passant
                         _chessBoard.board.location[oldLocation.x - 1][oldLocation.y] == "p" and _chessBoard.parent.board.location[oldLocation.x - 1][oldLocation.y + self.color] == "" and
                         _chessBoard.parent.board.location[oldLocation.x - 1][oldLocation.y] == "" and _chessBoard.board.location[oldLocation.x - 1][oldLocation.y + self.color] == ""))):
                        return True
                    elif (self.chessBoard[-1].parent == None):
                        _FEN =  self.game.fen.split(" ")
                        if (not _FEN[3] == "-"):
                           # and ((piece.rank == 4 and self.color == -1) or (piece.rank == 3 and self.color == 1)) and # En Passant
                           for i in range(int(len(_FEN[3])/2)):
                               _f = self.fileToInt(_FEN[3][i*2])
                               _r = int(_FEN[3][i*2+1])
                               if (oldLocation.x == _f + 1 or oldLocation.x == _f - 1):
                                   if (oldLocation.y == _r):
                                       print("En Passant Left")
                                       return True
                        else:
                            return False
            elif (type == "Knight"):
                if (not _chessBoard.board.location[newLocation.x][newLocation.y] in myPieces and 
                    (_chessBoard.board.location[newLocation.x][newLocation.y] in validPiecesToCapture or _chessBoard.board.location[newLocation.x][newLocation.y] == "")):
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
                    if (newLocation.y == oldLocation.y and  x_distance == 1): # Right Move
                        return self.check_horizontal(_chessBoard, oldLocation, newLocation, 1)
                    elif (newLocation.y == oldLocation.y and  x_distance == -1): # Left Move
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
                    elif (x_distance == 2 and y_distance == 0 and ((piece.rank == 0 and self.color == 1) or (piece.rank == 8 and self.color == -1)) and 
                          _chessBoard.board.location[7][newLocation.y] == "R"): # Castling Right
                        for i in range(1, 3):
                            if (not _chessBoard.board.location[oldLocation.x + i][oldLocation.y] == ""):
                                return False
                        return True
                    elif (x_distance == -2 and y_distance == 0 and ((piece.rank == 0 and self.color == 1) or (piece.rank == 8 and self.color == -1)) and 
                          _chessBoard.board.location[0][newLocation.y] == "R"): # Castling Left
                        for i in range(1, 4):
                            if (not _chessBoard.board.location[oldLocation.x - i][oldLocation.y] == ""):
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

    def create_move(self, actionObj, actionNum, newFile, newRank, _chessBoard):
        enemyPoints = 0
        myPoints = 0

        newBoard = chessBoard(_chessBoard)
        oldLocation = point(self.fileToInt(actionObj.file), actionObj.rank - 1)
        newLocation = point(self.fileToInt(newFile), newRank - 1)
        capturedPiece = newBoard.board.location[newLocation.x][newLocation.y]
        newBoard.board.location[newLocation.x][newLocation.y] = newBoard.board.location[oldLocation.x][oldLocation.y]
        newBoard.board.location[oldLocation.x][oldLocation.y] = ""

        enemyPoints = 100*len(newBoard.enemyPawn) + 300*len(newBoard.enemyBishop) + 300*len(newBoard.enemyKnight) + 500*len(newBoard.enemyRook) + 900*len(newBoard.enemyQueen)
        myPoints = 100*len(newBoard.pawn) + 300*len(newBoard.bishop) + 300*len(newBoard.knight) + 500*len(newBoard.rook) + 900*len(newBoard.queen)

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
            newBoard.board.location[oldLocation.x][oldLocation.y - self.player.rank_direction] == "Q"):
            myPoints -= 350
        if (oldLocation.y < 7 and oldLocation.y > 0 and
            newBoard.board.location[oldLocation.x][oldLocation.y - self.player.rank_direction] == "K"):
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
            if (newLocation.y+1 == newBoard.enemyKing[0].rank or self.intToFile(newLocation.x) == newBoard.enemyKing[0].file):
                print(actionObj.type, str(self.intToFile(oldLocation.x)) + str(oldLocation.y+1), "->", str(self.intToFile(newLocation.x)) + str(newLocation.y+1), "in same rank/file as enemy king", ":", newBoard.enemyKing[0].rank, newBoard.enemyKing[0].file)
                myPoints += 300
        if (actionObj.type == "Bishop" or actionObj.type == "Queen"):
            #print(newLocation.x+1, self.enemyKing[0].rank)
            for i in range(8):
                if (newLocation.x+i < 8 and newLocation.y+i < 8):
                    #print(i, actionObj.type, str(self.intToFile(oldLocation.x)) + str(oldLocation.y+1), "->", str(self.intToFile(newLocation.x)) + str(newLocation.y+1), "  ", newLocation.y+1+i, self.enemyKing[0].rank, self.intToFile(newLocation.x+i), self.enemyKing[0].file)
                    if ((newLocation.y+1+i == newBoard.enemyKing[0].rank) and (self.intToFile(newLocation.x+i) == newBoard.enemyKing[0].file)):
                        print(actionObj.type, str(self.intToFile(oldLocation.x)) + str(oldLocation.y+1), "->", str(self.intToFile(newLocation.x)) + str(newLocation.y+1), "possible LOS of enemy king", ":", newBoard.enemyKing[0].rank, newBoard.enemyKing[0].file)
                        myPoints += 100 + 250 if actionObj.type == "Bishop" else 0
                if (newLocation.x+i < 8 and newLocation.y-i >= 0):
                    #print(i, actionObj.type, str(self.intToFile(oldLocation.x)) + str(oldLocation.y+1), "->", str(self.intToFile(newLocation.x)) + str(newLocation.y+1), "  ", newLocation.y+1-i, self.enemyKing[0].rank, self.intToFile(newLocation.x+i), self.enemyKing[0].file)
                    if ((newLocation.y+1-i == newBoard.enemyKing[0].rank) and (self.intToFile(newLocation.x+i) == newBoard.enemyKing[0].file)):
                        print(actionObj.type, str(self.intToFile(oldLocation.x)) + str(oldLocation.y+1), "->", str(self.intToFile(newLocation.x)) + str(newLocation.y+1), "possible LOS of enemy king", ":", newBoard.enemyKing[0].rank, newBoard.enemyKing[0].file)
                        myPoints += 200 + 250 if actionObj.type == "Bishop" else 0
                if (newLocation.x-i >= 0 and newLocation.y-i >= 0):
                    #print(i, actionObj.type, str(self.intToFile(oldLocation.x)) + str(oldLocation.y+1), "->", str(self.intToFile(newLocation.x)) + str(newLocation.y+1), "  ", newLocation.y+1-i, self.enemyKing[0].rank, self.intToFile(newLocation.x-i), self.enemyKing[0].file)
                    if ((newLocation.y+1-i == newBoard.enemyKing[0].rank) and (self.intToFile(newLocation.x-i) == newBoard.enemyKing[0].file)):
                        print(actionObj.type, str(self.intToFile(oldLocation.x)) + str(oldLocation.y+1), "->", str(self.intToFile(newLocation.x)) + str(newLocation.y+1), "possible LOS of enemy king", ":", newBoard.enemyKing[0].rank, newBoard.enemyKing[0].file)
                        myPoints += 200 + 250 if actionObj.type == "Bishop" else 0
                if (newLocation.x-i >= 0 and newLocation.y+i < 8):
                    #print(i, actionObj.type, str(self.intToFile(oldLocation.x)) + str(oldLocation.y+1), "->", str(self.intToFile(newLocation.x)) + str(newLocation.y+1), "  ", newLocation.y+1+i, self.enemyKing[0].rank, self.intToFile(newLocation.x-i), self.enemyKing[0].file)
                    if ((newLocation.y+1+i == newBoard.enemyKing[0].rank) and (self.intToFile(newLocation.x-i) == newBoard.enemyKing[0].file)):
                        print(actionObj.type, str(self.intToFile(oldLocation.x)) + str(oldLocation.y+1), "->", str(self.intToFile(newLocation.x)) + str(newLocation.y+1), "possible LOS of enemy king", ":", newBoard.enemyKing[0].rank, newBoard.enemyKing[0].file)
                        myPoints += 200 + 250 if actionObj.type == "Bishop" else 0

        heuristicValue = myPoints - enemyPoints
        #print(heuristicValue)

        newBoard.currentMove = move(actionObj, actionNum, newFile, newRank)
        return newBoard, heuristicValue

    def makeLastMove(self):
        numPieces = len(self.game.pieces)

        newBoard = chessBoard()
        if (len(self.chessBoard) > 0):
            newBoard.parent = self.chessBoard[-1]

        self.chessBoard.append(newBoard)
        
        for i in range(numPieces):
            if (not self.game.pieces[i].owner.id == self.player.id): # If piece doesn't belong to me
                if (self.game.pieces[i].type == "Pawn"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "p"
                elif (self.game.pieces[i].type == "Bishop"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "b"
                elif (self.game.pieces[i].type == "Rook"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "r"
                elif (self.game.pieces[i].type == "Knight"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "n"
                elif (self.game.pieces[i].type == "Queen"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "q"
                elif (self.game.pieces[i].type == "King"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "k"
            elif (self.game.pieces[i].owner.id == self.player.id): # If piece belongs to me
                if (self.game.pieces[i].type == "Pawn"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "P"
                elif (self.game.pieces[i].type == "Bishop"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "B"
                elif (self.game.pieces[i].type == "Rook"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "R"
                elif (self.game.pieces[i].type == "Knight"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "N"
                elif (self.game.pieces[i].type == "Queen"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "Q"
                elif (self.game.pieces[i].type == "King"):
                    newBoard.board.location[self.fileToInt(self.game.pieces[i].file)][self.game.pieces[i].rank-1] = "K"
        #_chessBoard.board.location.reverse()
        #print(_chessBoard.board.location)

    def getMyMoves(self, _chessBoard):
        depthLimit = 1
        currentPossibleMoves = pQueue()
        for i in range(len(_chessBoard.pawn)): # Check PAWN moves
            if (not _chessBoard.pawn[i].actual_piece[0].captured): # If not captured
                if (not _chessBoard.pawn[i].actual_piece[0].has_moved): # If hasn't moved from starting position
                    if (self.valid_move(_chessBoard.pawn[i], _chessBoard.pawn[i].file, _chessBoard.pawn[i].rank + 2*self.color, _chessBoard)):
                        currentPossibleMoves.put(*self.create_move(_chessBoard.pawn[i], i, _chessBoard.pawn[i].file, _chessBoard.pawn[i].rank + 2*self.color, _chessBoard))
                        #_chessBoard.pawn[i].move(_chessBoard.pawn[i].file, _chessBoard.pawn[i].rank + 2*self.color)
                if (self.valid_move(_chessBoard.pawn[i], _chessBoard.pawn[i].file, _chessBoard.pawn[i].rank + 1*self.color, _chessBoard)):
                    currentPossibleMoves.put(*self.create_move(_chessBoard.pawn[i], i, _chessBoard.pawn[i].file, _chessBoard.pawn[i].rank + 1*self.color, _chessBoard))
                    #_chessBoard.pawn[i].move(_chessBoard.pawn[i].file, _chessBoard.pawn[i].rank + 1*self.color)
                if (not _chessBoard.pawn[i].file == "h" and self.valid_move(_chessBoard.pawn[i], self.add_file(_chessBoard.pawn[i].file, 1), _chessBoard.pawn[i].rank + 1*self.color, _chessBoard)):
                    currentPossibleMoves.put(*self.create_move(_chessBoard.pawn[i], i, self.add_file(_chessBoard.pawn[i].file, 1), _chessBoard.pawn[i].rank + 1*self.color, _chessBoard))
                    #_chessBoard.pawn[i].move(self.add_file(_chessBoard.pawn[i].file, 1), _chessBoard.pawn[i].rank + 1*self.color)
                if (not _chessBoard.pawn[i].file == "a" and self.valid_move(_chessBoard.pawn[i], self.add_file(_chessBoard.pawn[i].file, -1), _chessBoard.pawn[i].rank + 1*self.color, _chessBoard)):
                    currentPossibleMoves.put(*self.create_move(_chessBoard.pawn[i], i, self.add_file(_chessBoard.pawn[i].file, -1), _chessBoard.pawn[i].rank + 1*self.color, _chessBoard))
                    #_chessBoard.pawn[i].move(self.add_file(_chessBoard.pawn[i].file, -1), _chessBoard.pawn[i].rank + 1*self.color)
        for i in range(len(_chessBoard.knight)): # Check KNIGHT moves
            if (not _chessBoard.knight[i].actual_piece[0].captured): # If not captured
                if (not _chessBoard.knight[i].file == "h" and _chessBoard.knight[i].rank > 2 and
                    self.valid_move(_chessBoard.knight[i], self.add_file(_chessBoard.knight[i].file, 1), _chessBoard.knight[i].rank - 2, _chessBoard)):
                    currentPossibleMoves.put(*self.create_move(_chessBoard.knight[i], i, self.add_file(_chessBoard.knight[i].file, 1), _chessBoard.knight[i].rank - 2, _chessBoard))
                    #_chessBoard.knight[i].move(self.add_file(_chessBoard.knight[i].file, 1), _chessBoard.knight[i].rank - 2)
                if (not _chessBoard.knight[i].file == "a" and _chessBoard.knight[i].rank > 2 and
                    self.valid_move(_chessBoard.knight[i], self.add_file(_chessBoard.knight[i].file, -1), _chessBoard.knight[i].rank - 2, _chessBoard)):
                    currentPossibleMoves.put(*self.create_move(_chessBoard.knight[i], i, self.add_file(_chessBoard.knight[i].file, -1), _chessBoard.knight[i].rank - 2, _chessBoard))
                    #_chessBoard.knight[i].move(self.add_file(_chessBoard.knight[i].file, -1), _chessBoard.knight[i].rank - 2)
                if (not _chessBoard.knight[i].file == "a" and not _chessBoard.knight[i].file == "b" and _chessBoard.knight[i].rank > 1 and
                    self.valid_move(_chessBoard.knight[i], self.add_file(_chessBoard.knight[i].file, -2), _chessBoard.knight[i].rank - 1, _chessBoard)):
                    currentPossibleMoves.put(*self.create_move(_chessBoard.knight[i], i, self.add_file(_chessBoard.knight[i].file, -2), _chessBoard.knight[i].rank - 1, _chessBoard))
                    #_chessBoard.knight[i].move(self.add_file(_chessBoard.knight[i].file, -2), _chessBoard.knight[i].rank - 1)
                if (not _chessBoard.knight[i].file == "g" and not _chessBoard.knight[i].file == "h" and _chessBoard.knight[i].rank > 1 and
                    self.valid_move(_chessBoard.knight[i], self.add_file(_chessBoard.knight[i].file, 2), _chessBoard.knight[i].rank - 1, _chessBoard)):
                    currentPossibleMoves.put(*self.create_move(_chessBoard.knight[i], i, self.add_file(_chessBoard.knight[i].file, 2), _chessBoard.knight[i].rank - 1, _chessBoard))
                    #_chessBoard.knight[i].move(self.add_file(_chessBoard.knight[i].file, 2), _chessBoard.knight[i].rank - 1)
                if (not _chessBoard.knight[i].file == "h" and _chessBoard.knight[i].rank < 7 and
                    self.valid_move(_chessBoard.knight[i], self.add_file(_chessBoard.knight[i].file, 1), _chessBoard.knight[i].rank + 2, _chessBoard)):
                    currentPossibleMoves.put(*self.create_move(_chessBoard.knight[i], i, self.add_file(_chessBoard.knight[i].file, 1), _chessBoard.knight[i].rank + 2, _chessBoard))
                    #_chessBoard.knight[i].move(self.add_file(_chessBoard.knight[i].file, 1), _chessBoard.knight[i].rank + 2)
                if (not _chessBoard.knight[i].file == "a" and _chessBoard.knight[i].rank < 7 and
                    self.valid_move(_chessBoard.knight[i], self.add_file(_chessBoard.knight[i].file, -1), _chessBoard.knight[i].rank + 2, _chessBoard)):
                    currentPossibleMoves.put(*self.create_move(_chessBoard.knight[i], i, self.add_file(_chessBoard.knight[i].file, -1), _chessBoard.knight[i].rank + 2, _chessBoard))
                    #_chessBoard.knight[i].move(self.add_file(_chessBoard.knight[i].file, -1), _chessBoard.knight[i].rank + 2)
                if (not _chessBoard.knight[i].file == "a" and not _chessBoard.knight[i].file == "b" and _chessBoard.knight[i].rank <= 8 and	
                    self.valid_move(_chessBoard.knight[i], self.add_file(_chessBoard.knight[i].file, -2), _chessBoard.knight[i].rank + 1, _chessBoard)):
                    currentPossibleMoves.put(*self.create_move(_chessBoard.knight[i], i, self.add_file(_chessBoard.knight[i].file, -2), _chessBoard.knight[i].rank + 1, _chessBoard))
                    #_chessBoard.knight[i].move(self.add_file(_chessBoard.knight[i].file, -2), _chessBoard.knight[i].rank + 1)
                if (not _chessBoard.knight[i].file == "g" and not _chessBoard.knight[i].file == "h" and _chessBoard.knight[i].rank <= 8 and
                    self.valid_move(_chessBoard.knight[i], self.add_file(_chessBoard.knight[i].file, 2), _chessBoard.knight[i].rank + 1, _chessBoard)):
                    currentPossibleMoves.put(*self.create_move(_chessBoard.knight[i], i, self.add_file(_chessBoard.knight[i].file, 2), _chessBoard.knight[i].rank + 1, _chessBoard))
                    #_chessBoard.knight[i].move(self.add_file(_chessBoard.knight[i].file, 2), _chessBoard.knight[i].rank + 1)
        for i in range(len(_chessBoard.bishop)): # Check BISHOP moves
            if (not _chessBoard.bishop[i].actual_piece[0].captured): # If not captured
                for k in range(8):
                    if (self.fileToInt(_chessBoard.bishop[i].file) + k < 8 and _chessBoard.bishop[i].rank - k >= 0): # Bottom Right move
                        if (self.valid_move(_chessBoard.bishop[i], self.add_file(_chessBoard.bishop[i].file, k), _chessBoard.bishop[i].rank - k, _chessBoard)):
                            currentPossibleMoves.put(*self.create_move(_chessBoard.bishop[i], i, self.add_file(_chessBoard.bishop[i].file, k), _chessBoard.bishop[i].rank - k, _chessBoard))
                            #_chessBoard.bishop[i].move(self.add_file(_chessBoard.bishop[i].file, k), _chessBoard.bishop[i].rank - k)
                    if (self.fileToInt(_chessBoard.bishop[i].file) - k >= 0 and _chessBoard.bishop[i].rank - k >= 0): # Bottom Left move
                        if (self.valid_move(_chessBoard.bishop[i], self.add_file(_chessBoard.bishop[i].file, -k), _chessBoard.bishop[i].rank - k, _chessBoard)):
                            currentPossibleMoves.put(*self.create_move(_chessBoard.bishop[i], i, self.add_file(_chessBoard.bishop[i].file, -k), _chessBoard.bishop[i].rank - k, _chessBoard))
                            #_chessBoard.bishop[i].move(self.add_file(_chessBoard.bishop[i].file, -k), _chessBoard.bishop[i].rank - k)
                    if (self.fileToInt(_chessBoard.bishop[i].file) - k >= 0 and _chessBoard.bishop[i].rank + k <= 8): # Top Left move
                        if (self.valid_move(_chessBoard.bishop[i], self.add_file(_chessBoard.bishop[i].file, -k), _chessBoard.bishop[i].rank + k, _chessBoard)):
                            currentPossibleMoves.put(*self.create_move(_chessBoard.bishop[i], i, self.add_file(_chessBoard.bishop[i].file, -k), _chessBoard.bishop[i].rank + k, _chessBoard))
                            #_chessBoard.bishop[i].move(self.add_file(_chessBoard.bishop[i].file, -k), _chessBoard.bishop[i].rank + k)
                    if (self.fileToInt(_chessBoard.bishop[i].file) + k < 8 and _chessBoard.bishop[i].rank + k <= 8): # Top Right move
                        if (self.valid_move(_chessBoard.bishop[i], self.add_file(_chessBoard.bishop[i].file, k), _chessBoard.bishop[i].rank + k, _chessBoard)):
                            currentPossibleMoves.put(*self.create_move(_chessBoard.bishop[i], i, self.add_file(_chessBoard.bishop[i].file, k), _chessBoard.bishop[i].rank + k, _chessBoard))
                            #_chessBoard.bishop[i].move(self.add_file(_chessBoard.bishop[i].file, -k), _chessBoard.bishop[i].rank + k)
        for i in range(len(_chessBoard.rook)): # Check ROOK moves
            if (not _chessBoard.rook[i].actual_piece[0].captured): # If not captured
                for k in range(8):
                    if (self.fileToInt(_chessBoard.rook[i].file) + k < 8): # Right move
                        if (self.valid_move(_chessBoard.rook[i], self.add_file(_chessBoard.rook[i].file, k), _chessBoard.rook[i].rank, _chessBoard)):
                            currentPossibleMoves.put(*self.create_move(_chessBoard.rook[i], i, self.add_file(_chessBoard.rook[i].file, k), _chessBoard.rook[i].rank, _chessBoard))
                            #_chessBoard.rook[i].move(self.add_file(_chessBoard.rook[i].file, k), _chessBoard.rook[i].rank)
                    if (self.fileToInt(_chessBoard.rook[i].file) + k >= 0): # Left move
                        if (self.valid_move(_chessBoard.rook[i], self.add_file(_chessBoard.rook[i].file, -k), _chessBoard.rook[i].rank, _chessBoard)):
                            currentPossibleMoves.put(*self.create_move(_chessBoard.rook[i], i, self.add_file(_chessBoard.rook[i].file, -k), _chessBoard.rook[i].rank, _chessBoard))
                            #_chessBoard.rook[i].move(self.add_file(_chessBoard.rook[i].file, -k), _chessBoard.rook[i].rank)
                    if (_chessBoard.rook[i].rank + k <= 8): # Upwards move
                        if (self.valid_move(_chessBoard.rook[i], _chessBoard.rook[i].file, _chessBoard.rook[i].rank + k, _chessBoard)):
                            currentPossibleMoves.put(*self.create_move(_chessBoard.rook[i], i, _chessBoard.rook[i].file, _chessBoard.rook[i].rank + k, _chessBoard))
                            #_chessBoard.rook[i].move(_chessBoard.rook[i].file, _chessBoard.rook[i].rank + k)
                    if (_chessBoard.rook[i].rank - k >= 0): # Downwards move
                        #print("Rook Down?")
                        if (self.valid_move(_chessBoard.rook[i], _chessBoard.rook[i].file, _chessBoard.rook[i].rank - k, _chessBoard)):
                            currentPossibleMoves.put(*self.create_move(_chessBoard.rook[i], i, _chessBoard.rook[i].file, _chessBoard.rook[i].rank - k, _chessBoard))
                            #_chessBoard.rook[i].move(_chessBoard.rook[i].file, _chessBoard.rook[i].rank - k)
        for i in range(len(_chessBoard.queen)): # Check QUEEN moves
            if (not _chessBoard.queen[i].actual_piece[0].captured): # If not captured
                for k in range(8):
                    if (self.fileToInt(_chessBoard.queen[i].file) + k < 8 and _chessBoard.queen[i].rank - k >= 0): # Bottom Right move
                        if (self.valid_move(_chessBoard.queen[i], self.add_file(_chessBoard.queen[i].file, k), _chessBoard.queen[i].rank - k, _chessBoard)):
                            currentPossibleMoves.put(*self.create_move(_chessBoard.queen[i], i, self.add_file(_chessBoard.queen[i].file, k), _chessBoard.queen[i].rank - k, _chessBoard))
                            #_chessBoard.queen[i].move(self.add_file(_chessBoard.queen[i].file, k), _chessBoard.queen[i].rank - k)
                    if (self.fileToInt(_chessBoard.queen[i].file) - k >= 0 and _chessBoard.queen[i].rank - k >= 0): # Bottom Left move
                        if (self.valid_move(_chessBoard.queen[i], self.add_file(_chessBoard.queen[i].file, -k), _chessBoard.queen[i].rank - k, _chessBoard)):
                            currentPossibleMoves.put(*self.create_move(_chessBoard.queen[i], i, self.add_file(_chessBoard.queen[i].file, -k), _chessBoard.queen[i].rank - k, _chessBoard))
                            #_chessBoard.queen[i].move(self.add_file(_chessBoard.queen[i].file, -k), _chessBoard.queen[i].rank - k)
                    if (self.fileToInt(_chessBoard.queen[i].file) - k >= 0 and _chessBoard.queen[i].rank + k <= 8): # Top Left move
                        if (self.valid_move(_chessBoard.queen[i], self.add_file(_chessBoard.queen[i].file, -k), _chessBoard.queen[i].rank + k, _chessBoard)):
                            currentPossibleMoves.put(*self.create_move(_chessBoard.queen[i], i, self.add_file(_chessBoard.queen[i].file, -k), _chessBoard.queen[i].rank + k, _chessBoard))
                            #_chessBoard.queen[i].move(self.add_file(_chessBoard.queen[i].file, -k), _chessBoard.queen[i].rank + k)
                    if (self.fileToInt(_chessBoard.queen[i].file) + k < 8 and _chessBoard.queen[i].rank + k <= 8): # Top Right move
                        if (self.valid_move(_chessBoard.queen[i], self.add_file(_chessBoard.queen[i].file, k), _chessBoard.queen[i].rank + k, _chessBoard)):
                            currentPossibleMoves.put(*self.create_move(_chessBoard.queen[i], i, self.add_file(_chessBoard.queen[i].file, k), _chessBoard.queen[i].rank + k, _chessBoard))
                            #_chessBoard.queen[i].move(self.add_file(_chessBoard.queen[i].file, k), _chessBoard.queen[i].rank + k)
                    if (self.fileToInt(_chessBoard.queen[i].file) + k < 8): # Right move
                        if (self.valid_move(_chessBoard.queen[i], self.add_file(_chessBoard.queen[i].file, k), _chessBoard.queen[i].rank, _chessBoard)):
                            currentPossibleMoves.put(*self.create_move(_chessBoard.queen[i], i, self.add_file(_chessBoard.queen[i].file, k), _chessBoard.queen[i].rank, _chessBoard))
                            #_chessBoard.queen[i].move(self.add_file(_chessBoard.queen[i].file, k), _chessBoard.queen[i].rank)
                    if (self.fileToInt(_chessBoard.queen[i].file) + k >= 0): # Left move
                        if (self.valid_move(_chessBoard.queen[i], self.add_file(_chessBoard.queen[i].file, -k), _chessBoard.queen[i].rank, _chessBoard)):
                            currentPossibleMoves.put(*self.create_move(_chessBoard.queen[i], i, self.add_file(_chessBoard.queen[i].file, -k), _chessBoard.queen[i].rank, _chessBoard))
                            #_chessBoard.queen[i].move(self.add_file(_chessBoard.queen[i].file, -k), _chessBoard.queen[i].rank)
                    if (_chessBoard.queen[i].rank + k <= 8): # Upwards move
                        if (self.valid_move(_chessBoard.queen[i], _chessBoard.queen[i].file, _chessBoard.queen[i].rank + k, _chessBoard)):
                            currentPossibleMoves.put(*self.create_move(_chessBoard.queen[i], i, _chessBoard.queen[i].file, _chessBoard.queen[i].rank + k, _chessBoard))
                            #_chessBoard.queen[i].move(_chessBoard.queen[i].file, _chessBoard.queen[i].rank + k)
                    if (_chessBoard.queen[i].rank - k >= 0): # Downwards move
                        if (self.valid_move(_chessBoard.queen[i], _chessBoard.queen[i].file, _chessBoard.queen[i].rank - k, _chessBoard)):
                            currentPossibleMoves.put(*self.create_move(_chessBoard.queen[i], i, _chessBoard.queen[i].file, _chessBoard.queen[i].rank - k, _chessBoard))
                            #_chessBoard.queen[i].move(_chessBoard.queen[i].file, _chessBoard.queen[i].rank - k)
        for i in range(len(_chessBoard.king)): # Check KING moves
            if (not _chessBoard.king[i].actual_piece[0].captured): # If not captured
                if (self.fileToInt(_chessBoard.king[i].file) + 1 < 8 and _chessBoard.king[i].rank - 1 >= 0): # Bottom Right move
                    if (self.valid_move(_chessBoard.king[i], self.add_file(_chessBoard.king[i].file, 1), _chessBoard.king[i].rank - 1, _chessBoard)):
                        currentPossibleMoves.put(*self.create_move(_chessBoard.king[i], 0, self.add_file(_chessBoard.king[i].file, 1), _chessBoard.king[i].rank - 1, _chessBoard))
                        #_chessBoard.king[i].move(self.add_file(_chessBoard.king[i].file, 1), _chessBoard.king[i].rank - 1)
                if (self.fileToInt(_chessBoard.king[i].file) - 1 >= 0 and _chessBoard.king[i].rank - 1 >= 0): # Bottom Left move
                    if (self.valid_move(_chessBoard.king[i], self.add_file(_chessBoard.king[i].file, -1), _chessBoard.king[i].rank - 1, _chessBoard)):
                        currentPossibleMoves.put(*self.create_move(_chessBoard.king[i], 0, self.add_file(_chessBoard.king[i].file, -1), _chessBoard.king[i].rank - 1, _chessBoard))
                        #_chessBoard.king[i].move(self.add_file(_chessBoard.king[i].file, -1), _chessBoard.king[i].rank - 1)
                if (self.fileToInt(_chessBoard.king[i].file) - 1 >= 0 and _chessBoard.king[i].rank + 1 <= 8): # Top Left move
                    if (self.valid_move(_chessBoard.king[i], self.add_file(_chessBoard.king[i].file, -1), _chessBoard.king[i].rank + 1, _chessBoard)):
                        currentPossibleMoves.put(*self.create_move(_chessBoard.king[i], 0, self.add_file(_chessBoard.king[i].file, -1), _chessBoard.king[i].rank + 1, _chessBoard))
                        #_chessBoard.king[i].move(self.add_file(_chessBoard.king[i].file, -1), _chessBoard.king[i].rank + 1)
                if (self.fileToInt(_chessBoard.king[i].file) + 1 < 8 and _chessBoard.king[i].rank + 1 <= 8): # Top Right move
                    if (self.valid_move(_chessBoard.king[i], self.add_file(_chessBoard.king[i].file, 1), _chessBoard.king[i].rank + 1, _chessBoard)):
                        currentPossibleMoves.put(*self.create_move(_chessBoard.king[i], 0, self.add_file(_chessBoard.king[i].file, 1), _chessBoard.king[i].rank + 1, _chessBoard))
                        #_chessBoard.king[i].move(self.add_file(_chessBoard.king[i].file, 1), _chessBoard.king[i].rank + 1)
                if (self.fileToInt(_chessBoard.king[i].file) + 1 < 8): # Right move
                    if (self.valid_move(_chessBoard.king[i], self.add_file(_chessBoard.king[i].file, 1), _chessBoard.king[i].rank, _chessBoard)):
                        currentPossibleMoves.put(*self.create_move(_chessBoard.king[i], 0, self.add_file(_chessBoard.king[i].file, 1), _chessBoard.king[i].rank, _chessBoard))
                        #_chessBoard.king[i].move(self.add_file(_chessBoard.king[i].file, 1), _chessBoard.king[i].rank)
                if (self.fileToInt(_chessBoard.king[i].file) - 1 >= 0): # Left move
                    if (self.valid_move(_chessBoard.king[i], self.add_file(_chessBoard.king[i].file, -1), _chessBoard.king[i].rank, _chessBoard)):
                        currentPossibleMoves.put(*self.create_move(_chessBoard.king[i], 0, self.add_file(_chessBoard.king[i].file, -1), _chessBoard.king[i].rank, _chessBoard))
                        #_chessBoard.king[i].move(self.add_file(_chessBoard.king[i].file, -1), _chessBoard.king[i].rank)
                if (_chessBoard.king[i].rank + 1 <= 8): # Upwards move
                    if (self.valid_move(_chessBoard.king[i], _chessBoard.king[i].file, _chessBoard.king[i].rank + 1, _chessBoard)):
                        currentPossibleMoves.put(*self.create_move(_chessBoard.king[i], 0, _chessBoard.king[i].file, _chessBoard.king[i].rank + 1, _chessBoard))
                       # _chessBoard.king[i].move(_chessBoard.king[i].file, _chessBoard.king[i].rank + 1)
                if (_chessBoard.king[i].rank - 1 >= 0): # Downwards move
                    if (self.valid_move(_chessBoard.king[i], _chessBoard.king[i].file, _chessBoard.king[i].rank - 1, _chessBoard)):
                        currentPossibleMoves.put(*self.create_move(_chessBoard.king[i], 0, _chessBoard.king[i].file, _chessBoard.king[i].rank - 1, _chessBoard))
                        #_chessBoard.king[i].move(_chessBoard.king[i].file, _chessBoard.king[i].rank - 1)
                # CASTLING
                if (not _chessBoard.king[i].actual_piece[0].has_moved):
                    for k in range(0, len(_chessBoard.rook)):
                        if (not _chessBoard.rook[k].actual_piece[0].has_moved and not _chessBoard.rook[k].actual_piece[0].captured):
                            if (self.fileToInt(_chessBoard.rook[k].file) > self.fileToInt(_chessBoard.king[i].file)):
                                if (self.valid_move(_chessBoard.king[i], self.add_file(_chessBoard.king[i].file, 2), _chessBoard.king[i].rank, _chessBoard)):
                                    currentPossibleMoves.put(*self.create_move(_chessBoard.king[i], 0, self.add_file(_chessBoard.king[i].file, 2), _chessBoard.king[i].rank, _chessBoard))
                                    #_chessBoard.king[i].move(self.add_file(_chessBoard.king[i].file, 2), _chessBoard.king[i].rank)
                            elif (self.fileToInt(_chessBoard.rook[k].file) < self.fileToInt(_chessBoard.king[i].file)):
                                if (self.valid_move(_chessBoard.king[i], self.add_file(_chessBoard.king[i].file, -2), _chessBoard.king[i].rank, _chessBoard)):
                                    currentPossibleMoves.put(*self.create_move(_chessBoard.king[i], 0, self.add_file(_chessBoard.king[i].file, -2), _chessBoard.king[i].rank, _chessBoard))
                                    #_chessBoard.king[i].move(self.add_file(_chessBoard.king[i].file, -2), _chessBoard.king[i].rank)
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
            curPiece = self.game.pieces[i]
            if (curPiece.owner.id == self.player.id): # If piece belongs to me
                if (curPiece.type == "Pawn"):
                    self.chessBoard[-1].pawn.append(chessPiece(curPiece))
                elif (curPiece.type == "Bishop"):
                    self.chessBoard[-1].bishop.append(chessPiece(curPiece))
                elif (curPiece.type == "Rook"):
                    self.chessBoard[-1].rook.append(chessPiece(curPiece))
                elif (curPiece.type == "Knight"):
                    self.chessBoard[-1].knight.append(chessPiece(curPiece))
                elif (curPiece.type == "Queen"):
                    self.chessBoard[-1].queen.append(chessPiece(curPiece))
                elif (curPiece.type == "King"):
                    self.chessBoard[-1].king.append(chessPiece(curPiece))
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
                    self.chessBoard[-1].board.location[self.fileToInt(prevMove.to_file)][prevMove.to_rank-1] = prevMove.piece.type[0]
                else:
                    self.chessBoard[-1].board.location[self.fileToInt(prevMove.to_file)][prevMove.to_rank-1] = "N"

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
            else:
                if (not prevMove.piece.type == "Knight"):
                    self.chessBoard[-1].board.location[self.fileToInt(prevMove.to_file)][prevMove.to_rank-1] = prevMove.piece.type[0].lower()
                else:
                    self.chessBoard[-1].board.location[self.fileToInt(prevMove.to_file)][prevMove.to_rank-1] = "n"
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
            self.chessBoard[-1].board.location[self.fileToInt(prevMove.from_file)][prevMove.from_rank-1] = ""

            capturedPiece = False

            if (not prevMove.captured == None):
                if (prevMove.captured.type == "Pawn"):
                    for i in range(len(self.chessBoard[-1].pawn)):
                        if (prevMove.captured.id == self.chessBoard[-1].pawn[i].actual_piece[0].id):
                            print("Pawn captured")
                            del self.chessBoard[-1].pawn[i]
                            capturedPiece = True
                            break
                elif (prevMove.captured.type == "Bishop"):
                    for i in range(len(self.chessBoard[-1].bishop)):
                        if (prevMove.captured.id == self.chessBoard[-1].bishop[i].actual_piece[0].id):
                            print("Bishop captured")
                            del self.chessBoard[-1].bishop[i]
                            capturedPiece = True
                            break
                elif (prevMove.captured.type == "Rook"):
                    for i in range(len(self.chessBoard[-1].rook)):
                        if (prevMove.captured.id == self.chessBoard[-1].rook[i].actual_piece[0].id):
                            print("Rook captured")
                            del self.chessBoard[-1].rook[i]
                            capturedPiece = True
                            break
                elif (prevMove.captured.type == "Knight"):
                    for i in range(len(self.chessBoard[-1].knight)):
                        if (prevMove.captured.id == self.chessBoard[-1].knight[i].actual_piece[0].id):
                            print("Knight captured")
                            del self.chessBoard[-1].knight[i]
                            capturedPiece = True
                            break
                elif (prevMove.captured.type == "Queen"):
                    for i in range(len(self.chessBoard[-1].queen)):
                        if (prevMove.captured.id == self.chessBoard[-1].queen[i].actual_piece[0].id):
                            print("Queen captured")
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

        # 2) print the opponent's last move to the console
        #if len(self.game.moves) > 0:
            #print("Opponent's Last Move: ", self.game.moves[-1].piece.type, "'", self.game.moves[-1].to_file, self.game.moves[-1].to_rank, "'")

        # 3) print how much time remaining this AI has to calculate moves
        # print("Time Remaining: " + str(self.player.time_remaining) + " ns")

        # 4) make a random (and probably invalid) move.
        #random_piece = random.choice(self.player.pieces)
        #random_file = chr(ord("a") + random.randrange(8))
        #random_rank = random.randrange(8) + 1
        #random_piece.move(random_file, random_rank)
        currentPossibleMoves = pQueue()
        currentPossibleMoves = self.getMyMoves(self.chessBoard[-1]) # Look at all moves based on Minimax
        print(len(self.chessBoard))
        if (self.player.in_check):
            print("In Check...")

        bestMove, bestPriority = currentPossibleMoves.pop_back() # Get the best possible move using Minimax
        while (self.find_check_piece(bestMove)):
            bestMove, bestPriority = currentPossibleMoves.pop_back()

        #promotion = getPromotionType() # DEFINE THIS!
        print(bestMove.currentMove.actionObj.actual_piece[0].captured, bestMove.currentMove.actionObj.actual_piece[0].file, bestMove.currentMove.actionObj.actual_piece[0]. rank, bestMove.currentMove.actionObj.actual_piece[0].id)
        _move = bestMove.currentMove.actionObj.actual_piece[0].move(bestMove.currentMove.newFile, bestMove.currentMove.newRank, self.piece_types[random.randrange(len(self.piece_types))])
        
        bestMove.currentMove.actionObj.move(bestMove.currentMove.newFile, bestMove.currentMove.newRank)

        self.chessBoard.append(bestMove)
        
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
            print(f+1, "|", end="")
            for r in range(8):
                if (not self.chessBoard[-1].board.location[r][f] == ""):
                    print("", self.chessBoard[-1].board.location[r][f], end=" ")
                else:
                    print(" . ", end="")
            print("|")
        print("  +------------------------+")
        print("    a  b  c  d  e  f  g  h <- FILES")
