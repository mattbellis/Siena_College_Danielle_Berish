import numpy as np
import matplotlib.pylab as plt
import math
import sys

print sys.argv

################################################################################
def scale(n,t):
    xpts = np.array([])
    ypts = np.array([])
    new_ypts = np.array([])
    total = 0

    for line in n:
        vals = line.split()
        x = float(vals[0])
        y = float(vals[1])

        xpts = np.append(xpts,x)
        ypts = np.append(ypts,y)

    for i in ypts:
        new_y = i*(t/sum(ypts))
        new_ypts = np.append(new_ypts,new_y)
        total += new_y
        
    print total
    return new_ypts,xpts
    

#================================================================
# Read in the file from the command line
#================================================================

#================================================================
# ttbar
infile_0 = None
if len(sys.argv)>1:
    infile_0 = open(sys.argv[1],'r')
else:
    print "Need to pass in an input file for the first argument!!!!"
    exit(-1)   


ttpts,xpts = scale(infile_0,20000)
tot_pts = ttpts.copy()

#================================================================
# Wjets
infile_1 = None
if len(sys.argv)>1:
    infile_1 = open(sys.argv[1],'r')
else:
    print "Need to pass in an input file for the first argument!!!!"
    exit(-1)
    
wjetspts,xpts = scale(infile_1,2500)
tot_pts += wjetspts

#================================================================
# QCD
infile_2 = None
if len(sys.argv)>1:
    infile_2 = open(sys.argv[1],'r')
else:
    print "Need to pass in an input file for the first argument!!!!"
    exit(-1)
    

qcdpts,xpts = scale(infile_2,100)
tot_pts += qcdpts

#================================================================
# t
infile_3 = None
if len(sys.argv)>1:
    infile_3 = open(sys.argv[1],'r')
else:
    print "Need to pass in an input file for the first argument!!!!"
    exit(-1)
    

tpts,xpts = scale(infile_3,200)
tot_pts += tpts 

#================================================================
# tbar
infile_4 = None
if len(sys.argv)>1:
    infile_4 = open(sys.argv[1],'r')
else:
    print "Need to pass in an input file for the first argument!!!!"
    exit(-1)
    

tbarpts,xpts = scale(infile_4,300)
tot_pts += tbarpts


f = open("toy_cocktail.dat", 'w+')
output = ""

#xpts = np.array([])
for x,y in zip(xpts,tot_pts):
    
    output = "%f %f\n" % (x,y)
    
    f.write(output)

f.close()

#print tot_pts
#print len(tot_pts)

