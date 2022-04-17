from Board import Board
import strategies
from HammondStrategy import HammondStrategy
from player import Player
import sys
import time
import random
import copy
#this is the main file where games are played

def outputScoreToRealScore(size,score):
    return (size + score)//2

def Gametest(strat1,strat2,boardSize = 100,numGames = 1,printBoards = False):

    player1 = Player(strat1)
    player2 = Player(strat2)

    avgScore = 0
    for i in range(numGames):
        testBoard = Board(boardSize)
        avgScore += testBoard.game(player1,player2,printBoards)/numGames

    print("Average Score is " + str(outputScoreToRealScore(boardSize,avgScore)))

def HammondGame(boardSize = 100, sampleSize = 100, printBoards = False):
    GameOverCounter = 0

    GameBoard = Board(boardSize)

    testBoards = [Board(boardSize) for i in range(sampleSize)]
    for board in testBoards:
        board.randomizeBoard()
        board.updateWholePathArray()

    #setup is done

    stillPlaying = True

    while stillPlaying:
        countBoard = Board(boardSize).body #this board counts the number of times each path is on each point, (with some extra conditions)

        for board in testBoards:
            jList = [0] #stores all possible j indices
            for i in range(boardSize):
                if len(jList) == 1:
                    countBoard[i][jList[0]] += 1
                else:
                    for j in jList:
                        if board.body[i][j] == -1:
                            countBoard[i][j] += 1
                newjList = []
                for j in jList:
                    pathChoice = board.pathArray[i][j][1]
                    if pathChoice == 0:
                        if len(newjList) == 0 or [-1] != j:
                            newjList.append(j)
                    elif pathChoice == 1:
                        newjList.append(j+1)
                    elif pathChoice == 2:
                        if len(newjList) == 0 or [-1] != j:
                            newjList.append(j)
                        newjList.append(j+1)

                jList = newjList #adds count to coutboard

        blankIndices = GameBoard.blankIndices()

        if len(blankIndices) == 0:
            stillPlaying = False
            continue

        move = blankIndices[0]
        maxHits = countBoard[move[0]][move[1]]

        for index in blankIndices[1:]:  #counts the point with the most hits
            if countBoard[index[0]][index[1]] > maxHits:
                move = index
                maxHits = countBoard[index[0]][index[1]]

        if maxHits == 0:
            GameOverCounter +=1
            if GameOverCounter == 5:
                stillPlaying = False
        else:
            GameOverCounter = 0


        playerTurn = random.choice([-1,1])

        GameBoard.body[move[0]][move[1]] = playerTurn

        for board in testBoards:
            board.setAndUpdate(move, playerTurn)

        #print("BoardList.append(Board(" + str(self.size) + "," + str(self.body) + "))")
        if printBoards:
            print(GameBoard)

    #game is over, will now return final conditions

    GameBoardCopy = copy.deepcopy(GameBoard)
    GameBoardCopy.randomizeBlanks()
    GameBoardCopy.updateWholePathArray()

    if printBoards:
        jList = [0] #stores all possible j indices
        for i in range(boardSize):
            for j in jList:
                GameBoard.body[i][j] *= 2
            newjList = []
            for j in jList:
                pathChoice = GameBoardCopy.pathArray[i][j][1]
                if pathChoice == 0:
                    if len(newjList) == 0 or [-1] != j:
                        newjList.append(j)
                elif pathChoice == 1:
                    newjList.append(j+1)
                elif pathChoice == 2:
                    if len(newjList) == 0 or [-1] != j:
                        newjList.append(j)
                    newjList.append(j+1)

            jList = newjList #adds count to coutboard

        print(GameBoard)

    print("Score is " + str(outputScoreToRealScore(boardSize,GameBoardCopy.pathArray[0][0][0])))

HammondGame(50,100,True)
