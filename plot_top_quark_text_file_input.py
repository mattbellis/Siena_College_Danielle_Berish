import numpy as np
import matplotlib.pylab as plt
import math

import sys

import lichen.lichen as lch

################################################################################
# Figure out the number of combinations
################################################################################
def combinations(njets,ngroup):
    numer = math.factorial(njets)
    denom = math.factorial(ngroup)*math.factorial(njets-ngroup)

    nremaining_jets = njets-ngroup
    remainingjets_numer = math.factorial(nremaining_jets)
    remainingjets_denom = math.factorial(ngroup)*math.factorial(nremaining_jets-ngroup)

    return (numer/denom)*(remainingjets_numer/remainingjets_denom)

################################################################################

print sys.argv

# Read in the file from the command line
infile = None
if len(sys.argv)>1:
    infile = open(sys.argv[1],'r')
else:
    print "Need to pass in an input file for the first argument!!!!"
    exit(-1)

mass = -999*np.ones(500000)

content = np.array(infile.read().split()).astype('float')

print content

#exit()

not_at_end = True
nevent = 0
ncolumns = 4

count = 0
nentries = len(content)

i = 0
while count<nentries:

    #print content[count]
    njets = int(content[count])
    ncombos = combinations(njets,3)
    print ncombos

    nvalues_for_this_event = ncolumns*ncombos
    start = count+1
    end = count+1+nvalues_for_this_event

    values_for_this_event = content[start:end]

    index = np.arange(0,nvalues_for_this_event,ncolumns)
    m0  = values_for_this_event[index]
    pt0 = values_for_this_event[index+1]
    m1  = values_for_this_event[index+2]
    pt1 = values_for_this_event[index+3]

    #print "event"
    #print m0,pt0,m1,pt1

    index = np.argsort(pt0)[-1]
    mass[i] = m0[index]

    i += 1
    count += (1+nvalues_for_this_event)


print "Events: ",len(mass[mass>0])
lch.hist_err(mass[mass>0],bins=125,range=(0,1000))
plt.show()
