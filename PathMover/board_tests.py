from SquareBoard import Board
import time
import numpy as np
import copy
import matplotlib.pyplot as plt


#these mostly run fairly quickly for n < 40 and ensemble_size <= 3, but for larger n slows down
#and for larger ensemble_size slows down very quickly

#initializes the board, then drags the endpoint of the ensemble
# from the top right to the top left and displays the transtions
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


#initializes board, then repeatedly flips random grid points and updates the ensemble
def changing_board(n = 30, ensemble_size = 2, framerate = 24, num_reps = 5):
    B = Board(n, ensemble_size)
    t_l = time.time()
    for i in range(num_reps):
        B.highlight_path_from_end(highlighting = True)
        print(B)
        B.highlight_path_from_end(highlighting = False)

        B.flip_random_and_update()


#initializes reps number of boards with ensemble size 1, then
#creates a histogram of the displacements of the curves from the diagonal
def init_disp_distrib(n=100, reps = 100):
    data = []
    for i in range(reps):
        B = Board(n)
        data.append(B.disp_from_middle())
    print(statistics.mean(data))
    plt.hist(data, bins = 20, density = True)
    plt.show()


#number of times a random space on the board is flipped
#for position of middle of path to fully switch over diagonal
#this runs very slowly for large n, normally computer must be left to run for moderate size tests
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

    return (init_disp,num)

#creates scatterplot of time_flip_disp for many iterations
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




def track_area_changes(n = 70, do_print = False):
    #tracks the changes in the area underneath the curve as the endpoint moves from top right to top left
    #returns a list of the changes
    ret_list = []
    B = Board(n, ensemble_size = 1)
    first = True
    for i in range(n):
        B.highlight_path_from(tuple((n-1,n - 1 - i)))

        if do_print and i < 3:
            print(B)
            time.sleep(0.01)

        new = B.num_under_path()
        if not first:
            ret_list.append(last - new)
        last = new
        first = False
        B.highlight_path_from(tuple((n-1,n-1 - i)), False)
    return ret_list


def gen_area_change_data(n = 100, reps = 100):
    #appends multiple datasets from track_area_changes to make larger data set

    ret_list = []
    for i in range(reps):
        ret_list += track_area_changes(n)
    return ret_list

def area_change_data():
    #graphs data generated in gen_area_change_data

    data  = gen_area_change_data(50,50)
    plt.hist(data, bins = 200, density = True)
    plt.yscale('log')
    plt.show()
