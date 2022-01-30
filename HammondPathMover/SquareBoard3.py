import random
import time
import Colors

#In this file I will write the class board,
#as well as the mutateElement and getBestPath methods for it.

#linear transformation from form in parallelogram to body is i --> i, j --> j - i
#or (a,b) --> (a-b,b)
#inverse is i --> i, j --> j + i or (a,b) --> (a+b,b)

#board for ensemble size 2

class Board:

    def __init__(self, size):
        self.size = size

        self.body = [[0 for i in range(size)] for j in range(size)]

        self.ensemble_size = 2
        #path array is stored in parallelogram form 2 * size - 1 columns, each stores a diagonal of the Board
        self.path_array = [None for j in range(2 * size - 1)]
        #extra dimensions are added for each geodesic in the ensemble, they are restricted so that the
        #geodesics don't intersect

        def generate_grid(size):
            return [[None for i in range(j+1)] for j in range(size)]

        for i,grid in enumerate(self.path_array):
            #creates grid to store all possible ensemble configurations at this diagonal.
            #indexed by grid[a][b][c] ... a is position of first chord, b of second, etc.
            #must have restriction a > b > c > ... so that chords don't intersect
            if i < size:
                self.path_array[i]  = generate_grid(i + 1)
            else:
                self.path_array[i]  = generate_grid(-i + 2 * size - 1)
            #print(self.path_array[i])

        self.randomize_board()
        self.update_whole_path_array()

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


    def get_val_at_points(self,ind1,ind2):
        if ind1 < self.size:
            return sum([self.body[ind1-j][j] for j in ind2])
        else:
            """ind2_adj = ind2[0] + (self.size - 1) - (- ind1 + 2 * (self.size - 1))
            #adj = act + maximum should be attainable - maximum attainable by actual
            try:
                 a = self.body[ ind1 - ind2_adj]
            except IndexError:
                print(ind1_adj- ind2[0])
                print('len(self.body)')
                print(len(self.body))"""
            return sum([self.body[ ind1- (j - self.size + 1 + ind1 )][j - self.size + 1 + ind1 ] for j in ind2])

    def updatepath_array_at(self,ind1, ind2):
        #ind1, ind2 is of position in path array
        #ind1 is the diagonal the position is on
        #ind2 desribes the chords on the diagonal
        valid_moves = []

        changes = [[0,0], [0,1], [1,0], [1,1]]
        for change in changes:
            move = [ind2[j] - change[j] for j in range(len(change))]

            valid_move = True

            for j in range(2):
                if move[j] < 0:
                    valid_move = False

            if move[0] <= move[1]:
                valid_move = False

            if ind1 < self.size:
                if move[0] > ind1-1:
                    valid_move = False
            else:
                if move[0] > - ind1 + 2 * self.size:
                    valid_move = False

            if valid_move:
                valid_moves.append(move)

            #valid_moves_from_path_array = [self.path_array[ind1 - 1][move[0]][move[1]] for move in valid_moves]


        if len(valid_moves) == 0: #should only occur when all chords are adjacent on first or last possible diagonal
            self.path_array[ind1][ind2[0]][ind2[1]] = [self.get_val_at_points(ind1,ind2),[-1 for i in range(self.ensemble_size)]]

        else:
            best_move = valid_moves[0]
            score = self.path_array[ind1 - 1][best_move[0]][best_move[1]][0]
            for move in valid_moves[1:]:
                if self.path_array[ind1 - 1][move[0]][move[1]][0] > score:
                    best_move = move
                    score = self.path_array[ind1 - 1][move[0]][move[1]][0]
            self.path_array[ind1][ind2[0]][ind2[1]] = [score + self.get_val_at_points(ind1,ind2), best_move[1]]




    def updatepath_array_from(self,ind1):
        for k in range(ind1, 2 * self.size - self.ensemble_size):
            array = self.path_array[k]
            for i, row in enumerate(array):
                for j, col in enumerate(row):
                    self.updatepath_array_at(k, [i,j])

    def update_whole_path_array(self):
        self.updatepath_array_from(1)




    def highlight_path_from_dep(self,ind1, ind2):
        if ind1 < self.size:
            for j in ind2:
                self.body[ind1-j][j] *= 2
        else:
            for j in ind2:
                self.body[2 * ind1-2 * self.size + 1 - j][j - ind1 + 2 * self.size - 1] *= 2


        if self.path_array[ind1][ind2[0]][ind2[1]][1] != -1:
            print(self.path_array[ind1-1][ind2[0]][ind2[1]][j])
            self.highlight_path_from(ind1 - 1, [self.path_array[ind1-1][ind2[0]][ind2[1]][j] +  ind2[j] for j in range(len(ind2))])

    def highlight_path_from(self,ind1, ind2, highlighting = True):
        inds = {(ind1,tuple(ind2))}
        while len(inds) > 0:
            new_inds = set()
            for ind in inds:
                i = ind[0]
                js = ind[1]
                if highlighting:
                    if i < self.size:
                        for j in js:
                            if abs(self.body[i-j][j]) != 2:
                                self.body[i-j][j] *= 2
                    else:
                        for j in js:
                            if abs(self.body[2 * i-2 * self.size + 1 - j][j - i + 2 * self.size - 1]) != 2:
                                self.body[2 * i-2 * self.size + 1 - j][j - i + 2 * self.size - 1] *= 2
                else:
                    if i < self.size:
                        for j in js:
                            if abs(self.body[i-j][j]) == 2:
                                self.body[i-j][j] /= 2
                    else:
                        for j in js:
                            if abs(self.body[2 * i-2 * self.size + 1 - j][j - i + 2 * self.size - 1]) == 2:
                                self.body[2 * i-2 * self.size + 1 - j][j - i + 2 * self.size - 1] /= 2
                j0 = js[0]
                j1 = js[1]
                print(self.path_array[i])
                print(self.path_array[i][j0])
                print(self.path_array[i][j0][j1])
                move_val = self.path_array[i][j0][j1]
                if -1 not in move_val:
                    a = (i-1,tuple(move_val))
                    new_inds.add(a)
                else:
                    pass

            inds = new_inds



    def unhighlight_path_from(self,ind1, ind2):
        self.highlight_path_from(ind1, ind2, False)
