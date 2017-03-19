# Point class to store a point
import random
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
# state: Stores one a possible state in the Tree
# - Requires a Location Map, a Radiation Map, an array of Boats
# - an array of Alligators, an array of Turtles, and an array of Trees
# - with optional parameters of Path-Cost, and Parent State
class move:
    def __init__(self, Board = None, ActObj = None, ActObjNum = 0, newF = 0, newR = 0, heuristicV = 0):
        self.board = Board
        #self.pathCost = deepcopy(pState.pathCost)
        self.actionObj = ActObj
        self.actionObjNum = ActObjNum
        self.newFile = newF
        self.newRank = newR
        self.weight = heuristicV
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
            print("RANDOM!")
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