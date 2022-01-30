import numpy as np
def generate_grid(size,ensembleSize):
    if ensembleSize == 1:
        return [0 for i in range(size)]
    else:
        return [generate_grid(i ,ensembleSize - 1) for i in range(size)]

#print(generate_grid(2,2))

a = np.array([[0,1,2,3,4,5], [5,4,3,2,1,0], [-158,35,245,300,2000,301]])

a= np.reshape(a,(-1))
a=np.reshape(a,(-1,2))
print(a)

#b = a[np.all(a[0:-2:2] < a[2::2], axis = None)]#[np.all(a >= 0)]
# b = a[np.all(a >= 0, axis = 1)]
#
# c = a[np.logical_and(np.all(a[:,0:-2:2] < a[:,2::2], axis = 1), np.all(a >= 0, axis = 1))]
