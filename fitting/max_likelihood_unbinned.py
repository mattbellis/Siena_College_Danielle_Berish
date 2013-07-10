import numpy as np
import matplotlib.pyplot as plt

from scipy import optimize

from scipy.stats import norm
from scipy.stats import expon
from math import factorial

import lichen.lichen as lch

####################################################
# Signal
# Gaussian (normal) function 
####################################################
def mygauss(x,mu,sigma):
    exponent = ((x-mu)**2)/(2*sigma**2)
    a = 1.0/(sigma*np.sqrt(2*np.pi))
    ret = a*np.exp(-exponent)
    return ret

###################################################
# Background
# Exponential
###################################################
def myexp(k,mylambda):
    exponent = mylambda*k
    bkgrnd = mylambda*np.exp(-exponent)
    return bkgrnd

##################################################
# PDF
# Gaussian and background
###################################################
def pdf(p,total):
    # p is an array of the parameters
    # x is the data points
    fraction = p[3]
    signal = (np.cos(fraction)**2)*mygauss(total,p[0],p[1])
    bkgrnd = (np.sin(fraction)**2)*myexp(total,p[2])
    ret = signal+bkgrnd
    return ret

################################################################################
# Negative log likelihood  
################################################################################
def negative_log_likelihood(p, x, y):
    # Here you need to code up the sum of all of the negative log likelihoods (pdf)
    # for each data point.
    # y is a dummy variable, is not used
    ret = sum(-np.log(pdf(p, total)))
    return ret


################################################################################
# Generate fake data points and plot them 
################################################################################
mu = 1.5
sigma = 0.1
x = np.random.normal(mu,sigma,70)

mylambda = 1.0
k = np.random.exponential(1/mylambda,1000)

plt.figure()
#lch.hist_err(x,bins=50,range=(0,4.0),color='red',ecolor='red')
#lch.hist_err(k,bins=50,range=(0,4.0),color='blue',ecolor='blue')

total = np.append(x,k)
lch.hist_err(total,bins=50,range=(0,4.0),markersize=2)
################################################################################
# Now fit the data.
################################################################################
params_starting_vals = [1.5,0.1,1.0,1.34] #mu,sigma,mylambda,fraction
params_final_vals = optimize.fmin(negative_log_likelihood, params_starting_vals[:],args=(total,total),full_output=True,maxiter=10000000,maxfun=100000)
#second x is a dummy variable

print "Final values"
print params_final_vals

fit_mu = params_final_vals[0][0]
fit_sigma = params_final_vals[0][1]
fit_lambda = params_final_vals[0][2]
fit_nsig = params_final_vals[0][3]

npts = len(total)
nsignal = (np.cos(fit_nsig)**2)*npts
nbckgrnd = (np.sin(fit_nsig)**2)*npts
bin_width = ((4.0-0.0)/50.0)

print "# signal: %f" % (nsignal)
print "# bck: %f" % (nbckgrnd) 

# Plot the fit
xpts_sig = np.linspace(0.0,4.0,1000)
gaussian = norm(loc=fit_mu,scale=fit_sigma)
ypts_sig = gaussian.pdf(xpts_sig)
ypts_sig *= (nsignal*bin_width) #scale the gaussian
plt.plot(xpts_sig,ypts_sig)

# Plot the background 
xpts_bk = np.linspace(0.0,4.0,1000)
exponential = expon(scale=1/fit_lambda)
ypts_bk = exponential.pdf(xpts_bk)
ypts_bk *= (nbckgrnd*bin_width)
plt.plot(xpts_bk,ypts_bk,'--')

# Plot complete distribution
xpts = np.linspace(0.0,4.0,1000)
#f = (np.cos(fit_nsig)**2)*ypts_sig + (np.sin(fit_nsig)**2)*ypts_bk 
sig, bk = ypts_sig, ypts_bk
f = sig + bk
plt.plot(xpts,f)

plt.show()
