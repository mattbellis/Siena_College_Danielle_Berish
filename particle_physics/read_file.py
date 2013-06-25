import numpy as np
import matplotlib.pylab as plt
import sys

import hep_tools 

f = open(sys.argv[1])

print "Reading in the data...."
events = hep_tools.get_events(f)

print len(events)

for event in events:

    jets = event[0]
    muons = event[1]
    electrons = event[2]
    photons = event[3]
    met = event[4]

    #print "# of jets: %d" % (len(jets))
    if len(muons)>0:
        print muons

