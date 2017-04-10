# Point class to store a point
import random
from copy import deepcopy

class point:
    def __init__(self, xx, yy):
        self.x = xx
        self.y = yy
    def set(self, xx, yy):
        self.x = xx
        self.y = yy
    def __eq__(self, otherPt):
        if (self.x == otherPt.x and self.y == otherPt.y):
            return True
        else:
            return False
    def __ne__(self, otherPt):
        if (self.x == otherPt.x and self.y == otherPt.y):
            return False
        else:
            return True

# A Map, or Grid object
class MAP:
    def __init__(self, fileX = 0, rankY = 0):
        self.location = [["" for i in range(rankY)] for k in range(fileX)]
        self.xSize = fileX
        self.ySize = rankY
    def setSize(self, fileX, rankY):
        self.location = [["" for i in range(rankY)] for k in range(fileX)]
        self.xSize = fileX
        self.ySize = rankY
    def __eq__(self, otherMap):
        for i in range(self.ySize):
            for k in range(self.xSize):
                if (not self.location[i][k] == otherMap.location[i][k]):
                    return False
        return True
    def __ne__(self, otherMap):
        for i in range(len(self.location)):
            for k in range(len(self.location[i])):
                if (self.location[i][k] != otherMap.location[i][k]):
                    return True
        return False

######
# move: stores a given move on a chessboard
class move:
    def __init__(self, ActObj, ActObjNum = 0, newF = 0, newR = 0, heuristicV = 0, parent = None):
        #self.pathCost = deepcopy(pState.pathCost)
        self.actionObj = ActObj
        self.actionObjNum = ActObjNum
        self.newFile = newF
        self.newRank = newR
        self.weight = heuristicV
        self.parent = parent
        self.children = []
        if (ActObj == None):
            raise NameError("ActObj is None")
    #################################
    # __eq__: allows a state to be using in a comparison operator
    def __eq__(self, otherState):
        if (otherState == None):
            return False
        elif (self.board == otherState.locationMap and \
              self.actionObj == otherState.actionObj and \
              self.actionObjNum == otherState.actionObjNum):
            return True
        else:
            return False
    # setActionObj: Sets the object that is being acted upon in this state
    def setActionObj(self, actObj, num, pathC=0):
        self.actionObj = actObj
        self.pathCost = pathC
        self.actionObjNum = num
    def addChild(self, childMove):
        self.children.append(childMove)

####################################
# A basic priority queue state
class pQueue:
    def __init__(self):
        self.queue = []
    #put: Puts a new object into the pQueue, with the given weight.
    # - Looks through all items currently on the queue and compares that items weight
    # - with the item you want to add's weight. The new item is put after all
    # - items with the same weight
    def put(self, item, weight = 0):
        putOn = False
        startRange = 0
        stopRange = len(self.queue)
        for i in range(len(self.queue)):
            #print("put: ", self.queue[i].priority, weight, self.queue[i].priority > weight)
            if (self.queue[i].priority <= weight):
                startRange = i+1
            if (self.queue[i].priority > weight):
                stopRange = i
                if (startRange == i):
                    putOn = True
                    self.queue.insert(i, pQueueObject(item, weight))
                break

        if (not putOn and startRange < stopRange):
            self.queue.insert(random.randrange(startRange, stopRange), pQueueObject(item, weight))
        elif (not putOn):
            self.queue.insert(startRange, pQueueObject(item, weight))
        #else:
        #    self.queue.append(pQueueObject(item, weight))
    #pop: Removes the top item of the queue, and returns it. Does not return the weight
    def pop(self):
        if (len(self.queue) > 0):
            top = self.queue.pop(0)
            return top.item, top.priority
        else:
            print("Empty queue!")
            return False
    def pop_back(self):
        if (len(self.queue) > 0):
            back = self.queue.pop()
            return back.item, back.priority
        else:
            print("Empty queue!")
            return False
    #qsize: Returns the size of the queue
    def qsize(self):
        return len(self.queue)

# pQueueObject: used as a container for the information in each index of the pQueue
class pQueueObject:
    def __init__(self, data, weight):
        self.item = data
        self.priority = weight

class chessPiece:
    def __init__(self, actual):
        self.file = actual.file
        self.rank = actual.rank
        self.id = actual.id
        self.type = actual.type
        self.captured = actual.captured
        self.has_moved = actual.has_moved
        self.actual_piece = actual
    def move(self, newF, newR, promo = ""):
        self.file = newF
        self.rank = newR

class chessBoard:
    def __init__(self, pMove, cMove, flip = False):        
        if (pMove == None):
            self.pawn = []
            self.rook = []
            self.bishop = []
            self.knight = []
            self.queen = []
            self.king = []
            self.enemyPawn = []
            self.enemyRook = []
            self.enemyBishop = []
            self.enemyKnight = []
            self.enemyQueen = []
            self.enemyKing = []
            self.numMoves = 0
            self.board = MAP(8, 8)
            self.myPieces = []
            self.enemyPieces = []
        elif (not flip):
            self.pawn = deepCopy(pMove.pawn)
            self.rook = deepCopy(pMove.rook)
            self.bishop = deepCopy(pMove.bishop)
            self.knight = deepCopy(pMove.knight)
            self.queen = deepCopy(pMove.queen)
            self.king = deepCopy(pMove.king)
            self.enemyPawn = deepCopy(pMove.enemyPawn)
            self.enemyRook = deepCopy(pMove.enemyRook)
            self.enemyBishop = deepCopy(pMove.enemyBishop)
            self.enemyKnight = deepCopy(pMove.enemyKnight)
            self.enemyQueen = deepCopy(pMove.enemyQueen)
            self.enemyKing = deepCopy(pMove.enemyKing)
            self.numMoves = pMove.numMoves + 1
            self.board = deepcopy(pMove.board)
            self.myPieces = self.pawn + self.rook + self.bishop + self.knight + self.queen + self.king
            self.enemyPieces = self.enemyPawn + self.enemyRook + self.enemyBishop + self.enemyKnight + self.enemyQueen + self.enemyKing
        elif (flip):
            self.pawn = deepCopy(pMove.enemyPawn)
            self.rook = deepCopy(pMove.enemyRook)
            self.bishop = deepCopy(pMove.enemyBishop)
            self.knight = deepCopy(pMove.enemyKnight)
            self.queen = deepCopy(pMove.enemyQueen)
            self.king = deepCopy(pMove.enemyKing)
            self.enemyPawn = deepCopy(pMove.pawn)
            self.enemyRook = deepCopy(pMove.rook)
            self.enemyBishop = deepCopy(pMove.bishop)
            self.enemyKnight = deepCopy(pMove.knight)
            self.enemyQueen = deepCopy(pMove.queen)
            self.enemyKing = deepCopy(pMove.king)
            self.numMoves = pMove.numMoves + 1
            self.board = deepcopy(pMove.board)
            self.myPieces = self.pawn + self.rook + self.bishop + self.knight + self.queen + self.king
            self.enemyPieces = self.enemyPawn + self.enemyRook + self.enemyBishop + self.enemyKnight + self.enemyQueen + self.enemyKing

        self.children = []
        self.parent = pMove
        self.currentMove = cMove
    def flip(self):
        self.myPieces = self.enemyPawn + self.enemyRook + self.enemyBishop + self.enemyKnight + self.enemyQueen + self.enemyKing
        self.enemyPieces = self.pawn + self.rook + self.bishop + self.knight + self.queen + self.king

def deepCopy(oldList):
    newList = []
    newList.extend(oldList)
    return newList