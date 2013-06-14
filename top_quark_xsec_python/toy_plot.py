import numpy as np
import matplotlib.pylab as plt
import math
import sys

#====================================================
# Create scatter plot from input file
#====================================================

print sys.argv

# Read in the file from the command line
infile = None
if len(sys.argv)>1:
    infile = open(sys.argv[1],'r')
else:
    print "Need to pass in an input file for the first argument!!!!"
    exit(-1)


xpts = np.array([])
ypts = np.array([])

for line in infile:
    vals = line.split()
    x = float(vals[0])
    y = float(vals[1])

    xpts = np.append(xpts,x)
    ypts = np.append(ypts,y)


plt.scatter(xpts,ypts)
print sum(ypts)
#plt.ylim(0,500)
plt.show()
