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

    #print '---------------------'
    for i in xrange(32):
        pdg = chain.GetLeaf(truth_str[0]).GetValue(i)
        #status = chain.GetLeaf(truth_str[1]).GetValue(i)
        pt = chain.GetLeaf(truth_str[2]).GetValue(i)

        if pdg == 6:
            htop_pt.Fill(pt)
        elif pdg == -6:
            hantiTop_pt.Fill(pt)
        #print pdg,pt

################################################################################
# Histograms of the pT distribution of the truth top and antitop 
################################################################################
ctop = TCanvas('ctop','Top pt', 10, 10, 1400, 600)
htop_pt.Draw()
ctop.Update()

cantitop = TCanvas('cantitop', 'AntiTop pt', 10, 10, 1400, 600)
hantiTop_pt.Draw()
cantitop.Update()

################################################################################
if __name__=="__main__":
    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = raw_input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]

