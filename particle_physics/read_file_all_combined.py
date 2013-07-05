import numpy as np
import matplotlib.pylab as plt
import sys
import lichen.lichen as lch 

import hep_tools 

###############################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#calculate the magnitude of the momentum 

def momentum(n):    
    px = n[1]
    py = n[2]
    pz = n[3]

    p = np.sqrt(px**2 + py**2 + pz**2)  

    return p
         
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#calculate the magnitude of the MET

def mets(n):
    px = n[0]
    py = n[1]

    p = np.sqrt(px**2 + py**2)
    return p

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# find the three jets with the highest momentum
def top(n): #n = number of jets
    p = np.array([])
    m = np.array([])
    pt = np.array([])
    jet_index = []
    pt_comp = []
    for i in range(0,n):
        for j in range(i+1,n):
            for k in range(j+1,n):
                energy = jets[i][0] + jets[j][0] + jets[k][0]
                px = jets[i][1] + jets[j][1] + jets[k][1]
                py = jets[i][2] + jets[j][2] + jets[k][2]
                pz = jets[i][3] + jets[j][3] + jets[k][3]
                b_0,b_1,b_2 = jets[i][4], jets[j][4], jets[k][4]

                if b_0 >= 0 or b_1 >= 0 or b_2 >= 0:
                    p_new = px**2 + py**2 + pz**2
                    m_new = np.sqrt(energy**2 - p_new)
                    pt_new =np.sqrt(px**2 + py**2)
                    jet_index_new = [i,j,k]
                    pt_comp_new = [px,py]

                    p = np.append(p,np.sqrt(p_new))
                    m = np.append(m,m_new)
                    pt = np.append(pt,pt_new)
                    jet_index.append([jet_index_new])
                    pt_comp.append(pt_comp_new)

    return p,m,pt,jet_index,pt_comp

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# find the second top 
def second_top(n):
    second_top_m = np.array([])
    second_top_p = np.array([])
    for muon in muons:
        E_n = np.sqrt(met[0]**2 + met[1]**2)
        E = E_n + muon[0] + jets[n][0]
        px = met[0] + muon[1] + jets[n][1]
        py = met[1] + muon[2] + jets[n][2]
        pz = 0

        second_top_m_new = np.sqrt(E**2 - (px**2 + py**2 + pz**2))
        second_top_p_new = np.sqrt(px**2 + py**2 + pz**2)
        
        second_top_m = np.append(second_top_m,second_top_m_new)
        second_top_p = np.append(second_top_p,second_top_p_new)

    return second_top_m,second_top_p


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# find W jet in top jets
def w_jet(n): #n = number of jets
    p = np.array([])
    m = np.array([])
    for i in range(0,n):
        for j in range(i+1,n):
            energy = top_jets[i][0] + top_jets[j][0]
            px = top_jets[i][1] + top_jets[j][1]
            py = top_jets[i][2] + top_jets[j][2]
            pz = top_jets[i][3] + top_jets[j][3]

            p_new = px**2 + py**2 + pz**2
            m_new = np.sqrt(energy**2 - p_new)

            p = np.append(p,np.sqrt(p_new))
            m = np.append(m,m_new)

    return p,m

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# find angle between MET and pt
def angle(n):   # n = index of top candidate
    met_x = met[0]
    met_y = met[1]
    pt_x = pt_comp_top[n][0]
    pt_y = pt_comp_top[n][1]

    pt_len = pt_top[n]
    met_len = np.sqrt(met_x**2 + met_y**2)

    k = k = pt_x*met_x + pt_y*met_y

    x = k/(pt_len*met_len)
    theta = np.arccos(x)

    return theta

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

top_mass = -999*np.ones(1000000)
top_momentum = -999*np.ones(1000000)
top_pt = -999*np.ones(1000000)

tm = 0
tp = 0
tpt = 0

second_top_mass = np.array([])
second_top_momentum = np.array([])

wjet_mass = np.array([]) 
wjet_momentum =  np.array([])

theta = np.array([])

for count,event in enumerate(events):

    jets = event[0]
    muons = event[1]
    electrons = event[2]
    photons = event[3]
    met = event[4]
    top_jets = []

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

    ################################
    #reconstruct top
    n = len(jets)
    if n<3:
        None
    if n>=3:
        p_top,m_top,pt_top,jet_index,pt_comp_top = top(n)
        if len(p_top)>0:
            i = np.argmax(p_top)
            top_mass_new = m_top[i]
            top_momentum_new = np.sqrt(p_top[i])
            top_p_transverse_new = pt_top[i]

            top_mass[tm] = top_mass_new
            tm += 1

            top_momentum[tp] = top_momentum_new
            tp +=1

            top_pt[tpt] = top_p_transverse_new
            tpt +=1 
            
            #find angle between MET and pt
            theta_new = angle(i)
            theta = np.append(theta,theta_new)

            #find wjet
            top_jets.append(jets[jet_index[i][0][0]])
            top_jets.append(jets[jet_index[i][0][1]])
            top_jets.append(jets[jet_index[i][0][2]])

            n = len(top_jets)
            p_w, m_w = w_jet(n)
            
            wjet_mass = np.append(wjet_mass, m_w)
            wjet_momentum = np.append(wjet_momentum, p_w)


            #reconstruct second top
            i = np.argmax(pt_top)

            jets.pop(jet_index[i][0][0])
            jets.pop((jet_index[i][0][1]-1))
            jets.pop((jet_index[i][0][2]-2))

            n = len(jets)
            if n>0:
                if jets[0][4] >= 0 or jets[n-1][4] >= 0:
                    second_top_m_new,second_top_p_new = second_top(0)
                    
                    second_top_mass = np.append(second_top_mass, second_top_m_new)
                    second_top_momentum = np.append(second_top_momentum, second_top_p_new)
                elif jets[n-1][4] != jets[0][4] and jets[n-1][4] >= 0:
                    second_top_m_new,second_top_p_new = second_top(n-1)

                    second_top_mass = np.append(second_top_mass, second_top_m_new)
                    second_top_momentum = np.append(second_top_momentum, second_top_p_mew)

###########################################################################
tag = sys.argv[1].split('/')[-1].split('.')[0]

print "Making the plots....."

plt.figure()
#lch.hist_2D(theta,top_momentum[top_momentum>-999], xbins=50,ybins=50)
#lch.hist_2D(top_mass[top_mass>-999],top_momentum[top_momentum>-999], xbins=50, ybins=50)
lch.hist_2D(theta,second_top_mass,xbins=50,ybins=50)
plt.show()






#################################################################################################################
'''
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
'''
