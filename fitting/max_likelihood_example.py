import numpy as np
import matplotlib.pyplot as plt

from scipy import optimize

from scipy.stats import norm

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
    # So replace "1" with some function. You may want to refer to the chi-square
    # example.
    # y is a dummy variable, is not used 
    ret = sum(-np.log(pdf(p, x)))
    return ret

################################################################################
# Generate some fake data points and plot them
################################################################################
mu = 5.0
sigma = 0.5
x = np.random.normal(mu,sigma,10000)
plt.figure()
lch.hist_err(x,bins=25)

################################################################################
# Now fit the data.
################################################################################
params_starting_vals = [1.0,1.0] #parameter p 
params_final_vals = optimize.fmin(negative_log_likelihood, params_starting_vals[:],args=(x,x),full_output=True,maxiter=10000000,maxfun=100000)
#second x is a dummy variable

print "Final values"
print params_final_vals

fit_mu = params_final_vals[0][0]
fit_sigma = params_final_vals[0][1]

# Plot the fit 
xpts = np.linspace(3.0,7.0,1000)
gaussian = norm(loc=fit_mu,scale=fit_sigma)
ypts = gaussian.pdf(xpts)
npts = len(x)
bin_width = ((7.0-3.0)/25.0)
ypts *= (npts*bin_width) #scale the gaussian 
plt.plot(xpts,ypts)

plt.show()
