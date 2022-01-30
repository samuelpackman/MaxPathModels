import random
import time
import Colors

#In this file I will write the class board,
#as well as the mutateElement and getBestPath methods for it.

#linear transformation from form in parallelogram to body is i --> i, j --> j - i
#or (a,b) --> (a-b,b)
#inverse is i --> i, j --> j + i or (a,b) --> (a+b,b)

class Board:

    def __init__(self, size, ensemble_size = 2):
        self.size = size

        self.body = [[0 for i in range(size)] for j in range(size)]

        self.ensemble_size = ensemble_size
        #path array is stored in parallelogram form 2 * size - 1 columns, each stores a diagonal of the Board
        self.path_array = [None for j in range(2 * size - 1)]
        #extra dimensions are added for each geodesic in the ensemble, they are restricted so that the
        #geodesics don't intersect

        def generate_grid(size,ensemble_size):
            if ensemble_size == 1:
                return [None for i in range(size)]
            else:
                return [generate_grid(i ,ensemble_size - 1) for i in range(size)]

        for i,grid in enumerate(self.path_array):
            #creates grid to store all possible ensemble configurations at this diagonal.
            #indexed by grid[a][b][c] ... a is position of first chord, b of second, etc.
            #must have restriction a > b > c > ... so that chords don't intersect
            if i < size:
                self.path_array[i]  = generate_grid(i + 1, ensemble_size)
            else:
                self.path_array[i]  = generate_grid(-i + 2 * size - 1 , ensemble_size)

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

    def randomize_board(self):
        for i in range(self.size):
            for j in range(self.size):
                self.body[i][j] = random.choice([-1,1]) #randomizes all positions in board

    def blank_indices(self):
        retList = []
        for i in range(self.size):
            for j in range(self.size):
                if self.body[i][j] == 0:
                    retList.append([i,j])  #finds black points

        return retList #finds black points

    def randomize_blanks(self):
        for i in self.blank_indices():
            self.body[i[0]][i[1]] = random.choice([-1,1])

    def getpath_array(self,ind1,ind2):
        #accesses a specific element of path_array
        #ind1, ind2 is of position in path array
        #ind1 is the diagonal the position is on
        #ind2 desribes the chords on the diagonal
        def helper(array, ind2):
            if len(ind2) == 1:
                return array[ind2[0]]
            else:
                return helper(array[ind2[0]], ind2[1:])

        return helper(self.path_array[ind1], ind2)

    def setpath_array(self, val, ind1, ind2):
        def helper(array, ind2):
            if len(ind2) == 1:
                array[ind2[0]] = val
            else:
                helper(array[ind2[0]], ind2[1:])

        helper(self.path_array[ind1], ind2)

    def updatepath_array_at(self,ind1, ind2):
        #ind1, ind2 is of position in path array
        #ind1 is the diagonal the position is on
        #ind2 desribes the chords on the diagonal
        valid_moves = []

        for i in range(2**len(ind2)):
            binary = bin(i)[2:]
            change = [int(j) for j in binary]
            move = [index[j] - change[j] for j in range(len(change))]

            valid_move = True

            for j in range(len(move) - 1):
                if move[j] <= move[j +1]:
                    valid_move = False

            if move[-1] < 0:
                valid_move = False

            if ind1 < self.size:
                if move[0] > ind1:
                    valid_move = False
            else:
                if move[0] > - ind1 + 2 * size - 1:
                    valid_move = False

            if valid_move:
                valid_moves.append(move)

            valid_moves_from_path_array = [self.getpath_array(ind1 - 1, move) for move in valid_moves]

        def get_val_at_points(self,ind1,ind2):
            if ind1 < self.size:
                return sum([self.body[ind1-j][j] for j in ind2])
            else:
                return sum([self.body[2 * ind1-2 * self.size + 1 - j][j - ind1 + 2 * size - 1] for j in ind2])

        if len(valid_moves) == 0: #should only occur when all chords are adjacent on first or last possible diagonal
            self.setpath_array([self.get_val_at_points(ind1,ind2),[-1 for i in range(self.ensemble_size)]], ind1, ind2)

        else:
            best_move = self.getpath_array(inf1 - 1, valid_moves[0])
            score = best_move[0]
            for move in valid_moves[1:]:
                if self.getpath_array(inf1 - 1, move)[0] > score:
                    best_move = self.getpath_array(inf1 - 1, move)
                    score = best_move[0]
            self.setpath_array(
            [score + self.get_val_at_points(ind1,ind2), best_move[1]], ind1, ind2)

    def updatepath_array_from_helper(self,array,ind1, ind2): #recursively accesses all elements of array and runs update_path_array_at
        if type(array[0]) == int:
            updatepath_array_at(self,ind1, ind2)
        else:
            if len(ind2) != 0:
                for i in range(ind2[-1] - 1):
                    self.updatepath_array_from_helper(array, ind1, ind2 + [i])
            else:
                for i in range(ind1 + 1):
                    self.updatepath_array_from_helper(array, ind1, [i])


    def updatepath_array_from(self,ind1):
        for i in range(ind1, 2 * self.size - self.ensemble_size):
            self.updatepath_array_from_helper(self.path_array[ind1], ind1, [])


    def update_whole_path_array(self):
        self.updatepath_array_from(self.ensemble_size-1)

    def highlight_path_from(self,ind1, ind2):
        print(ind2)
        if ind1 < self.size:
            for j in ind2:
                self.body[ind1-j][j] *= 2
        else:
            for j in ind2:
                self.body[2 * ind1-2 * self.size + 1 - j][j - ind1 + 2 * size - 1] *= 2

        if self.getpath_array(ind1,ind2)[1][0] == -1:
            return

        else:
            self.highlight_path_from(ind1 - 1, [self.getpath_array(ind1,ind2)[1][j] + ind2[j] for j in range(len(ind2))])


    def unhighlight_path_from(self,ind1, ind2):
        if ind1 < self.size:
            for j in ind2:
                self.body[ind1-j][j] /= 2
        else:
            for j in ind2:
                self.body[2 * ind1-2 * self.size + 1 - j][j - ind1 + 2 * size - 1] /= 2

        if self.getpath_array(ind1,ind2)[1][0] == -1:
            return

        else:
            self.highlight_path_from(ind1 - 1, [self.getpath_array(ind1,ind2)[1][j] + ind2[j] for j in range(len(ind2))])
