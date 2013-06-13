import numpy as np
import matplotlib.pylab as plt
import math
import sys

from scipy.stats import poisson 

#====================================================

print sys.argv

def toy_MC(n,max_files=1,tag="default"):
    i = 0
    
    while i<max_files:
        outfilename = "toy_%s_%05d.dat" % (tag,i)
        f = open(outfilename,'w+')
        output = ""
        
        xpts = np.array([])
        ypts = np.array([])
        new_ypts = np.array([])
        n.seek(0) # Rewind input file to beginning.
        for line in n:
            vals = line.split()
            x = float(vals[0])
            y = float(vals[1])

            xpts = np.append(xpts,x)
            ypts = np.append(ypts,y)

            rv = poisson(y)
            if y>0:
                #print y
                R = poisson.rvs(int(y))
                new_ypts = np.append(new_ypts,R)
            else:
                R = 0.0
                new_ypts = np.append(new_ypts,R)

            output += "%f " % (x)
            output += " "
            output += "%f " % (R)
            output += "\n"
        f.write(output)
        f.close()
        
        i += 1
 

#============================================================


# Read in the file from the command line
infile = None
if len(sys.argv)>1:
    infile = open(sys.argv[1],'r')
else:
    print "Need to pass in an input file for the first argument!!!!"
    exit(-1)

tag = sys.argv[1].split('/')[-1].split('.')[0]
toy_MC(infile,10000,tag)


        
#print xpts, ypts
#print new_ypts

#plt.scatter(xpts,ypts)
#plt.scatter(xpts,new_ypts,c='r')
#plt.show()



