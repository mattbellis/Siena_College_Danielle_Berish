import numpy as np
import matplotlib.pylab as plt
import math

import sys

def combinations(njets,ngroup):
    numer = math.factorial(njets)
    denom = math.factorial(ngroup)*math.factorial(njets-ngroup)

    return numer/denom


print sys.argv

# Read in the file from the command line
infile = None
if len(sys.argv)>1:
    infile = open(sys.argv[1],'r')
else:
    print "Need to pass in an input file for the first argument!!!!"
    exit(-1)

mass = np.zeros(500000)

i = 0
for line in infile:
    vals = line.split()
    #print vals
    if len(vals)>=4:
        mass[i] = float(vals[0])
        i += 1

plt.hist(mass[mass>0],bins=500)
plt.show()
