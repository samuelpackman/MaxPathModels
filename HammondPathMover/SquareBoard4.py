import random
import time
import Colors
import numpy as np

#In this file I will write the class board,
#as well as the mutateElement and getBestPath methods for it.

#linear transformation from form in parallelogram to body is i --> i, j --> j - i
#or (a,b) --> (a-b,b)
#inverse is i --> i, j --> j + i or (a,b) --> (a+b,b)

#board for ensemble size 2

class Board:

    def __init__(self, size, ensemble_size = 2):
        self.size = size

        self.body = np.zeros((size,size), dtype = np.int8)

        self.ensemble_size = 2

        # 2*ensemble_size dimensional np array side lengths size
        self.move_array = np.zeros(tuple([size for i in range(2 * ensemble_size)] + [2 * ensemble_size]), dtype = np.int16)
        #stores the end locations of the moves not the 0/1 move values
        self.score_array = np.zeros(tuple([size for i in range(2 * ensemble_size)]), dtype = np.int16)
        #stores the score at each point

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
                self.body[(i,j)] = random.choice([-1,1]) #randomizes all positions in board

    def blank_indices(self):
        retList = []
        for i in range(self.size):
            for j in range(self.size):
                if self.body[(i,j)] == 0:
                    retList.append((i,j))  #finds black points

        return retList #finds black points

    def randomize_blanks(self):
        for i in self.blank_indices():
            self.body[i] = random.choice([-1,1])


    def get_score_at_points(self,i):
        return sum([self.body[i[j:j+2]] for j in range(0,2 * ensemble_size,2)])

    def updatepath_array_at(self,i):

        #i is position in move_array self.move_array[i] indexes the move
        valid_moves = []

        changes = np.array([
        [1,0,1,0],
        [1,0,0,1],
        [0,1,1,0],
        [0,1,0,1]
        ])
        l=0
        for change in changes:
            move = np.array(i) - change

            valid_move = True

            for j in move:
                if j < 0:
                    valid_move = False

            #order of chord conditions
            if move[0] >= move[2]:
                valid_move = False

            if valid_move:
                valid_moves.append(move)

        #print(valid_moves  )


        if len(valid_moves) == 0: #should only occur when all chords are adjacent on first or last possible diagonal
            self.move_array[i] = np.array([-1 for i in range(2* self.ensemble_size)])
            self.score_array[i] = sum([self.body[i[j:j+2]] for j in range(0,2 * self.ensemble_size,2)])

        else:


            best_move = valid_moves[0]
            best_move_score = self.score_array[tuple(best_move)]

            for move in valid_moves[1:]:
                move_score = self.score_array[tuple(move)]
                if move_score > best_move_score:
                    best_move = move
                    best_move_score = move_score
            self.move_array[i] = best_move
            self.score_array[i] = best_move_score + sum([self.body[i[j:j+2]] for j in range(0,2 * self.ensemble_size,2)])

    def updatepath_array_from(self,i):
        if type(i) == tuple:
            inds = {i}
        elif type(i) == set:
            inds = i

        changes = np.array([
        [1,0,1,0],
        [1,0,0,1],
        [0,1,1,0],
        [0,1,0,1]
        ])

        while len(inds) > 0:
            new_inds = set()
            for ind in inds:
                self.updatepath_array_at(ind)

                for change in changes:
                    next_ind = tuple(np.array(ind) + change)

                    valid_move  = True

                    #order of chord conditions
                    #ind[0] < ind[2] is the condition we are enforcing
                    if next_ind[0] >= next_ind[2]:
                        valid_move = False

                    for j in next_ind:
                        if j >= self.size:
                            valid_move = False

                    if valid_move:
                        new_inds.add(next_ind)

            inds = new_inds


    def update_whole_path_array(self):
        self.updatepath_array_from((0,1,1,0))


    def highlight_path_from(self, i, highlighting = True):
        inds = {i}

        while len(inds) > 0:
            new_inds = set()
            for ind in inds:
                for j in range(0, 2 * self.ensemble_size,2):
                    k = ind[j:j+2]

                    if highlighting == True:
                        if abs(self.body[k]) != 2:
                            self.body[k] *= 2
                    else:
                        if abs(self.body[k]) == 2:
                            self.body[k] /= 2

                next_ind = tuple(self.move_array[ind])

                if -1 not in next_ind:
                    for k in next_ind:
                        if k!= 0:
                            new_inds.add(next_ind)


            inds = new_inds

    def highlight_path_from_end(self, highlighting = True):
        self.highlight_path_from((self.size - 2, self.size -1, self.size -1, self.size - 2), highlighting)

    def unhighlight_path_from(self,ind1, ind2):
        self.highlight_path_from(ind1, ind2, False)

    def flip_random_and_update(self):
        i0 = random.randint(0, self.size - 1) #randind1 is ind3
        i1 = random.randint(0, self.size - 1)

        self.body[i0,i1] *= -1

        inds = set()
        #ind[0] < ind[2] is the condition we are enforcing

        i2 = i0 + 1 #i is ind[0]
        i3 = i1 - 1
        while i3 >= 0 and i2 < self.size:
            inds.add((i0,i1,i2,i3))
            i2 += 1
            i3 -= 1

        i2 = i0 - 1 #i is ind[0]
        i3 = i1 + 1
        while i2 >= 0 and i3 < self.size:
            inds.add((i2,i3,i0,i1))
            i3 += 1
            i2 -= 1

        self.updatepath_array_from(inds)
