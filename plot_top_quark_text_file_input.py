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

mass0 = -999*np.ones(500000)
mass1 = -999*np.ones(500000)
unique_m0 = -999*np.ones(500000)
unique_pt0 = -999*np.ones(500000)

content = np.array(infile.read().split()).astype('float')

print content

#exit()

not_at_end = True
nevent = 0
ncolumns = 4

count = 0
nentries = len(content)

i = 0
allm0count= 0
allpt0count = 0
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

    #remove all of the duplicate masses in first column
    for m in set(m0):
        unique_m0[allm0count] = m
        allm0count += 1

    #remove all of the duplicate pt in second column
    for pt in set(pt0):
        unique_pt0[allpt0count] = pt
        allpt0count += 1

    #print "event"
    #print m0,pt0,m1,pt1
   
    #sort groups to find highest pt and find corresponding mass
    index = np.argsort(pt0)[-1]
    mass0[i] = m0[index]

    #find left over jets that correspond to those with highest pt 
    other_jets = m1[m0==mass0[i]]
    other_pt = pt1[m0==mass0[i]]

    #sort jets that are left to find highest pt
    index = np.argsort(other_pt)[-1]
    mass1[i] = other_jets[index]

    i += 1
    count += (1+nvalues_for_this_event)


print "Events: ",len(mass0[mass0>0])
plt.figure()
lch.hist_err(mass0[mass0>0],bins=125,range=(0,1000))
plt.figure()
lch.hist_err(mass1[mass1>0],bins=125,range=(0,1000))

plt.figure()
lch.hist_2D(mass0,mass1,xbins=100,ybins=100,xrange=(0,500),yrange=(0,500))

#######################
#plot all of the masses in column one
plt.figure()
lch.hist_err(unique_m0[unique_m0>0],bins=125,range=(0,1000))

#######################
#plot all of the pt in column two
plt.figure()
lch.hist_err(unique_pt0[unique_pt0>0],bins=125,range=(0,1000))


plt.show()

    
