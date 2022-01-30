from SquareBoard5 import Board
import time
import numpy as np
import copy



def moving_end_point(n = 70, ensemble_size = 3):
    B = Board(n, ensemble_size)

    coord1 = (n - ensemble_size) * np.ones(2 * ensemble_size, dtype = np.int16)
    i = 0
    j = ensemble_size - 1

    coord2 = []
    while j >= 0:
        coord2 += [i,j]
        i += 1
        j -= 1

    coord = coord1 + np.array(coord2)

    inc = np.array(([i%2 for i in range(2*ensemble_size)]))

    while coord[-1] >= 0:
        B.highlight_path_from(tuple(coord), highlighting = True)
        print(B)
        B.highlight_path_from(tuple(coord), highlighting = False)
        coord -= inc
        time.sleep(0.1)

def changing_board(n = 30, ensemble_size = 2, framerate = 24, num_reps = 5):
    B = Board(n, ensemble_size)
    t_l = time.time()
    for i in range(num_reps):
        B.highlight_path_from_end(highlighting = True)
        # t_c =  time.time()
        # Dt = t_c - t_l
        # time.sleep(1./framerate - Dt)
        # t_l = time.time()
        print(B)
        B.highlight_path_from_end(highlighting = False)

        B.flip_random_and_update()

#moving_end_point(30,3)
# B = Board(30, ensemble_size = 2)
# # B.highlight_path_from_end()
# # print(B)
#
#
# B.highlight_path_from_end()
#
# print(B)
#

#moving_end_point(n = 30, ensemble_size = 4)
# changing_board(25,3, num_reps = 10**6)

#moving_end_point(n = 40, ensemble_size = 2)

#changing_board(n = 30, ensemble_size = 1, framerate = 24, num_reps  =500)


B = Board(50,2)
C = Board(50,1)
C.body = B.body
C.update_whole_path_array()

B.highlight_path_from_end()
C.highlight_path_from_end()
#print(B)
print(C)
