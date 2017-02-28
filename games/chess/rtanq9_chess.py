# Point class to store a point
class point:
    def __init__(self, xx, yy):
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
# state: Stores one a possible state in the Tree
# - Requires a Location Map, a Radiation Map, an array of Boats
# - an array of Alligators, an array of Turtles, and an array of Trees
# - with optional parameters of Path-Cost, and Parent State
class move:
    def __init__(self, Board = None, ActObj = None, ActObjNum = 0, newF = 0, newR = 0):
        self.board = Board
        #self.pathCost = deepcopy(pState.pathCost)
        self.actionObj = ActObj
        self.actionObjNum = ActObjNum
        self.newFile = newF
        self.newRank = newR
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