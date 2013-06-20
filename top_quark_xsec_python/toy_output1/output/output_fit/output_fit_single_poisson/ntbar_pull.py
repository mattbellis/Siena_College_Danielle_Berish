import numpy as np
import matplotlib.pylab as plt
import math
import sys

#================================================
print sys.argv

def tbar_pull(n):
    
    ntbar = np.array([])
    tbar_unc = np.array([])

    pull = np.array([])

    true_tbar = 364
    
    
    for odd_line,even_line in zip(n,n):
        ntbar_new = float(odd_line.strip())
        tbar_unc_new = float(even_line.strip())

        ntbar = np.append(ntbar,ntbar_new)
        tbar_unc = np.append(tbar_unc,tbar_unc_new)

        pt = (ntbar_new - true_tbar)/tbar_unc_new
        pull = np.append(pull,pt)

    return pull,ntbar

#==================================================    
# Read in the file from the command line
infile_0 = None
if len(sys.argv)>1:
    infile_0 = open(sys.argv[1],'r')
else:
    print "Need to pass in an input file for the first argument!!!!"
    exit(-1)


pull,ntbar = tbar_pull(infile_0)

print "mean: ",np.mean(pull)
print "std dev: ",np.std(pull)

plt.figure()
plt.hist(pull,50)
plt.xlabel("Pull")

print "mean: ",np.mean(ntbar)
print "std dev: ",np.std(ntbar)


plt.figure()
plt.hist(ntbar,50)
plt.xlabel(r'# of $\bar{t}$ events returned by fit')


plt.show()
