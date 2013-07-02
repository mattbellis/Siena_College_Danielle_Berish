import numpy as np
import matplotlib.pylab as plt
import math
import sys

#================================================
print sys.argv

def ttbar_pull(n,m):
    
    nttbar = np.array([])
    ttbar_unc = np.array([])

    pull = np.array([])
    
    
    for odd_line,even_line,i in zip(n,n,m):
        nttbar_new = float(odd_line.strip())
        ttbar_unc_new = float(even_line.strip())

        nttbar = np.append(nttbar,nttbar_new)
        ttbar_unc = np.append(ttbar_unc,ttbar_unc_new)

        pt = (nttbar_new - float(i))/ttbar_unc_new
        #pt = (nttbar_new - 19000.0)/ttbar_unc_new
        pull = np.append(pull,pt)

    return pull,nttbar

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

pull,nttbar = ttbar_pull(infile_0,infile_1)

print "mean: ",np.mean(pull)
print "std dev: ",np.std(pull)

plt.figure()
plt.hist(pull,50)
plt.xlabel("Pull")

print "mean: ",np.mean(nttbar)
print "std dev: ",np.std(nttbar)


plt.figure()
plt.hist(nttbar,50)
plt.xlabel(r'# of $t\bar{t}$ events returned by fit')


plt.show()
