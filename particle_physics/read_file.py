import numpy as np
import matplotlib.pylab as plt
import sys

import hep_tools 

f = open(sys.argv[1])

print "Reading in the data...."
events = hep_tools.get_events(f)

print len(events)

for event in events:

    jets = events[0]
    muons = events[1]
    electrons = events[2]
    photons = events[3]
    met = events[4]

    print "# of jets: %d" % (len(jets))

