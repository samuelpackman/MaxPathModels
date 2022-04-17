from Board import Board
import copy
import matplotlib.pyplot as plt
from Graphs import Graphs
import math

#Give plot a snazzy title
plt.suptitle("Graphs of Score Values For Each End Point")

circleGraph = []

avgMaxVal = 0
for graph in Graphs:
    avgMaxVal += max(graph)/50

for i in range(200):
    circleGraph.append(
    (avgMaxVal - 100)/100 * math.sqrt(10000 - (i-99.5)**2)+100
    )



#Itterate through bridges and plot them
for num in range(len(Graphs)):
    #"cd" into the correct subplot
    plt.subplot(10,10,num+1)
    #Remove the (honestly distracting) numbers next to graphs
    plt.xticks([])
    plt.yticks([])
    #Plot the "bodies" (i.e actual numbers) of the bridges
    #newGraph = [
    #math.sqrt(abs(10000 - ((100/(avgMaxVal - 100)) * (x - 100))**2))
    #for x in Graphs[num]
    #]
    plt.plot(Graphs[num])
    plt.plot(circleGraph)


#Finish this first graph by rendering it
plt.show()

#Go through each bridge and do the repeated addition algorithm 10,000 times


exit()

def main(size):
    testBoard = Board(size)
    testBoard.randomizeBoard()

    retList = []

    for i in range(size):
        tempBoard = copy.deepcopy(testBoard)
        for j in range(size):
            if j != i:
                tempBoard.body[size - 1][j] = - size - 1
        retList.append(int((tempBoard.findBestPathScore() + size)/2))
    return retList


for i in range(50):
    print(main(200))

GraphingArray = main(100)
print(GraphingArray)

#Choose the size we want for our bridges
#Get a set of 100 random bridges of size N
#Give plot a snazzy title
plt.suptitle("Graphs of Score Values For Each End Point")

    #"cd" into the correct subplot
    #Remove the (honestly distracting) numbers next to graphs

    #Plot the "bodies" (i.e actual numbers) of the bridges
plt.plot(GraphingArray)

#Finish this first graph by rendering it
plt.show()

#Go through each bridge and do the repeated addition algorithm 10,000 times
