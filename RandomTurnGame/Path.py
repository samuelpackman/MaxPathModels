#in this class I write the pasth class
#stores the path information as well as the list of points on the pasth
#it also stores the path score
#it stores the start point as well

class Path:

    def __init__(self,score,path,start,size,pathList = None):
        self.score = score #score is sum of path elements, includes start
        self.path = path
        self.start = start #for [i,j] is the index of the start
        self.boardSize = size

        if pathList == None:
            self.pathList = [start] #list of points on path

            startInd = start

            i = start[0]
            while startInd[0] < size:
                startInd[0] += 1
                if path[i] == 1:
                    startInd[1] += 1
                i += 1
                self.pathList.append([startInd[0],startInd[1]])
        else:
            self.pathList = pathList
