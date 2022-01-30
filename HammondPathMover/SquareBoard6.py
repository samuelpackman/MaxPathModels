import random
import time
import Colors
import numpy as np
import itertools
import sparse as sp

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

        self.ensemble_size = ensemble_size

        # 2*ensemble_size dimensional np array side lengths size
        self.move_array = np.zeros(tuple([size for i in range(2 * ensemble_size)] + [2 * ensemble_size]), dtype = np.int16)
        #stores the end locations of the moves not the 0/1 move values
        self.move_choice_array = sp.COO(np.zeros(tuple([size for i in range(2 * ensemble_size)]), dtype = tuple))

        self.score_array = np.zeros(tuple([size for i in range(2 * ensemble_size)]), dtype = np.int16)
        #stores the score at each point

        self.changes = np.zeros((2**ensemble_size, 2 * ensemble_size), dtype = np.int16)
        print(-1)
        pos_changes = list(itertools.product([0, 1], repeat=ensemble_size))
        for i in range(2 ** ensemble_size):
            change = []
            for j in pos_changes[i]:
                if j == 0:
                    change += [0,1]
                else:
                    change += [1,0]
            self.changes[i] = np.array(change)


        print(0)
        self.randomize_board()
        print(1)
        self.init_move_choice_array()
        print(2)
        self.update_whole_path_array()
        print(3)

    def init_move_choice_array(self):
        i = 0
        j = self.ensemble_size - 1

        coord = ()
        while j >= 0:
            coord += (i,j)
            i += 1
            j -= 1


        inds = {coord}
        while len(inds) > 0:
            new_inds = set()
            for ind in inds:
                #put relevant code here to do thing
                move_choices = []
                for change in self.changes:
                    move = np.array(ind) - change

                    valid_move = True

                    for j in move:
                        if j < 0:
                            valid_move = False

                for j in range(0,2 * self.ensemble_size-2,2):
                    if move[j] >= move[j+2]:
                        valid_move = False

                if valid_move:
                    move_choices.append(tuple(move))

                self.move_choice_array[ind] = move_choices

                for change in self.changes:
                    next_ind = tuple(np.array(ind) + change)

                    valid_move  = True

                    #order of chord conditions
                    #ind[0] < ind[2] is the condition we are enforcing
                    for j in range(0,2 * self.ensemble_size-2,2):
                        if next_ind[j] >= next_ind[j+2]:
                            valid_move = False

                    for j in next_ind:
                        if j >= self.size:
                            valid_move = False

                    if valid_move:
                        new_inds.add(next_ind) #finds next inds to update

            inds = new_inds


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
        ret_list = []
        for i in range(self.size):
            for j in range(self.size):
                if self.body[(i,j)] == 0:
                    ret_list.append((i,j))  #finds black points

        return ret_list #finds blank points (0s in self.body)

    def randomize_blanks(self):
        for i in self.blank_indices():
            self.body[i] = random.choice([-1,1])

    def get_score_at_points(self,i):
        return sum([self.body[i[j:j+2]] for j in range(0,2 * ensemble_size,2)])

    def updatepath_array_at(self,i):
        time_0 = time.time()
        #i is position in move_array self.move_array[i] indexes the move
        valid_moves = self.move_choice_array[i]

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
        inds = {i}
        num_calls = 0
        while len(inds) > 0:
            new_inds = set()
            for ind in inds:
                num_calls += 1
                self.updatepath_array_at(ind)

                for change in self.changes:
                    next_ind = tuple(np.array(ind) + change)

                    valid_move  = True

                    #order of chord conditions
                    #ind[0] < ind[2] is the condition we are enforcing
                    for j in range(0,2 * self.ensemble_size-2,2):
                        if next_ind[j] >= next_ind[j+2]:
                            valid_move = False

                    for j in next_ind:
                        if j >= self.size:
                            valid_move = False

                    if valid_move:
                        new_inds.add(next_ind)

            inds = new_inds
        print("num_calls:" + str(num_calls))


    def update_whole_path_array(self):
        t_0 = time.time()
        #sum of values in each pair should add to #ensemble-1
        i = 0
        j = self.ensemble_size - 1

        coord = []
        while j >= 0:
            coord += [i,j]
            i += 1
            j -= 1

        self.updatepath_array_from(tuple(coord))
        print(time.time() - t_0)


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
                    new_inds.add(next_ind)


            inds = new_inds

    def highlight_path_from_end(self, highlighting = True):
        coord1 = (self.size - self.ensemble_size) * np.ones(2 * self.ensemble_size, dtype = np.int16)
        i = 0
        j = self.ensemble_size - 1

        coord2 = []
        while j >= 0:
            coord2 += [i,j]
            i += 1
            j -= 1

        coord = coord1 + np.array(coord2)
        self.highlight_path_from(tuple(coord), highlighting)

    def unhighlight_path_from(self,ind1, ind2):
        self.highlight_path_from(ind1, ind2, False)

    #don't use yet for ensemble_size != 2
    def flip_random_and_update(self):
        i0 = random.randint(0, self.size - 1)
        i1 = random.randint(0, self.size - 1)
        self.body[i0,i1] *= -1
        self.update_whole_path_array()
