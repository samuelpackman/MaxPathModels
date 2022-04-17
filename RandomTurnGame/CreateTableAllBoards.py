def CreateTableHelper(tempBody): #creates table of best path value for every board state
        if Board(len(tempBody),tempBody).isFilled():
            return Board(len(tempBody),tempBody).findBestPathScore()
        else:
            tempBody1 = copy.deepcopy(tempBody)
            tempBody2 = copy.deepcopy(tempBody)
            i=0
            j=-1
            while tempBody[i][j] != 0:
                j+=1
                if i < j:
                    i+=1
                    j=0

            tempBody1[i][j] = 1
            tempBody2[i][j] = -1
            return [CreateTableHelper(tempBody1),CreateTableHelper(tempBody2)]

def CreateTable(size1):
    body = Board(size1).body
    return CreateTableHelper(body)
