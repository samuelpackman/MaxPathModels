import random
import time
import Colors
import numpy as np
import itertools
import subset_sum
import math
#In this file I will write the class board,
#as well as the mutateElement and getBestPath methods for it.

#linear transformation from form in parallelogram to body is i --> i, j --> j - i
#or (a,b) --> (a-b,b)
#inverse is i --> i, j --> j + i or (a,b) --> (a+b,b)

#board for ensemble size 2

#pdf = e^-x
#int e^-x dx |_0^y = x x uniform
# 1 - e^ - y = x
# y = - ln(1-x)

class Board:

    def X_realize(self):
        # return - math.log(1-random.random()) #exponential distribution
        #return random.random() # uniform distribution
        return random.randrange(0,2)

    def __init__(self, size, ensemble_size = 2):

        self.size = size

        self.body = -1 * np.ones((size,size))

        self.ensemble_size = ensemble_size

        # 2*ensemble_size dimensional np array side lengths size
        self.move_array = np.zeros(tuple([size for i in range(2 * ensemble_size)] + [2 * ensemble_size]), dtype = np.int16)
        #stores the end locations of the moves not the 0/1 move values
        self.score_array = np.zeros(tuple([size for i in range(2 * ensemble_size)]))
        #stores the score at each point

        self.changes = np.zeros((2**ensemble_size, 2 * ensemble_size), dtype = np.int16)

        pos_changes = list(itertools.product([0, 1], repeat=ensemble_size))
        for i in range(2 ** ensemble_size):
            change = []
            for j in pos_changes[i]:
                if j == 0:
                    change += [0,1]
                else:
                    change += [1,0]
            self.changes[i] = np.array(change)



        self.randomize_board()
        self.update_whole_path_array(is_init = True)

    def __str__(self):
        retString = ""
        #for i in range(self.size-1,-1,-1):
            #for j in range(self.size - i):
                #char = self.body[i+j][j]


        for i in range(self.size):
            for j in range(self.size):
                char = self.body[self.size - 1 - i][j]


                if char==-1:
                    retString += Colors.bGray("~ ")
                #    retString += "  "
                elif char==1:
                    retString += "1 "
                    #retString += Colors.bRed("1 ")
                elif char == 0:
                    retString += "0 "
                    #retString += Colors.bBlue("0 ")
                elif char == 3: #2 and -2 are numbers on the path, they will be printed in yellow
                    retString += Colors.bOrange("1 ")
                elif char == 2:
                    retString += Colors.bOrange("0 ")
                else:
                    retString += (str(char)+" ")[0:2]
            retString += "\n"
        return retString #return body, formatted line by line

    def randomize_board(self):
        for i in range(self.size):
            for j in range(self.size):
                self.body[(i,j)] = self.X_realize() #randomizes all positions in board

    def blank_indices(self):
        ret_list = []
        for i in range(self.size):
            for j in range(self.size):
                if self.body[(i,j)] == 0:
                    ret_list.append((i,j))  #finds black points

        return ret_list #finds blank points (0s in self.body)

    def randomize_blanks(self):
        for i in self.blank_indices():
            self.body[i] = self.X_realize()

    def get_score_at_points(self,i):
        return sum([self.body[i[j:j+2]] for j in range(0,2 * self.ensemble_size,2)])

    def updatepath_array_at(self,i): #returns true if changes value, false else
        #i is position in move_array self.move_array[i] indexes the move
        # print(i)
        # print(np.tile(np.array(i), (2 ** self.ensemble_size, 1)))
        # print(self.changes)
        pos_moves = np.tile(np.array(i), (2 ** self.ensemble_size, 1)) - self.changes

        cond1 = np.all(pos_moves >= 0, axis = 1)
        cond2 = np.all(pos_moves[:,0:-2:2] < pos_moves[:,2::2], axis = 1)
        valid_moves = pos_moves[np.logical_and(cond1, cond2)]

        new_score = self.get_score_at_points(i)
        #sum([self.body[i[j:j+2]] for j in range(0,2 * self.ensemble_size,2)])

        if np.size(valid_moves) == 0: #should only occur when all chords are adjacent on first or last possible diagonal
            self.move_array[i] = np.tile(-1,(2* self.ensemble_size))

        else:
            move_scores = np.array([self.score_array[tuple(move)] for move in valid_moves])

            arg_max = np.argmax(move_scores)

            best_move = valid_moves[arg_max]
            best_move_score = move_scores[arg_max]


            # best_move = valid_moves[0]
            # best_move_score = self.score_array[tuple(best_move)]
            #
            # for move in valid_moves[1:]:
            #     move_score = self.score_array[tuple(move)]
            #     if move_score > best_move_score:
            #         best_move = move
            #         best_move_score = move_score


            self.move_array[i] = best_move
            new_score += best_move_score

        if self.score_array[i] == new_score:
            return False

        else:
            self.score_array[i] = new_score
            return True

    def updatepath_array_from_inds(self,inds, is_init = False):
        num_calls = 0
        while len(inds) > 0:
            new_inds = set()
            for ind in inds:
                num_calls += 1

                has_changed = self.updatepath_array_at(ind)

                if has_changed or is_init:

                    # pos_next_inds = np.tile(np.array(ind), (2 ** self.ensemble_size, 1)) + self.changes
                    #
                    # valid_inds = pos_next_inds[np.all(pos_next_inds < self.size) and np.all(pos_next_inds[0:-2:2] < pos_next_inds[2::2])]
                    #
                    # for valid in valid_inds:
                    #     new_inds.add(tuple(valid))
                    pos_moves = np.tile(np.array(ind), (2 ** self.ensemble_size, 1)) + self.changes

                    cond1 = np.all(pos_moves < self.size , axis = 1)
                    cond2 = np.all(pos_moves[:,0:-2:2] < pos_moves[:,2::2], axis = 1)
                    valid_moves = pos_moves[np.logical_and(cond1, cond2)]

                    for move in valid_moves:
                        new_inds.add(tuple(move))

                    #for change in self.changes:
                        # next_ind = tuple(np.array(ind) + change)
                        #
                        # valid_move  = True
                        #
                        # #order of chord conditions
                        # #ind[0] < ind[2] is the condition we are enforcing
                        # for j in range(0,2 * self.ensemble_size-2,2):
                        #     if next_ind[j] >= next_ind[j+2]:
                        #         valid_move = False
                        #
                        # for j in next_ind:
                        #     if j >= self.size:
                        #         valid_move = False
                        #
                        # if valid_move:
                        #     new_inds.add(next_ind)



            inds = new_inds
        #print("num_calls:" + str(num_calls))

    def updatepath_array_from(self, i, is_init = False):
        self.updatepath_array_from_inds({i}, is_init)

    def update_whole_path_array(self, is_init = False):
        t_0 = time.time()
        #sum of values in each pair should add to #ensemble-1
        i = 0
        j = self.ensemble_size - 1

        coord = []
        while j >= 0:
            coord += [i,j]
            i += 1
            j -= 1

        self.updatepath_array_from(tuple(coord), is_init)
        #print(time.time() - t_0)

    def highlight_path_from(self, i, highlighting = True):
        inds = {i}

        while len(inds) > 0:
            new_inds = set()
            for ind in inds:
                for j in range(0, 2 * self.ensemble_size,2):
                    k = ind[j:j+2]

                    if highlighting == True:
                        self.body[k] = self.body[k] % 2 + 2
                    else:
                        self.body[k] = self.body[k] % 2

                next_ind = tuple(self.move_array[ind])

                if -1 not in next_ind:
                    new_inds.add(next_ind)

            inds = new_inds

    def highlight_path_from_end(self, highlighting = True):
        coord1 =  np.tile((self.size - self.ensemble_size), 2 * self.ensemble_size)
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

    def flip_random_and_update(self):
        i = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
        val = self.X_realize()
        self.flip_coord_and_update(i, val)
        
    
    def flip_coord_and_update(self, i, val):
        self.body[i] = val

        update_inds = set()
        for ind in self.find_inds_from_bodyind(i):
            update_inds.add(tuple(ind))
        self.updatepath_array_from_inds(update_inds, is_init = False)
        
        
    def find_inds_from_bodyind(self,body_ind):
        tuple_list = []

        for place in range(self.ensemble_size):
            smaller_inds = subset_sum.inc_seq(0, body_ind[0], place)
            bigger_inds = subset_sum.inc_seq(body_ind[0] + 1, self.size, self.ensemble_size - 1 - place)


            for i_smaller in smaller_inds:
                for i_bigger in bigger_inds:
                    ret_tuple = ()

                    for j in i_smaller:
                        ret_tuple += (j, body_ind[0] + body_ind[1] - j)
                    ret_tuple += body_ind

                    for j in i_bigger:
                        ret_tuple += (j, body_ind[0] + body_ind[1] - j)

                    tuple_list.append(ret_tuple)

        tuple_list = np.array(tuple_list)
        return tuple_list[np.all(tuple_list < self.size, axis = 1)]


    def scores_from(self, i, highlighting = True):
        scores = np.zeros(self.ensemble_size)

        inds = {i}

        while len(inds) > 0:
            new_inds = set()
            for ind in inds:
                for j in range(0,self.ensemble_size):
                    k = ind[2 * j:2 * j+2]

                    scores[j] += self.body[k]



                next_ind = tuple(self.move_array[ind])

                if -1 not in next_ind:
                    new_inds.add(next_ind)

            inds = new_inds

        return scores



    def moving_end_point(self):

        coord1 = (self.size - self.ensemble_size) * np.ones(2 * self.ensemble_size, dtype = np.int16)
        i = 0
        j = self.ensemble_size - 1

        coord2 = []
        while j >= 0:
            coord2 += [i,j]
            i += 1
            j -= 1

        coord = coord1 + np.array(coord2)

        inc = np.array(([i%2 for i in range(2*self.ensemble_size)]))

        while coord[-1] >= 0:
            yield self.scores_from(tuple(coord))
            coord -= inc
