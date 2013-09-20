# A timing test to compare calculating distance between points by hand vs. with a pre-written function 

import time

import numpy as np 
import scipy.spatial 

npts = 10000

x = np.random.random(npts)
y = np.random.random(npts)

################################################################################
# Calculating it all ``by hand"
################################################################################
def byhand(x,y):

    npts = len(x)

    dist = np.zeros((npts*npts-npts)/2)
    i = 0
    index_start = 0
    index_end = npts-1
    for i in range(0,len(x)):

        dist_new = np.sqrt((x[i] - x[i+1:])**2 + (y[i] - y[i+1:])**2)
        #print len(dist_new)
        #print index_start,index_end
        dist[index_start:index_end] = dist_new[:]
        i += 1 

        index_start += (npts-i)
        index_end = index_start + (npts-(i+1))
    
    print "len: %d" % (len(dist))
    #print dist[0:10]
    
    return dist


################################################################################
# Using the scipy code.
################################################################################
def using_pdist(x,y):

    new_array = np.vstack((x.T,y.T)).T
    #print new_array

    #print new_array
    # http://stackoverflow.com/questions/11144513/numpy-cartesian-product-of-x-and-y-array-points-into-single-array-of-2d-points

    # calculates distance between every point in the new array 
    dist = scipy.spatial.distance.pdist(new_array, 'euclidean')
    print "len: %d" % (len(dist))
    #print dist[0:10]

    return dist




################################################################################
# Let's run these and time them.
################################################################################

print "Running byhand.........."
start = time.time()
d0 = byhand(x,y)
end = time.time()

print "time interval: %f seconds \t\t start/end (UNIX time) %f %f" % (end-start, start, end)



print "Running using_pdist.........."
start = time.time()
d1 = using_pdist(x,y)
end = time.time()

print "time interval: %f seconds \t\t start/end (UNIX time) %f %f" % (end-start, start, end)


print "Compare the two methods"
print d1
print d0
print d1-d0
