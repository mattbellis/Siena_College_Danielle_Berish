import numpy as np
import matplotlib.pylab as plt
import math
import sys

#======================================================

print sys.argv

def cocktail(n):

    #vals = np.loadtxt(n)
    #vals.swapaxes(1,0)

    #xpts = vals[0]
    #ypts = vals[1]

    xpts = np.array([])
    ypts = np.array([])

    #'''
    for line in n:
        vals = line.split()
        x = float(vals[0])
        y = float(vals[1])

        xpts = np.append(xpts,x)
        ypts = np.append(ypts,y)
    #'''

    return ypts,xpts


#================================================================
# Read in the file from the command line
#================================================================

#===============================================================================================
# ttbar
infile_0 = None
if len(sys.argv)>1:
    infile_0 = open(sys.argv[1],'r')
else:
    print "Need to pass in an input file for the first argument!!!!"
    exit(-1)
    
# Wjets
infile_1 = None
if len(sys.argv)>1:
    infile_1 = open(sys.argv[2],'r')
else:
    print "Need to pass in an input file for the first argument!!!!"
    exit(-1)

# QCD
infile_2 = None
if len(sys.argv)>1:
    infile_2 = open(sys.argv[3],'r')
else:
    print "Need to pass in an input file for the first argument!!!!"
    exit(-1)

# t
infile_3 = None
if len(sys.argv)>1:
    infile_3 = open(sys.argv[4],'r')
else:
    print "Need to pass in an input file for the first argument!!!!"
    exit(-1)

# tbar
infile_4 = None
if len(sys.argv)>1:
    infile_4 = open(sys.argv[5],'r')
else:
    print "Need to pass in an input file for the first argument!!!!"
    exit(-1)

#===================================================================================================


ttpts,xpts = cocktail(infile_0)
tot_pts = ttpts.copy()

wjetspts,xpts = cocktail(infile_1)
tot_pts += wjetspts

qcdpts,xpts = cocktail(infile_2)
tot_pts += qcdpts

tpts,xpts = cocktail(infile_3)
tot_pts += tpts 

tbarpts,xpts = cocktail(infile_4)
tot_pts += tbarpts
#===================================================================================================

tag = sys.argv[1].split('/')[-1].split('.')[0]
tag = str(tag)
name = tag[-5:]

outfilename = "toy_cocktail_output_%s.dat" % (name)
f = open(outfilename, 'w')
output = ""

#xpts = np.array([])
for x,y in zip(xpts,tot_pts):
    
    output = "%f %f\n" % (x,y)
    
    f.write(output)

f.close()

