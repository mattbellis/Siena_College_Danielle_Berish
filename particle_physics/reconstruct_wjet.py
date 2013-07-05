import numpy as np
import matplotlib.pylab as plt
import sys
import lichen.lichen as lch

import hep_tools

######################################################################
# find the three jets with the highest momentum
def top(n): #n = number of jets 
    p = np.array([])
    m = np.array([])
    pt = np.array([])
    jet_index = []
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

                    p = np.append(p,p_new)
                    m = np.append(m,m_new)
                    pt = np.append(pt,pt_new)
                    jet_index.append(jet_index_new)
    return p,m,pt,jet_index
######################################################################
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


#######################################################################
f = open(sys.argv[1])

print "Reading in the data...."
events = hep_tools.get_events(f)

print len(events)

top_mass = np.array([])
top_momentum = np.array([])
top_pt = np.array([])
wjet_mass = np.array([])

for count,event in enumerate(events):
    jets = event[0]
    muons = event[1]
    electrons = event[2]
    photons = event[3]
    met = event[4]
    top_jets = []

    n = len(jets)

    if n<3:
        None
    elif n>=3:
        p,m,pt,jet_index = top(n)
        if len(p)>0:
            i = np.argmax(p) #find index of largest momentum 
            mass = m[i]      # and corresponding mass
            momentum = np.sqrt(p[i])
            p_transverse = pt[i]

            top_mass = np.append(top_mass,mass)
            top_momentum = np.append(top_momentum,momentum)
            top_pt = np.append(top_pt,p_transverse)   
           
            top_jets.append(jets[jet_index[i][0]])
            top_jets.append(jets[jet_index[i][1]])
            top_jets.append(jets[jet_index[i][2]])

            n = len(top_jets)
            p_w,m_w = w_jet(n)
            wjet_mass = np.append(wjet_mass,m_w)


#######################################################
'''
#find the percentage of top quark events that 
#have a pt>400

count = 0
for pt in top_pt:
    if pt > 400:
        count += 1

fraction = float(count)/len(top_pt)
print "Fraction of top with pt>400: %f" % (fraction)
'''
######################################################
tag = sys.argv[1].split('/')[-1].split('.')[0]

plt.figure()
lch.hist_err(top_mass,bins=50,range=(0,500))
plt.title("%s: Top Mass" % (tag))

plt.figure()

plt.subplot(121)
lch.hist_err(top_momentum,bins=50,range=(0,1500))
plt.title("%s: Top momentum" % (tag))

plt.subplot(122)
lch.hist_err(top_pt,bins=50,range=(0,400))
plt.title("%s: Top pt" % (tag))

plt.figure()
lch.hist_err(wjet_mass,bins=50,range=(0,500))
plt.title("%s: Wjet Mass" % (tag))
plt.show()
