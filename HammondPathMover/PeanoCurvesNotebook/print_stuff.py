import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
from matplotlib import collections  as mc

def show_trees(tree_segments, gem_tree_segments, peano_curve_segments):

    segments = tree_segments+gem_tree_segments + peano_curve_segments
    color_list = ["blue" for i in tree_segments] + ["orange" for i in gem_tree_segments] + ["black" for i in peano_curve_segments]
    lc = mc.LineCollection(segments, colors=color_list, linewidths=1)
    fig, ax = pl.subplots()
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)

    plt.axis("equal")
    plt.show()


def show_curve(points):
    segments = [[points[i], points[i+1]] for i in range(len(points) - 1)]
    color_list = ["black" for i in segments]
    lc = mc.LineCollection(segments, colors=color_list, linewidths=1)
    fig, ax = pl.subplots()
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)

    plt.axis("equal")
    plt.show()
