""""    def updatePathArrayFrom(self,index): #updates whole array starting at index
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
""""
