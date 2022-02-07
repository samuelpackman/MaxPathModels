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



def time_flip_disp(n = 50):
    num = 0
    B = Board(n)
    init_disp = B.disp_from_middle()

    def has_ended(disp,init):
        if init > 0:
            return disp <= - init
        elif init < 0:
            return disp >= - init
        elif init == 0:
            return True

    while not has_ended(B.disp_from_middle(), init_disp):
        num += 1
        B.flip_random_and_update()
        """if num%10 == 0:
            B.highlightPathFrom()
            print(B)
            B.unhighlightPathFrom()"""
    return (init_disp,num)

def time_flip_data(n = 100, reps = 100):
    init_data = []
    num_data = []
    for rep in range(reps):
        print(rep)
        datum = time_flip_disp(n)
        init_data.append(datum[0])
        num_data.append(datum[1])
    print("init data:")
    print(init_data)
    print("num data")
    print(num_data)

    plt.scatter(init_data, num_data)
    plt.xlabel('Initial Displacement')
    plt.ylabel('Number Random Flips')
    plt.show()

def init_disp_distrib(n=100, reps = 100):
    data = []
    for i in range(reps):
        B = Board(n)
        data.append(B.disp_from_middle())
    print(statistics.mean(data))
    plt.hist(data, bins = 20, density = True)
    plt.show()

time_flip_data(n = 50, reps = 20)
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
