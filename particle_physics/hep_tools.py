import numpy as np


################################################################################
################################################################################
def get_events(infile,verbose=False):

    events = []

    not_at_end = True
    event_count = 0
    while ( not_at_end ):

        ############################################################################
        # Read in one event
        ############################################################################
        line = infile.readline()

        if event_count%1000==0 and verbose:
            print "Event count: ",event_count

        if line=="":
            not_at_end = False

        if line.find("Event")>=0:
            new_event = True

        if new_event==True:

            # Read in the jet info for this event.
            jets = []
            line = infile.readline()
            njets = int(line)
            for i in xrange(njets):
                line = infile.readline()
                vals = line.split()
                e = float(vals[0])
                px = float(vals[1])
                py = float(vals[2])
                pz = float(vals[3])
                bquark_jet_tag = float(vals[4])
                jets.append([e,px,py,pz,bquark_jet_tag])

            # Read in the muon info for this event.
            muons = []
            line = infile.readline()
            nmuons = int(line)
            num_mu=0
            for i in xrange(nmuons):
                line = infile.readline()
                vals = line.split()
                e = float(vals[0])
                px = float(vals[1])
                py = float(vals[2])
                pz = float(vals[3])
                charge = int(vals[4])
                muons.append([e,px,py,pz,charge])
                num_mu+=1
                

            # Read in the electron info for this event.
            electrons = []
            line = infile.readline()
            nelectrons = int(line)
            for i in xrange(nelectrons):
                line = infile.readline()
                vals = line.split()
                e = float(vals[0])
                px = float(vals[1])
                py = float(vals[2])
                pz = float(vals[3])
                charge = int(vals[4])
                electrons.append([e,px,py,pz,charge])

            # Read in the photon info for this event.
            photons = []
            line = infile.readline()
            nphotons = int(line)
            for i in xrange(nphotons):
                line = infile.readline()
                vals = line.split()
                e = float(vals[0])
                px = float(vals[1])
                py = float(vals[2])
                pz = float(vals[3])
                photons.append([e,px,py,pz])


            # Read in the information about the missing transverse energy (MET) in the event.
            # This is really the x and y direction for the missing momentum.
            line = infile.readline()
            vals = line.split()
            met_px = float(vals[0])
            met_py = float(vals[1])

            new_event = False
            event_count += 1

            events.append([jets,muons,electrons,photons,[met_px,met_py]])

    return events

################################################################################
################################################################################
def get_events_np(infilename,verbose=False):

    events = []

    not_at_end = True
    event_count = 0
    #all_vals = np.loadtxt(infilename,unpack=True)
    infile = open(infilename)
    all_vals = np.array(infile.read().split()) #.astype('float')

    nall_vals = len(all_vals)
    #print all_vals[0:10]

    ii = 0

    while ( ii < nall_vals ):

        #print "ii: ",ii

        if event_count%1000==0 and verbose:
            print "Event count: ",event_count

        ############################################################################
        # Read in one event
        ############################################################################
        nvals = all_vals[ii]
        #print "nvals: ",nvals
        ii += 1


        # Read in the jet info for this event.
        jets = []
        #print ii
        #print all_vals[ii]
        njets = int(all_vals[ii])
        #print njets
        ii +=1 
        vals = all_vals[ii:ii+(njets*5)]
        #print vals
        for i in xrange(njets):
            e = float(vals[0 + 5*i])
            px = float(vals[1 + 5*i])
            py = float(vals[2 + 5*i])
            pz = float(vals[3 + 5*i])
            bquark_jet_tag = float(vals[4 + 5*i])
            jets.append([e,px,py,pz,bquark_jet_tag])
            ii += 5

        # Read in the muon info for this event.
        muons = []
        nmuons = int(all_vals[ii])
        ii += 1
        vals = all_vals[ii:ii+nmuons*5]
        #print ii
        #print nmuons
        #print vals
        for i in xrange(nmuons):
            e = float(vals[0+5*i])
            px = float(vals[1+5*i])
            py = float(vals[2+5*i])
            pz = float(vals[3+5*i])
            charge = int(vals[4+5*i])
            muons.append([e,px,py,pz,charge])
            ii += 5
            

        # Read in the electron info for this event.
        electrons = []
        nelectrons = int(all_vals[ii])
        ii += 1
        vals = all_vals[ii:ii+nelectrons*5]
        for i in xrange(nelectrons):
            e = float(vals[0+5*i])
            px = float(vals[1+5*i])
            py = float(vals[2+5*i])
            pz = float(vals[3+5*i])
            charge = int(vals[4+5*i])
            electrons.append([e,px,py,pz,charge])
            ii += 5

        # Read in the photon info for this event.
        photons = []
        nphotons = int(all_vals[ii])
        ii += 1
        vals = all_vals[ii:ii+nphotons*4]
        for i in xrange(nphotons):
            e = float(vals[0+4*i])
            px = float(vals[1+4*i])
            py = float(vals[2+4*i])
            pz = float(vals[3+4*i])
            photons.append([e,px,py,pz])
            ii += 4


        # Read in the information about the missing transverse energy (MET) in the event.
        # This is really the x and y direction for the missing momentum.
        met_px = float(all_vals[ii])
        met_py = float(all_vals[ii+1])
        ii += 2

        event_count += 1

        events.append([jets,muons,electrons,photons,[met_px,met_py]])

    return events
