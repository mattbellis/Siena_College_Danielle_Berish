import numpy as np
import matplotlib.pylab as plt
import math
import sys

#================================================
print sys.argv

def qcd_pull(n,m):
    
    nqcd = np.array([])
    qcd_unc = np.array([])

    pull = np.array([])
    
    
    for odd_line,even_line,i in zip(n,n,m):
        nqcd_new = float(odd_line.strip())
        qcd_unc_new = float(even_line.strip())

        nqcd = np.append(nqcd,nqcd_new)
        qcd_unc = np.append(qcd_unc,qcd_unc_new)

        pt = (nqcd_new - float(i))/qcd_unc_new
        pull = np.append(pull,pt)

    return pull,nqcd

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

pull,nqcd = qcd_pull(infile_0,infile_1)

print "mean: ",np.mean(pull)
print "std dev: ",np.std(pull)

plt.figure()
plt.hist(pull,50)
plt.xlabel("Pull")

print "mean: ",np.mean(nqcd)
print "std dev: ",np.std(nqcd)


plt.figure()
plt.hist(nqcd,50)
plt.xlabel(r'# of qcd events returned by fit')


plt.show()
