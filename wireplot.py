from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

import pickle

with open('plot_data.dat', 'rb') as f:
    alldata = pickle.load(f)
 
X = []
Y = []
Z = [] 
 
for index_i,i in enumerate([2, 4, 6, 8, 10, 15, 20, 30, 50, 100]):
    x = []
    y = []
    z = []
    for index_j, j in enumerate(range(15)):        
        x.append(i)
        y.append(j + 1)
        z.append( alldata[index_i*15 + j] )
    Y.append(x)
    X.append(y)
    Z.append(z)
  

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#X, Y, Z = axes3d.get_test_data(0.05)
print Y
#ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
ax.plot_surface(X, Y, Z,  rstride=1, cstride=1, color='b')

plt.show()

