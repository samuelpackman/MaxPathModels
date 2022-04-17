from SquareBoard7 import Board
import time
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.axes as axes

#/Users/Liz/Documents/HammondProjectMasterFolder/HammondPathMover/intersecting_trees.py

def create_trees(n = 50):
    B = Board(n, 1)

    print_tree = False
    print_complement = False
    print_peano_curve = True

    for i in range(n):
        for j in range(n):
            move = B.move_array[i,j]

            if i != 0 or j!= 0:

                if print_tree:
                    plt.plot([j, move[1]], [i, move[0]], color = "blue")

                move_is_horiz = (move[0] == i)

                if print_complement:
                    if i != 0 and j != 0:
                        plt.plot(np.array([j, move[1]]) - 0.5 + move_is_horiz , np.array([i, move[0]]) + 0.5 - move_is_horiz, color = "orange")

                if print_peano_curve:
                    if move[0] == i:
                        if i != 0 and j != 0:

                            #black group adjacent to oranges
                            for k in (0,0.5):
                                plt.plot(np.array([j + 0.25, move[1] + 0.75]) , np.array([i - 0.25, move[0] - 0.25]) - k, color = "black")

                        #black group adjacent to blues
                        plt.plot([j - 0.25, move[1] + 0.25] , [i + 0.25, move[0] + 0.25], color = "black")
                        if i != 0:
                            plt.plot([j - 0.25, move[1] + 0.25] , [i - 0.25, move[0] - 0.25], color = "black")

                    else:
                        if i != 0 and j != 0:

                            #black group adjacent to oranges
                            for k in (0,0.5):
                                plt.plot(np.array([j - 0.25, move[1] - 0.25]) - k , np.array([i + 0.25, move[0] + 0.75]), color = "black")

                        #black group adjacent to blues
                        plt.plot([j + 0.25, move[1] + 0.25] , [i - 0.25, move[0] + 0.25], color = "black")
                        if j != 0:
                            plt.plot([j - 0.25, move[1] - 0.25] , [i - 0.25, move[0] + 0.25], color = "black")

    if print_complement:
        plt.plot([0.5, n - 0.5], [n - 0.5, n - 0.5], color = "orange")
        plt.plot([n - 0.5, n - 0.5], [0.5, n - 0.5], color = "orange")

    if print_peano_curve:
        for i in range(n-1):
            plt.plot([0.75 + i, 1.25 + i], [n - 0.75, n - 0.75], color = "black")
            plt.plot([n - 0.75, n - 0.75], [0.75 + i, 1.25 + i], color = "black")
    plt.axis("equal")
    #axes.set_aspect('equal', adjustable='box')
    plt.show()

create_trees(50)
