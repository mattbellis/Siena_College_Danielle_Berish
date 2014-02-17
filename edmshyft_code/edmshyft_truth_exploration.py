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
    elif (pdg0 <= 18 and pdg0) >= 11 or (pdg0 >= -18 and pdg0 <= -11):  #lepton
        classification.append(1)

    if pdg2 <=6 and pdg2 >= -6:
        classification.append(0)
    elif (pdg2 <= 18 and pdg2) >= 11 or (pdg2 >= -18 and pdg0 <= -11):
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

htop_jet = TH1D("htop_jet","p_{T} top jet", 80,0,800.0)

hcsvjet_aftercuts = TH2D("hcsvjet_aftercuts","CSV variable vs. top p_{T}", 7,100,800,10,0,1.0)

htop_pt = TH1D("htop_pt","pT Distribution of the top",80,0,800.0)
hantiTop_pt = TH1D("hantiTop_pt","pT Distribution of the anti-top",80,0,800.0)

htop_lepton = TH1D("htop_semilepton","Tops that decay semi-leptonically", 80,0,800)
htop_hadron = TH1D("htop_hadron","Tops that decay hadronically", 80,0,800)


# Top Truth
truth_str = []
truth_str.append("floats_pfShyftTupleGenParticles_pdgId_ANA.obj")
truth_str.append("floats_pfShyftTupleGenParticles_status_ANA.obj")
truth_str.append("floats_pfShyftTupleGenParticles_pt_ANA.obj")

# Top reconstructed from the top tagging info.
top_str = []
top_str.append("floats_pfShyftTupleJetsLooseTopTag_pt_ANA.obj")
top_str.append("floats_pfShyftTupleJetsLooseTopTag_eta_ANA.obj")
top_str.append("floats_pfShyftTupleJetsLooseTopTag_phi_ANA.obj")
top_str.append("floats_pfShyftTupleJetsLooseTopTag_mass_ANA.obj")
top_str.append("floats_pfShyftTupleJetsLooseTopTag_nSubjets_ANA.obj")
top_str.append("floats_pfShyftTupleJetsLooseTopTag_minMass_ANA.obj")

p4 = TLorentzVector()

#chain.SetBranchStatus('*', 1 )
chain.SetBranchStatus('*', 0 )
for s in truth_str:
    chain.SetBranchStatus(s, 1 )
for s in top_str:
    chain.SetBranchStatus(s, 1 )


nev = chain.GetEntries()
print nev

hadron_count = 0
lepton_count = 0
semi_lepton_count = 0
not_semi_lepton_count = 0

################################################################################
# Loop over the events
################################################################################
for n in xrange(nev):
    if n%1000==0:
        print "%d of %d" % (n,nev)

    chain.GetEntry(n)
    flag_tops = 0
    flag_Ws_bs = 0
    flag = 0
    decay_count = 0
    decay = []
    top_antitop_pt = []

    #print '---------------------'
    for i in xrange(32):
        pdg = chain.GetLeaf(truth_str[0]).GetValue(i)
        #status = chain.GetLeaf(truth_str[1]).GetValue(i)
        pt = chain.GetLeaf(truth_str[2]).GetValue(i)


        if pdg == 6:
            htop_pt.Fill(pt)
            top_antitop_pt.append(pt)
            flag_tops += 1
        elif pdg == -6:
            hantiTop_pt.Fill(pt)
            top_antitop_pt.append(pt)
            flag_tops += 1
        
        # look for W+,b,W-,b
        if flag_tops >= 2:
            if pdg==24 or pdg ==-24 or pdg==5 or pdg ==-5:
                flag_Ws_bs += 1
                flag = 0
            else:
                flag = 1
        
        # when flag is 4, put next four entries into list 
        if flag == 1 and decay_count < 4 and flag_Ws_bs == 4:
            decay.append(pdg)
            decay_count += 1
    
        #print pdg,pt
    #print decay
    if len(decay) > 0:
        classif = classify(decay[0],decay[1],decay[2],decay[3])
        
        #count how many tops decay hadronically vs. leptonically
        if classif[0] == 0 or classif[1] == 0:
            hadron_count += 1
        elif classif[0] == 1 or classif[1] == 1:
            lepton_count += 1

        #plot semi-leptonically decaying events
        if classif == [0,1]:
            htop_lepton.Fill(top_antitop_pt[1])
            htop_hadron.Fill(top_antitop_pt[0])
            semi_lepton_count += 1
        elif classif == [1,0]:
            htop_lepton.Fill(top_antitop_pt[1])
            htop_hadron.Fill(top_antitop_pt[0])
            semi_lepton_count += 1
        else:
            not_semi_lepton_count += 1

    top_pt = 0
    for i in xrange(2):
        top_pt = chain.GetLeaf(top_str[0]).GetValue(i)

        if top_pt>0:
            htop_jet.Fill(top_pt)




print "Hadronically: ", hadron_count
print "Leptonically: ", lepton_count
print "Semi_leptonically: ", semi_lepton_count
print "Not Semi_leptonically: ", not_semi_lepton_count
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

ctoplep = TCanvas('ctoplep', 'Tops that Decay Leptonically', 10, 10, 1400, 600)
htop_lepton.Draw()
ctoplep.Update()

ctophad = TCanvas('ctophad', 'Tops that Decay Hadronically', 10, 10, 1400, 600)
htop_hadron.Draw()
ctophad.Update()

ctopjet = TCanvas('ctopjet', 'Tops jets', 10, 10, 1400, 600)
htop_jet.Draw()
ctopjet.Update()

################################################################################
if __name__=="__main__":
    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = raw_input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]

