import numpy as np
import matplotlib.pyplot as plt

from scipy import optimize

import lichen.lichen as lch

################################################################################
# Gaussian (normal) function 
# x: x values
# mu: the mean of the Gaussian
# sigma: the width of the Gaussian
#
# returns the height of the Gaussian (probability), where the area under the 
# curve has been normalized to 1.
################################################################################
def mygauss(x,mu,sigma):
    exponent = ((x-mu)**2)/(2*sigma**2)
    a = 1.0/(sigma*np.sqrt(2*np.pi))
    ret = a*np.exp(-exponent)
    return ret

################################################################################
# A generic function for the overall PDF. We can use this then if we need
# to add two Gaussians, or a Gaussian and some background, or a bunch 
# of extra terms together.
#
# Think of this as just some organizational function.
################################################################################
def pdf(p,x): # Probability distribution function 
    # p is an array of the parameters 
    # x is the data points
    # So p[0] will be whatever you want.
    # The functional form of your hypothesis (Gaussian).
    ret = mygauss(x,p[0],p[1])
    return ret

################################################################################
#
################################################################################
def negative_log_likelihood(p, x, y):
    # Here you need to code up the sum of all of the negative log likelihoods (pdf)
    # for each data point.
    # So replace ``1" with some function. You may want to refer to the chi-square
    # example.
    ret = 1
    return ret

################################################################################
# Generate some fake data points and plot them
################################################################################
mu = 5.0
sigma = 0.5
x = np.random.normal(mu,sigma,100)
plt.figure()
lch.hist_err(x,bins=25)

################################################################################
# Now fit the data.
################################################################################
params_starting_vals = [1.0,1.0]
params_final_vals = optimize.fmin(negative_log_likelihood, params_starting_vals[:],args=(x,x),full_output=True,maxiter=10000000,maxfun=100000)

print "Final values"
print params_final_vals
fit_mu = params_final_vals[0][0]
fit_sigma = params_final_vals[0][1]

plt.show()
