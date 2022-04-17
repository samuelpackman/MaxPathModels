import random
from Board import Board
import copy

def HammondStrategy(body,numSamples = 100,printTrue = False):
    #implements Hammmond's strategy, counts -1 if on any best path, counts 1 if on sole best path
    #will use statistical test to make sure finds correct answer
    #account for when one point on all paths


    size = len(body)
    countBoard = Board(size)
    tempBoard = Board(size,copy.deepcopy(body))
    blankIndices  = tempBoard.blankIndices()

    for s in range(numSamples):
        for i in blankIndices:
            tempBoard.body[i[0]][i[1]] = random.choice([-1,1])

        paths = tempBoard.findBestPathAllPaths()[0][1:] #optimal path

        countBoardCopy = copy.deepcopy(countBoard)

        c = 0
        for path in paths:
            c += 1
            j = 0
            for i in range(size-1):
                if [i,j] in blankIndices:
                    if tempBoard.body[i][j] == -1:
                        countBoard.body[i][j] = countBoardCopy.body[i][j] + 1
                    countBoardCopy.body[i][j] += 1

                    if c == len(paths) and tempBoard.body[i][j] == 1 and countBoardCopy.body[i][j] == c + countBoard.body[i][j]:
                        countBoard.body[i][j] += 1

                j += path[i]
            if [size -1,j] in blankIndices:
                if tempBoard.body[size - 1][j] == -1:
                    countBoard.body[size - 1][j] = countBoardCopy.body[size-1][j] + 1
                countBoardCopy.body[size - 1][j] += 1
                if c == len(paths) and tempBoard.body[size - 1][j] == 1 and countBoardCopy.body[size - 1][j] == c + countBoard.body[size -1][j]:
                    countBoard.body[size - 1][j] += 1


    retInd = blankIndices[0]
    maxHits = countBoard.body[retInd[0]][retInd[1]]

    if printTrue:
        print(countBoard)

    for index in blankIndices[1:]:  #counts the point with the most hits
        if countBoard.body[index[0]][index[1]] > maxHits:
            retInd = index
            maxHits = countBoard.body[index[0]][index[1]]

    global GameOverCounter

    if maxHits == 0:
        GameOverCounter +=1
        if GameOverCounter == 5:
            return retInd + [True]
    else:
        GameOverCounter = 0

    return retInd #should be optimal for large sample size, plan to implement p-test
