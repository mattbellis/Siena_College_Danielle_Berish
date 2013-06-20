import numpy as np
import matplotlib.pylab as plt
import math
import sys

#================================================
print sys.argv

def wjets_pull(n,m):
    
    nwjets = np.array([])
    wjets_unc = np.array([])

    pull = np.array([])
    
    
    for odd_line,even_line,i in zip(n,n,m):
        nwjets_new = float(odd_line.strip())
        wjets_unc_new = float(even_line.strip())

        nwjets = np.append(nwjets,nwjets_new)
        wjets_unc = np.append(wjets_unc,wjets_unc_new)

        pt = (nwjets_new - float(i))/wjets_unc_new
        pull = np.append(pull,pt)

    return pull,nwjets

#==================================================    
# Read in the file from the command line
infile_0 = None
if len(sys.argv)>1:
    infile_0 = open(sys.argv[1],'r')
else:
    print "Need to pass in an input file for the first argument!!!!"
    exit(-1)

infile_1 = None
if len(sys.argv)>1:
    infile_1 = open(sys.argv[2],'r')
else:
    print "Need to pass in an input file for the first argument!!!!"
    exit(-1)

pull,nwjets = wjets_pull(infile_0,infile_1)

print "mean: ",np.mean(pull)
print "std dev: ",np.std(pull)

plt.figure()
plt.hist(pull,50)
plt.xlabel("Pull")

print "mean: ",np.mean(nwjets)
print "std dev: ",np.std(nwjets)


plt.figure()
plt.hist(nwjets,50)
plt.xlabel(r'# of w+jet events returned by fit')


plt.show()
