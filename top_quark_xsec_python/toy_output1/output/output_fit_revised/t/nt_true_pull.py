import numpy as np
import matplotlib.pylab as plt
import math
import sys

#================================================
print sys.argv

def t_pull(n,m):
    
    nt = np.array([])
    t_unc = np.array([])

    pull = np.array([])
    
    
    for odd_line,even_line,i in zip(n,n,m):
        nt_new = float(odd_line.strip())
        t_unc_new = float(even_line.strip())

        nt = np.append(nt,nt_new)
        t_unc = np.append(t_unc,t_unc_new)

        pt = (nt_new - float(i))/t_unc_new
        pull = np.append(pull,pt)

    return pull,nt

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

pull,nt = t_pull(infile_0,infile_1)

print "mean: ",np.mean(pull)
print "std dev: ",np.std(pull)

plt.figure()
plt.hist(pull,50)
plt.xlabel("Pull")

print "mean: ",np.mean(nt)
print "std dev: ",np.std(nt)


plt.figure()
plt.hist(nt,50)
plt.xlabel(r'# of t events returned by fit')


plt.show()
