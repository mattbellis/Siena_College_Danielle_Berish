import numpy as np
import matplotlib.pylab as plt
import math
import sys

#==============================================
print sys.argv

# Read in the file from the command line
infile = None
if len(sys.argv)>1:
    infile = open(sys.argv[1],'r')
else:
    print "Need to pass in an input file for the first argument!!!!"
    exit(-1)

nttbar = np.array([])
ttbar_unc = np.array([])
true_ttbar = 19000

pull = np.array([])

for odd_line,even_line in zip(infile, infile):
    nttbar_new = float(odd_line.strip())
    ttbar_unc_new = float(even_line.strip())
    
    nttbar = np.append(nttbar,nttbar_new)
    ttbar_unc = np.append(ttbar_unc,ttbar_unc_new)

    pt = (nttbar_new - true_ttbar)/ttbar_unc_new
    pull = np.append(pull,pt)


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

