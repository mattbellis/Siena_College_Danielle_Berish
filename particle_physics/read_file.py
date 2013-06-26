import numpy as np
import matplotlib.pylab as plt
import sys

import hep_tools 

f = open(sys.argv[1])

print "Reading in the data...."
events = hep_tools.get_events(f)
#events = hep_tools.get_events_np(sys.argv[1])

print len(events)

print "Looping over the events..."
for event in events:

<<<<<<< HEAD
    jets = event[0]
    muons = event[1]
    electrons = event[2]
    photons = event[3]
    met = event[4]

    #print "# of jets: %d" % (len(jets))
    if len(muons)>0:
        print muons
=======
    jets = events[0]
    muons = events[1]
    electrons = events[2]
    photons = events[3]
    met = events[4]

    #print "# of jets: %d" % (len(jets))
>>>>>>> 7fee3d5e398b4e9c9c265fcc03500e49106dac0b

