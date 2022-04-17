import random
import time
from player import Player
import Colors
from Path import Path

#In this file I will write the class board,
#as well as the mutateElement and getBestPath methods for it.

#linear transformation from form in body to triangular is i --> i, j --> j - i
#or (i,j) --> (i-j,j)

class Board:

    def __init__(self, size, body = None):
        self.size = size

        self.body = []

        self.numTurns = 0 #counts the number of turns that have taken place

        self.pathArray = [] #path array stores all of the paths
        for i in range(size):
            self.pathArray +=[[None for j in range(i+1)]]

        for i in range(size):
            self.body +=[[0 for j in range(i+1)]]

            #initializes body as all 0. The ith list will have i elements
            #If the list is printed, then the diagonal will go up right instead of down right
            #The last list is the longest and is the booundary of the board
            #0 is empty space, 1 is player 1, -1 is player 2

        if body != None: #checks that body is correct
            bodyCorrect = True
            if type(body) == list and len(body) == size:
                for i in range(size):
                    if type(body[i])==list and len(body[i])==i+1:
                        for j in range(i+1):
                            if body[i][j] not in [-1,0,1]:
                                bodyCorrect = False
                                raise Exception("Body elements not in [-1,0,1]")
                    else:
                        bodyCorrect = False
                        raise Exception("Body sublist is wrong size or isn't a list")
            else:
                bodyCorrect = False
                raise Exception("Body is not list or is wrong size")

            if bodyCorrect:
                self.body = body
            else:
                print("body input was incorrect") #size is the number of points on each axis, body stores the array of values

    def __str__(self):
        retString = ""
        for i in range(self.size-1,-1,-1):
            for j in range(self.size - i):
                char = self.body[i+j][j]
                if char==0:
                    retString += Colors.bGray("~ ")
                #    retString += "  "
                elif char==1:
                    retString += Colors.bRed("1 ")
                elif char == -1:
                    retString += Colors.bBlue("0 ")
                elif char == 2: #2 and -2 are numbers on the path, they will be printed in yellow
                    retString += Colors.bOrange("1 ")
                elif char == -2:
                    retString += Colors.bOrange("0 ")
            retString += "\n"
        return retString #return body, formatted line by line

    def randomizeBoard(self):
        for i in range(self.size):
            for j in range(i+1):
                self.body[i][j] = random.choice([-1,1]) #randomizes all positions in board

    def randomizeBlanks(self):
        for i in self.blankIndices():
            self.body[i[0]][i[1]] = random.choice([-1,1])

    def sampleRandomFillings(self, numSamples = 100): #returns boards
        retList = []
        temp = copy.deepcopy(self)
        blankIndices = temp.blankIndices()
        for s in range(numSamples):
            for i in blankIndices:
                temp.body[i[0]][i[1]] = random.choice([-1,1])
            retList += [temp]
        return retList

    def isFilled(self): #checks if every entry has a -1 or 1, has a new value entered
        for i in range(self.size):
            for j in range(i+1):
                if self.body[i][j] == 0:
                    return False
        return True

    def updatePathArrayAt(self,index):
        ind1 = index[0]
        ind2 = index[1]
        if ind1 == self.size - 1: #last row in body array
        #uses two elements lists [s,d] s is score of point,
        #d is direction: -1 is for last element no direction, 0 is down (or right), 1 is down right (or up), 2 is 0 and 1 are equivalent
            self.pathArray[ind1][ind2] = [self.body[ind1][ind2], -1]
        else:
            PathListChoice1 = self.pathArray[ind1 + 1][ind2]
            PathListChoice2 = self.pathArray[ind1 + 1][ind2 + 1]
            pathScoreDiff = PathListChoice1[0] - PathListChoice2[0]
            if pathScoreDiff > 0: #straight path is better
                self.pathArray[ind1][ind2] = [self.body[ind1][ind2] + PathListChoice1[0],0]
            elif pathScoreDiff < 0:
                self.pathArray[ind1][ind2] = [self.body[ind1][ind2] + PathListChoice2[0],1]
            else:
                self.pathArray[ind1][ind2] = [self.body[ind1][ind2] + PathListChoice2[0],1]

    def updateWholePathArray(self):
        for ind1 in range(self.size - 1, -1, -1):
            for ind2 in range(ind1 + 1):
                self.updatePathArrayAt([ind1,ind2])

    def updatePathArrayFrom(self,index): #updates whole array starting at index
        for i in range(index[0]-index[1],-1,-1):
            for j in range(index[1],-1,-1):
                self.updatePathArrayAt([i+j,j])

    def updatePathArrayFindBestPathScore(self):
        self.updateWholePathArray()
        return self.pathArray[0][0].score

    def updatePathArrayFindBestPathPath(self):
        self.updateWholePathArray()
        return self.pathArray[0][0].path

    def setAndUpdate(self,index,value):
        if self.body[index[0]][index[1]] == value:
            pass
        else:
            self.body[index[0]][index[1]] = value
            self.updatePathArrayFrom(index)

    def turn(self,player1,player2,printBoard = False, printingToFile = False): #player is a class
        if self.isFilled():
            return False
        else:
            randnum = random.randint(0,1)
            move = player1.move(self.body)
            if len(move) == 3:
                isGameFinished = move[2]
                move = move[:2]
                if isGameFinished:
                    return False
            if randnum == 0:
                move.append(1) #move will be a 2 element list with the location that the player goes
            elif randnum == 1:
                move.append(-1)

            if self.body[move[0]][move[1]] == 0:
                self.body[move[0]][move[1]] = move[2]
                if printBoard:
                    if printingToFile:
                        print("BoardList.append(Board(" + str(self.size) + "," + str(self.body) + "))")
                    else:
                        print(self)
            else:
                print("Incorrect move")
                return False
            self.numTurns +=1
            return True

    def game(self,player1,player2, printBoard = False):
        stillPlaying = True
        while stillPlaying:
            stillPlaying = self.turn(player1,player2,printBoard)

        self.randomizeBlanks()
        bestPath = self.findBestPath()
        if printBoard:
            print("#Score is " + str(int((bestPath[0][0] + self.size)/2)) + "\n" + "#best path is " + str(bestPath[0][1]))
        return bestPath[0][0] #plays game between players

    def blankIndices(self):
        retList = []
        for i in range(self.size):
            for j in range(i+1):
                if self.body[i][j] == 0:
                    retList += [[i,j]]  #finds black points

        return retList #finds black points
