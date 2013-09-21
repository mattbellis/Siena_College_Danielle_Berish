import numpy as np
import matplotlib.pyplot as plt

from scipy import optimize

from scipy.stats import norm
from scipy.stats import expon
from math import factorial, log

import lichen.lichen as lch

from iminuit import Minuit 

import lichen.iminuit_fitting_utilities as fitutils

total = None 

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
def pdf(total,mu,sigma,mylambda,fraction):
    # p is an array of the parameters
    # x is the data points
    #fraction = p[3]
    n = len(total)
    signal = (np.cos(fraction)**2)*mygauss(total,mu,sigma)
    bkgrnd = (np.sin(fraction)**2)*myexp(total,mylambda)
    #poisson = (np.exp(-p[4])*(p[4]**n))/factorial(n)
    poisson = 1
    ret = poisson*(signal+bkgrnd)
    return ret

################################################################################
# Negative log likelihood  
################################################################################
def negative_log_likelihood(mu,sigma,mylambda,fraction):
    # Here you need to code up the sum of all of the negative log likelihoods (pdf)
    # for each data point.
    # y is a dummy variable, is not used
    n = len(total)
    #pois = -n*log(p[4]) + p[4] + log(factorial(n))
    pois = 1.0
    #ret = pois + sum(-np.log(pdf(total,mu,sigma,mylambda,fraction)))
    ret = sum(-np.log(pdf(total,mu,sigma,mylambda,fraction)))
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

m = Minuit(negative_log_likelihood,mu=1.0,limit_mu=(0,3.0), \
                                   sigma=1.0,limit_sigma=(0,3.0), \
                                   mylambda=1.0,limit_mylambda=(0,3.0), \
                                   fraction=0.5,limit_fraction=(0,3.14) \
                                   )
m.migrad()
m.hesse()

print 'fval', m.fval

print m.get_fmin()

values = m.values
print values

print m.print_matrix()

frac_sig = np.cos(values['fraction'])**2
print "Fraction of signal: %f" % (frac_sig)
print "Fraction of bkg: %f" % (1.0-frac_sig)


