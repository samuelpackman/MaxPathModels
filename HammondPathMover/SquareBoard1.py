import random
import time
import Colors
import math

#In this file I will write the class board,
#as well as the mutateElement and getBestPath methods for it.

#linear transformation from form in body to triangular is i --> i, j --> j - i
#or (i,j) --> (i-j,j)

class Board:

    def __init__(self, size, body = None):
        self.size = size

        self.body = [[0 for i in range(size)] for j in range(size)]

        self.numTurns = 0 #counts the number of turns that have taken place

        self.pathArray = [[None for i in range(size)] for j in range(size)] #path array stores all of the paths

        self.randomizeBoard()
        self.updateWholePathArray()

    def __str__(self):
        retString = ""
        #for i in range(self.size-1,-1,-1):
            #for j in range(self.size - i):
                #char = self.body[i+j][j]


        for i in range(self.size):
            for j in range(self.size):
                char = self.body[self.size - 1 - i][j]


                if char==0:
                    retString += Colors.bGray("~ ")
                #    retString += "  "
                elif char==1:
                    retString += "1 "
                    #retString += Colors.bRed("1 ")
                elif char == -1:
                    retString += "0 "
                    #retString += Colors.bBlue("0 ")
                elif char == 2: #2 and -2 are numbers on the path, they will be printed in yellow
                    retString += Colors.bOrange("1 ")
                elif char == -2:
                    retString += Colors.bOrange("0 ")
            retString += "\n"
        return retString #return body, formatted line by line

    def randomizeBoard(self):
        for i in range(self.size):
            for j in range(self.size):
                self.body[i][j] = random.choice([-1,1]) #randomizes all positions in board

    def blankIndices(self):
        retList = []
        for i in range(self.size):
            for j in range(self.size):
                if self.body[i][j] == 0:
                    retList.append([i,j])  #finds black points

        return retList #finds black points

    def randomizeBlanks(self):
        for i in self.blankIndices():
            self.body[i[0]][i[1]] = random.choice([-1,1])


    def updatePathArrayAt(self,index):
        ind1 = index[0]
        ind2 = index[1]

        #cheating
        if ind1 > self.size - 1 or ind2 > self.size -1:
            return

        if ind1 == 0 and ind2 == 0: #first element
        #uses two elements lists [s,d] s is score of point,
        #d is direction: -1 is for first element no direction, 0 is down (or right), 1 is down right (or up), 2 is 0 and 1 are equivalent
            self.pathArray[ind1][ind2] = [self.body[0][0], -1]

        elif ind1 == 0:

            self.pathArray[0][ind2] = [self.body[0][ind2] + self.pathArray[0][ind2 - 1][0],1]

        elif ind2 == 0:
            self.pathArray[ind1][0] = [self.body[ind1][0] + self.pathArray[ind1 - 1][0][0],0]

        else:
            PathListChoice1 = self.pathArray[ind1 - 1][ind2]
            PathListChoice2 = self.pathArray[ind1][ind2 - 1]
            pathScoreDiff = PathListChoice1[0] - PathListChoice2[0]
            if pathScoreDiff > 0: #going down path is better
                self.pathArray[ind1][ind2] = [self.body[ind1][ind2] + PathListChoice1[0],0]
            elif pathScoreDiff < 0:
                self.pathArray[ind1][ind2] = [self.body[ind1][ind2] + PathListChoice2[0],1]
            else:
                self.pathArray[ind1][ind2] =  [self.body[ind1][ind2] + PathListChoice2[0],2]

    def updatePathArrayFrom(self,index):
        ind1 = index[0]
        ind2 = index[1]

        while True:
            self.updatePathArrayAt([ind1,ind2])

            if ind2 == 0:
                ind2 = ind1 + 1
                ind1 = 0
                while ind2 > self.size - 1:
                    ind1 += 1
                    ind2 -= 1

            else:
                ind1 += 1
                ind2 -= 1



            if ind1 == self.size and ind2 == self.size - 2:
                break

    def updateWholePathArray(self):
        self.updatePathArrayFrom([0,0])

    def highlightPathFrom_deprecated(self,index = [-1,-1]):
        if index == [-1,-1]:
            index = [self.size - 1, self.size - 1]
        ind1 = index[0]
        ind2 = index[1]

        while True:

            self.body[ind1][ind2] *= 2

            if self.pathArray[ind1][ind2][1] == 0:
                ind1 -= 1
            elif self.pathArray[ind1][ind2][1] == 1:
                ind2 -= 1
            elif self.pathArray[ind1][ind2][1] == -1:
                break
            else:
                print("something messed up. This statement shouldn't be called")
                exit()

    def highlightPathFrom(self,index = (-1,-1), highlighting = True):
        if index == (-1,-1):
            index = (self.size - 1, self.size - 1)

        inds = {index}
        while len(inds) > 0:
            new_inds = set()
            for ind in inds:
                i = ind[0]
                j = ind[1]
                if highlighting == True:
                    if abs(self.body[i][j]) != 2:
                        self.body[i][j] *= 2
                else:
                    if abs(self.body[i][j]) == 2:
                        self.body[i][j] /= 2

                move_val = self.pathArray[i][j][1]
                if move_val == 0:
                    new_inds.add((i-1,j))
                elif move_val == 1:
                    new_inds.add((i,j-1))
                elif move_val == 2:
                    new_inds.add((i-1,j))
                    new_inds.add((i,j-1))
                else:
                    pass

            inds = new_inds



    def num_under_path(self):
        num = 0
        for row in range(self.size):
            for col in range(self.size-1,-1,-1):
                if abs(self.body[row][col]) == 2:
                    num += col + 1
                    break
        return num

    def disp_from_middle(self): #calculates the displacement from the middle of the halfway point
        self.highlightPathFrom()
        is_first = True
        for i in range(self.size):
            if abs(self.body[self.size - i - 1][i]) == 2:
                if is_first:
                    first = i - (self.size-1)/2.
                    is_first = False
                last = i - (self.size-1)/2.
        self.highlightPathFrom(highlighting = False)
        return (first + last)/2

    def flip_random_and_update(self):
        randind1 = random.randint(0, self.size - 1)
        randind2 = random.randint(0, self.size - 1)
        self.body[randind1][randind2] *= -1
        self.updatePathArrayFrom([randind1,randind2])
