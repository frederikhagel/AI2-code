from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.gca(projection='3d')

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
    
X = np.array(X)
Y = np.array(Y)
Z = np.array(Z)   
    
    
    
xlen = len(X)
ylen = len(Y)    
    
colortuple = ('y', 'b')
colors = np.empty(X.shape, dtype=str)
for y in range(ylen):
    for x in range(xlen):
        colors[x, y] = colortuple[(x + y) % len(colortuple)]

surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1)

ax.set_zlim3d(-1, 1)
ax.w_zaxis.set_major_locator(LinearLocator(6))

plt.show()

