from SquareBoard1 import Board
import sys
import time
import random
import copy
import time
import matplotlib.pyplot as plt

def track_area_changes(n = 70, do_print = False):
    ret_list = []
    B = Board(n)
    first = True
    for i in range(n):
        B.highlightPathFrom([n-1,n - 1 - i])

        if do_print and i < 3:
            print(B)
            time.sleep(0.01)

        new = B.num_under_path()
        if not first:
            ret_list.append(last - new)
        last = new
        first = False
        B.unhighlightPathFrom([n-1,n-1 - i])
    return ret_list

def gen_area_change_data(n = 100, reps = 100):
    ret_list = []
    for i in range(reps):
        ret_list += track_area_changes(n)
    return ret_list

def area_change_data():
    data  = gen_area_change_data(50,50)
    plt.hist(data, bins = 200, density = True)
    plt.yscale('log')
    plt.show()

area_change_data()
