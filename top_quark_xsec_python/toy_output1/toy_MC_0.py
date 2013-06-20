import numpy as np
import matplotlib.pylab as plt
import math
import sys

from scipy.stats import poisson

#==========================================================

print sys.argv


def scale(n,t,max_files=1,tag="default"):
    m = 0

    while m<max_files:
        outfilename = "toy_%s_%05d.dat" % (tag,m)
        f = open(outfilename,'w+')
        output = ""
        
        xpts = np.array([])
        ypts = np.array([])
        #ypts_new = np.array([])
        ypts_pois = np.array([])
        n.seek(0)
        for line in n:
            vals = line.split()
            x = float(vals[0])
            y = float(vals[1])

            xpts = np.append(xpts,x)
            ypts = np.append(ypts,y)
            
        # Use the scaling factor as a Poisson input.
        # In other words, don't generate the same number of events each time.
        # Instead, the number of events will be random for each one, but will
        # be distributed according to a Poisson distribution.
        #scaling_factor = poisson.rvs(int(t))
        # ACTUALLY, MAYBE WE DON'T NEED TO DO THIS PART
        scaling_factor = t
        #print "number of events for this sample: %d" % (scaling_factor)    

        for i in ypts:
            new_y = i*(scaling_factor/sum(ypts))
            #ypts_new = np.append(ypts_new,new_y)

            #rv = poisson(new_y)
            R = 0.0
            if np.ceil(new_y)>0:
                R = poisson.rvs(np.ceil(new_y))

            ypts_pois = np.append(ypts_pois,R)

        # This is to make sure that we get the same number of entries as our
        # new_scaling (Poisson total for this toy).
        # I *think* this works. It will give you floats for the bin heights,
        # but I think that's OK for these toy tests.
        # ACTUALLY MAYBE THIS IS NOT OK. 
        #nentries= sum(ypts_pois)
        #new_scaling = scaling_factor/nentries
        #ypts_pois *= new_scaling

        print "number of events for this sample: %d" % (sum(ypts_pois))

                
        for x,y in zip(xpts,ypts_pois):
            output = "%f %f\n" % (x,y)     
            f.write(output)
            
        f.close()

        m += 1



#===========================================================
# Read in the file from the command line
infile = None
if len(sys.argv)>1:
    infile = open(sys.argv[1],'r')
else:
    print "Need to pass in an input file for the first argument!!!!"
    exit(-1)

scaling_factor = 19000
if len(sys.argv)>2:
    scaling_factor = float(sys.argv[2])


tag = sys.argv[1].split('/')[-1].split('.')[0]

number_of_files_to_generate = 1000
scale(infile,scaling_factor,number_of_files_to_generate,tag)
