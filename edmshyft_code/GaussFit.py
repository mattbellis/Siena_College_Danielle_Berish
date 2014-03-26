#!/usr/bin/env python

from ROOT import TH1D, TH1, TCanvas

import ROOT
import numpy as np
import sys
import matplotlib.pyplot as plt

#################################################################################

# Read in the file from the command line
infile = None
if len(sys.argv) > 1:
    infile = open(sys.argv[1],'r')
else:
    print "Need to pass in an input file"
    exit(-1)

content = np.array(infile.read().split()).astype('float')
#print content


# Separate content into designated lists
mean = []
meanError = []
std = []
stdError = []

i = 0

count = 0

while count < len(content):
    mean.append(content[i])
    meanError.append(content[i+1])
    std.append(content[i+2])
    stdError.append(content[i+3])

    i += 4
    count += 4


############################################
# List of pT's 
pT = []
n = 10

while n <= 800:
    pT.append(n)
    n += 20

###########################################
# Fit the mean and std. dev. 

slope,intercept = np.polyfit(pT,mean,1)
print "Slope of Mean: ",slope
#print intercept

slope_std,intercept_std = np.polyfit(pT,std,1)
print "Slope of Std. Dev.: ", slope_std
#print intercept_std

############################################
# Plot the mean and std. dev. 

plt.figure(1)
plt.subplot(211)
plt.ylabel("Mean")
plt.scatter(pT,mean)

plt.subplot(212)
plt.xlabel("Top pT")
plt.ylabel("Std. Dev.")
plt.scatter(pT,std)
plt.show()



