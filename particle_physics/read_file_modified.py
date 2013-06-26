import numpy as np
import matplotlib.pylab as plt
import sys
import lichen.lichen as lch 

import hep_tools 

###############################################################################
#calculate the magnitude of the momentum 

def momentum(n):    
    px = n[1]
    py = n[2]
    pz = n[3]

    p = np.sqrt(px**2 + py**2 + pz**2)  

    return p
         
###############################################################################
#calculate the magnitude of the MET

def mets(n):
    px = n[0]
    py = n[1]

    p = np.sqrt(px**2 + py**2)
    return p

###############################################################################

f = open(sys.argv[1])

print "Reading in the data...."
events = hep_tools.get_events(f)

print len(events)

p_jets = -999*np.ones(10000000)
p_muons = -999*np.ones(1000000)
p_electrons = -999*np.ones(1000000)
p_photons = -999*np.ones(1000000)
p_met = -999*np.ones(1000000)

npj = 0
npm = 0
npe = 0
npp = 0
nbq = 0

nm = 0

num_jets = -999*np.ones(1000000)
num_muons = -999*np.ones(1000000)
num_electrons = -999*np.ones(1000000)
num_photons = -999*np.ones(1000000)

bquark_jet_tag = -999*np.ones(10000000)

for count,event in enumerate(events):

    jets = event[0]
    muons = event[1]
    electrons = event[2]
    photons = event[3]
    met = event[4]
   
    for jet in jets:
        n = len(jets)
        num_jets[count]= n

        p = momentum(jet)
        p_jets[npj] = p
        npj += 1

        tag = jet[4]
        bquark_jet_tag[nbq] = tag
        nbq += 1

    for muon in muons:
        n = len(muons)
        num_muons[count] = n

        p = momentum(muon)
        p_muons[npm] = p
        npm += 1

    for electron in electrons:        
        n = len(electrons)
        num_electrons[count] = n
        
        p = momentum(electron)
        p_electrons[npe] = p
        npe += 1

    for photon in photons:
        n = len(photons)
        num_photons[count] = n

        p = momentum(photon)
        p_photons[npp] = p
        npp += 1
    
    p = mets(met)
    p_met[nm] = p
    nm += 1

###########################################################################
tag = sys.argv[1].split('/')[-1].split('.')[0]

print "Making the plots....."
# Histograms of momentum
plt.figure()

plt.subplot(321)
lch.hist_err(p_jets[p_jets>-999],bins=50,range=(0,400),fmt='o',markersize=5,color='black',ecolor='black')
plt.title("%s: Jet momentum" % (tag))
plt.locator_params(nbins=6)
#plt.xlabel("Momentum")

plt.subplot(322)
lch.hist_err(p_muons[p_muons>-999],bins=50,range=(0,300),fmt='o',markersize=5,color='red',ecolor='red')
plt.title("%s: Muon momentum" % (tag))
#plt.xlabel("Momentum")

plt.subplot(323)
lch.hist_err(p_electrons[p_electrons>-999],bins=50,range=(0,200),fmt='o',markersize=5,color='green',ecolor='green')
plt.title("%s: Electron momentum" % (tag))
#plt.xlabel("Momentum")

plt.subplot(324)
lch.hist_err(p_photons[p_photons>-999],bins=50,range=(0,200),fmt='o',markersize=5,color='orange',ecolor='orange')
plt.title("%s: Photon momentum" % (tag))
#plt.xlabel("Momentum")

plt.subplot(325)
lch.hist_err(p_met[p_met>-999],bins=50,range=(0,150),fmt='o',markersize=5,color='teal',ecolor='teal')
plt.title("%s: MET" % (tag))
plt.locator_params(nbins=6)
#plt.xlabel("Momentum")

plt.subplots_adjust(hspace = 0.5)
############################################################################

# Histograms of the number of jets, muons, electrons, and photons
plt.figure()

plt.subplot(221)
lch.hist_err(num_jets[num_jets>-999],bins=10,range=(0,10),markersize=5,color='dimgray',ecolor='dimgray')
plt.title("%s: # Jets" % (tag))

plt.subplot(222)
lch.hist_err(num_muons[num_muons>-999],bins=10,range=(0,10),markersize=5,color='firebrick',ecolor='firebrick')
plt.title("%s: # Muons" % (tag))

plt.subplot(223)
lch.hist_err(num_electrons[num_electrons>-999],bins=10,range=(0,10),markersize=5,color='darkgreen',ecolor='darkgreen')
plt.title("%s: # Electrons" % (tag))

plt.subplot(224)
lch.hist_err(num_photons[num_photons>-999],bins=10,range=(0,10),markersize=5,color='darkorange',ecolor='darkorange')
plt.title("%s: # Photons" % (tag))


plt.figure()
lch.hist_err(bquark_jet_tag[bquark_jet_tag>-999],50,range=(0.5,5),markersize=5,color='navy',ecolor='navy')
plt.title("%s: bquark_jet_tag" % (tag))

plt.show()
