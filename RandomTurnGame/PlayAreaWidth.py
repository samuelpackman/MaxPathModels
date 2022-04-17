from Board import Board
import matplotlib.pyplot as plt
import random
import sys
#from data import BoardListListList

#checks state of board at endpoint or when

def checkNumFilled(BoardList,halfwaypoint): #checks at halfway total number filled spaces
    count = 0
    tempBoard = BoardList[halfwaypoint]
    for i in tempBoard.body[tempBoard.size // 2]:
        if i != 0:
            count += 1
    return count

def checkFirstFilledLastFilled(BoardList,halfwaypoint): #checks at halfway total number filled spaces
    count = 0
    tempBoard = BoardList[halfwaypoint]
    lastFilled = -1
    firstFilled = -1
    for index, value in enumerate(tempBoard.body[tempBoard.size // 2]):
        if value != 0:
            lastFilled = index
            if firstFilled == -1:
                firstFilled = index
    return lastFilled - firstFilled + 1

def halfwaypointEnd(BoardList):
    return len(BoardList)//2

def halfwaypointFirstToEnd(BoardList):
    for index,board in enumerate(BoardList):
        lastRow = board.body[-1]
        for i in lastRow:
            if i != 0:
                return index //2
    print("something went wront in halfwaypointFirstToEnd")
    return halfwaypointEnd(BoardList) #failsafe if screws up for some reason

def findNumAcross(BoardList):
    return checkFirstFilledLastFilled(BoardList, halfwaypointEnd(BoardList))

def HammondGameOutputBoardList(boardSize = 100, sampleSize = 100):
    boardList = []

    GameOverCounter = 0

    GameBoard = Board(boardSize)

    testBoards = [Board(boardSize) for i in range(sampleSize)]
    for board in testBoards:
        board.randomizeBoard()
        board.updateWholePathArray()

    #setup is done

    stillPlaying = True

    while stillPlaying:
        boardList.append(GameBoard)

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

    return boardList

def createGraph(maxBoardSize = 100, numGamesPerSample = 1, sampleSize = 100):

    BoardListListList = []
    for boardSize in range(1,maxBoardSize+1):
        BoardListList = []
        for j in range(numGamesPerSample):
            BoardListList.append(HammondGameOutputBoardList(boardSize,sampleSize))
        BoardListListList.append(BoardListList)
        print(boardSize)

    data = []
    for BoardListList in BoardListListList:
        avg = 0
        for BoardList in BoardListList:
            avg += findNumAcross(BoardList)
        avg/=len(BoardListList)
        data.append(avg)

    plt.plot([0] + data)
    plt.show()

def CreateGameData(maxBoardSize = 100, numGamesPerSample = 1, sampleSize = 100):
    sys.stdout=open("/Users/Liz/Desktop/HammondGameSamRewrite/dataBoardSize200.txt","w")

    sys.stdout.truncate()


    for boardSize in range(1,maxBoardSize+1):
        print("BoardSize:" + str(boardSize))
        for j in range(numGamesPerSample):
            GameList = HammondGameOutputBoardList(boardSize,sampleSize)
            print("NewGame")
            for board in GameList:
                print(board.body)


    sys.stdout.close()

def createGraphFromData(BoardListListList):
    data = []
    for BoardListList in BoardListListList:
        avg = 0
        for BoardList in BoardListList:

            avg += findNumAcross(BoardList)
        avg/=len(BoardListList)
        data.append(avg)

    print(data)
    plt.plot([0] + data)
    plt.show()

CreateGameData(maxBoardSize = 106, numGamesPerSample = 5, sampleSize = 200)
