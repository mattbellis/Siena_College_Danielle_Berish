import numpy as np
import matplotlib.pylab as plt
import math
import sys

#==========================================================

def events(n,tag="default"):
    #outfilename = "sum_events_%s.dat" % (tag)
    #f = open(outfilename,'w+')
    output = ""

    #xpts = np.array([])
    ypts = np.array([])

    for line in n:
        vals = line.split()
        #x = float(vals[0])
        y = float(vals[1])

        #xpts = np.append(xpts,x)
        ypts = np.append(ypts,y)

    total = sum(ypts)
    output = "%f" % (total)
    print output
    #f.write(output)
    #f.close()


#===========================================================
# Read in the file from the command line
infile = None
if len(sys.argv)>1:
    infile = open(sys.argv[1],'r')
else:
    print "Need to pass in an input file for the first argument!!!!"
    exit(-1)

tag = sys.argv[1].split('/')[-1].split('.')[0]

events(infile,tag)
