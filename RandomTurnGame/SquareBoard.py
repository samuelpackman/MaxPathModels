import random
import time
from player import Player
import Colors
#In this file I will write the class board,
#as well as the mutateElement and getBestPath methods for it.

class SquareBoard:
    def __init__(self, size, body = None):
        self.size = size

        self.body = []

        self.numTurns = 0 #counts the number of turns that have taken place

        for i in range(size):
            self.body +=[[0 for j in range(i+1)]]
        for i in range(size - 1):
            self.body +=[[0 for j in range(size - i - 1)]]

            #initializes body as all 0. The ith list will have i elements
            #If the list is printed, then the diagonal will go up right instead of down right
            #The last list is the longest and is the booundary of the board
            #0 is empty space, 1 is player 1, -1 is player 2

        if body != None: #checks that body is correct
            self.body = body
     #size is the number of points on each axis, body stores the array of values

    def __str__(self):
        retString = ""
        for index,value in enumerate(self.body):
            if index > self.size - 1:
                for i in range(index - self.size + 1):
                    retString += "  "
            for j in value:
                if j==0:
                    retString += "_ "
                if j==1:
                    retString += Colors.bRed("1 ")
                if j == -1:
                    retString += Colors.bBlue("0 ")
            retString += "\n"
        return retString #return body, formatted line by line

    def printAllNums(self):
        retString = ""
        for index,value in enumerate(self.body):
            if index > self.size - 1:
                for i in range(index - self.size + 1):
                    retString += "  "
            for j in value:
                if j==0:
                    retString += "_ "
                else:
                    retString += str(j) + " "
            retString += "\n"
        return retString



    def randomizeHalfBoard(self): #randomizes top half
        for i in range(self.size):
            for j in range(i+1):
                self.body[i][j] = random.choice([-1,1])
        #randomizes all positions in board

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

    def findBestPath(self,i=0): #finds the best path from a particular location. Returns a list with the value and the path in it. 0 will indicate forward, and 1 is forward and up
        if not self.isFilled():
            print("The Board is not filled")
        else:
            if i == self.size - 1:               #function is recursively defined. This is the base case when the point is on the edge
                return [[self.body[i][j],[]] for j in range(i+1)] #creates all of the base paths
            else:
                recursivePath = self.findBestPath(i+1)
                retList = []
                for j in range(i+1):
                    choicePath1 = recursivePath[j] #the path just going forward 1, not up
                    choicePath2 = recursivePath[j+1]  #the path going forward and up

                    if choicePath1[0] > choicePath2[0]: #forward is the best path
                        retList += [[self.body[i][j] + choicePath1[0], [0] + choicePath1[1]]]

                    elif choicePath2[0] > choicePath1[0]: #forward and up is the best path
                        retList += [[self.body[i][j] + choicePath2[0], [1] + choicePath2[1]]]

                    else: #both paths are equal, for now will arbitrarily choose choicePath1
                        retList += [[self.body[i][j] + choicePath1[0], [0] + choicePath1[1]]]
                return retList

    def findBestPathAllPaths(self,i=0): #finds the best path from a particular location. Returns a list with the value and the path in it. 0 will indicate forward, and 1 is forward and up
        if not self.isFilled():
            print("The Board is not filled")
        else:
            if i == 2 * self.size - 2:         #function is recursively defined. This is the base case when the point is on the edge
                return [[self.body[i][0],[]] ] #creates all of the base paths
            elif i < self.size - 1:
                recursivePath = self.findBestPathAllPaths(i+1)
                retList = []
                for j in range(i+1):
                    choicePath1 = recursivePath[j] #the list of paths just going forward 1, not up
                    choicePath2 = recursivePath[j+1]  #the list of paths going forward and up

                    if choicePath1[0] > choicePath2[0]: #forward is the best path
                        retList.append(#this layer contains score then paths
                        [self.body[i][j] + choicePath1[0]] + [[0] + choicePath for choicePath in choicePath1[1:]]
                        )
                    elif choicePath2[0] > choicePath1[0]: #forward and up is the best path
                        retList.append(#this layer contains score then paths
                        [self.body[i][j] + choicePath2[0]] + [[1] + choicePath for choicePath in choicePath2[1:]]
                        )
                    else: #both paths are equal
                        retList.append(#this layer contains score then paths
                        [self.body[i][j] + choicePath1[0]] + [[0] + choicePath for choicePath in choicePath1[1:]] + [[1] + choicePath for choicePath in choicePath2[1:]]
                        )

                return retList
            else:
                recursivePath = self.findBestPathAllPaths(i+1)
                retList = []
                for j in range(2 * self.size - i - 3):
                    choicePath1 = recursivePath[j] #the list of paths just going forward 1, not up
                    choicePath2 = recursivePath[j+1]  #the list of paths going forward and up

                    if choicePath1[0] > choicePath2[0]: #forward is the best path
                        retList.append(#this layer contains score then paths
                        [self.body[i][j] + choicePath1[0]] + [[0] + choicePath for choicePath in choicePath1[1:]]
                        )

                    elif choicePath2[0] > choicePath1[0]: #forward and up is the best path
                        retList.append(#this layer contains score then paths
                        [self.body[i][j] + choicePath2[0]] + [[1] + choicePath for choicePath in choicePath2[1:]]
                        )
                    else: #both paths are equal
                        retList.append(#this layer contains score then paths
                        [self.body[i][j] + choicePath1[0]] + [[0] + choicePath for choicePath in choicePath1[1:]] + [[1] + choicePath for choicePath in choicePath2[1:]]
                        )

                return [ [self.body[i][-1] + recursivePath[0][0]] + [[1] + choicePath for choicePath in recursivePath[0][1:]] ] + retList + [ [self.body[i][-1] + recursivePath[-1][0]] + [[0] + choicePath for choicePath in recursivePath[-1][1:]] ]


    def findBestPathScore(self):
        return self.findBestPath()[0][0]

    def turn(self,player1,player2,printBoard = False): #player is a class
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
                    print("BoardList.append(Board(" + str(self.size) + "," + str(self.body) + "))")
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
                    retList.append([i,j])  #finds black points
        for i in range(self.size, 2 * self.size-1):
            for j in range(2 * self.size - i -1 ):
                if self.body[i][j] == 0:
                    retList.append([i,j])  #finds black points
        return retList #finds black points
