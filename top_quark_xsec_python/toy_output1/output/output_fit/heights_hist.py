import numpy as np
import matplotlib.pylab as plt
import math
import sys

#====================================================
# Create histogram of number of events of ttbar
#====================================================

print sys.argv

# Read in the file from the command line
infile = None
if len(sys.argv)>1:
    infile = open(sys.argv[1],'r')
else:
    print "Need to pass in an input file for the first argument!!!!"
    exit(-1)

ypts = np.array([])

for n in infile:
    ypts = np.append(ypts,float(n))


print "mean: ", np.mean(ypts)
print "std dev: ", np.std(ypts)

plt.hist(ypts,50)
plt.show()
