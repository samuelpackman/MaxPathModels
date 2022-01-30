from SquareBoard1 import Board
import sys
import time
import random
import copy
import time
import matplotlib.pyplot as plt
import statistics


def moving_end_point(n = 70):
    B = Board(n)
    B.randomizeBlanks()
    B.updateWholePathArray()


    for i in range(n):
        B.highlightPathFrom([n-1,n - 1 - i])
        print(B)
        B.unhighlightPathFrom([n-1,n-1 - i])
        time.sleep(0.1)

def changing_board(n = 70):
    framerate = 24
    B = Board(n)
    t_l = time.time()
    for i in range(10 ** 4):
        B.highlightPathFrom(highlighting = True)
        t_c =  time.time()
        Dt = t_c - t_l
        print(Dt)
        time.sleep(1./framerate - Dt)
        t_l = time.time()
        print(B)
        B.highlightPathFrom(highlighting = False)
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

#init_disp_distrib(reps = 100)

#changing_board(50)
