import copy
import random
from SquareBoard import SquareBoard
from SquareBoardHammondStrategy import SquareBoardHammondStrategy

size = 20
Board = SquareBoard(size)
Board.randomizeHalfBoard()
countBoard = SquareBoard(size)
tempBoard = SquareBoard(size,copy.deepcopy(Board.body))
blankIndices  = tempBoard.blankIndices()
numSamples = 100


for s in range(numSamples):
    for i in blankIndices:
        tempBoard.body[i[0]][i[1]] = random.choice([-1,1])

    paths = tempBoard.findBestPathAllPaths()[0][1:] #optimal path

    countBoardCopy = copy.deepcopy(countBoard)

    c = 0
    for path in paths:
        c += 1
        j = 0
        for i in range(2 * size - 2):
            if [i,j] in blankIndices:
                if tempBoard.body[i][j] == -1:
                    countBoard.body[i][j] = countBoardCopy.body[i][j] + 1
                countBoardCopy.body[i][j] += 1

                if c == len(paths) and tempBoard.body[i][j] == 1 and countBoardCopy.body[i][j] == c + countBoard.body[i][j]:
                    countBoard.body[i][j] += 1

            j += path[i]
            if i >= size - 1:
                j -= 1
        if [2 * size -2,0] in blankIndices:
            if tempBoard.body[2 * size - 2][0] == -1:
                countBoard.body[2 * size - 2][0] = countBoardCopy.body[2 * size - 2][0] + 1
            countBoardCopy.body[2 * size - 2][0] += 1
            if c == len(paths) and tempBoard.body[2 * size - 2][0] == 1 and countBoardCopy.body[2 * size - 2][0] == c + countBoard.body[2 * size - 2][0]:
                countBoard.body[2 * size - 2][0] += 1


print(countBoard.printAllNums())
