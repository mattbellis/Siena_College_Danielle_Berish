#!/usr/bin/env python
# ==============================================================================
# ==============================================================================

from ROOT import gRandom, TH1, TH1D, cout, TCanvas
from ROOT import kRed,kBlack,kBlue
from ROOT import TLorentzVector,TH2D

import ROOT

import sys

import numpy as np

tag = "ttbar_MC_truth"
#tag = "data"

###############################################################################
# Function that takes in four pdg numbers and classifies them
def classify(pdg0,pdg1,pdg2,pdg3):
    classification = []  # 0 = hadron, 1 = lepton
    if pdg0 <= 6 and pdg0 >= -6:  # hadronic 
        classification.append(0)
    elif pdg0 <= 18 and pdg0 >= 11 or pdg0 >= -18 and pdg0 <= -11:  #lepton
        classification.append(1)

    if pdg2 <=6 and pdg2 >= -6:
        classification.append(0)
    elif pdg2 <= 18 and pdg2 >= 11 or pdg2 >= -18 and pdg0 <= -11:
        classification.append(1)

    return classification 


# ==============================================================================
#  Read in the data.
# ==============================================================================

#ROOT.gStyle.SetOptStat(111111111)
ROOT.gStyle.SetOptStat(1)

chain = ROOT.TChain("Events")

for file in sys.argv[1:]:
        chain.AddFile(file)

###############################################################################
# Assignment! 
# Fill these hisograms
###############################################################################
htop_ptmax = TH1D("htop_ptmax","Highest p_{T} top jet", 80,0,800.0)
hcsvjet_ptmax = TH1D("hcsvjet_ptmax","Highest p_{T} b-jet", 110,0.0,800.0)
hmuon_ptmax = TH1D("hmuon_ptmax","Highest p_{T} muon", 80,0.0,800.0)

hcsvjet_aftercuts = TH2D("hcsvjet_aftercuts","CSV variable vs. top p_{T}", 7,100,800,10,0,1.0)

htop_pt = TH1D("htop_pt","pT Distribution of the top",80,0,800.0)
hantiTop_pt = TH1D("hantiTop_pt","pT Distribution of the anti-top",80,0,800.0)

htop_semilepton = TH1D("htop_semilepton","Tops that decay semi-leptonically", 80,0,800)
htop_hadron = TH1D("htop_hadron","Tops that decay hadronically", 80,0,800)


# Top Truth
truth_str = []
truth_str.append("floats_pfShyftTupleGenParticles_pdgId_ANA.obj")
truth_str.append("floats_pfShyftTupleGenParticles_status_ANA.obj")
truth_str.append("floats_pfShyftTupleGenParticles_pt_ANA.obj")

p4 = TLorentzVector()

#chain.SetBranchStatus('*', 1 )
chain.SetBranchStatus('*', 0 )
for s in truth_str:
    chain.SetBranchStatus(s, 1 )


nev = chain.GetEntries()
print nev

################################################################################
# Loop over the events
################################################################################
for n in xrange(nev):
    if n%1000==0:
        print "%d of %d" % (n,nev)

    chain.GetEntry(n)
    flag = 0
    flag_1 = 0
    decay_count = 0
    decay = []
    top_antitop_pt = []

    print '---------------------'
    for i in xrange(32):
        pdg = chain.GetLeaf(truth_str[0]).GetValue(i)
        #status = chain.GetLeaf(truth_str[1]).GetValue(i)
        pt = chain.GetLeaf(truth_str[2]).GetValue(i)

        if pdg == 6:
            htop_pt.Fill(pt)
            top_antitop_pt.append(pt)
        elif pdg == -6:
            hantiTop_pt.Fill(pt)
            top_antitop_pt.append(pt)
        
        # look for W+,b,W-,b
        if pdg==24 or pdg ==-24 or pdg==5 or pdg ==-5:
            flag += 1
            flag_1 = 0
        else:
            flag_1 = 1
        
        # when flag is 4, put next four entries into list 
        if flag == 4 and flag_1 == 1 and decay_count < 4:
            decay.append(pdg)
            decay_count += 1
    
        print pdg,pt
    print decay
    thing = classify(decay[0],decay[1],decay[2],decay[3])
    print thing  

################################################################################
# Histograms of the pT distribution of the truth top and antitop 
################################################################################
ctop = TCanvas('ctop','Top pt', 10, 10, 1400, 600)
print "===================================="
print "Top exponential"
htop_pt.Fit("expo","","",115,650)
htop_pt.Draw()
ctop.Update()

cantitop = TCanvas('cantitop', 'AntiTop pt', 10, 10, 1400, 600)
print "====================================="
print "Antitop exponential"
hantiTop_pt.Fit("expo","","",130,650)
hantiTop_pt.Draw()
cantitop.Update()

################################################################################
if __name__=="__main__":
    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = raw_input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]

