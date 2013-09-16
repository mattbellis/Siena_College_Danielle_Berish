#!/usr/bin/env python
# ==============================================================================
# ==============================================================================

from ROOT import gRandom, TH1, TH1D, cout, TCanvas
from ROOT import kRed,kBlack,kBlue

import ROOT

import sys

import numpy as np

# ==============================================================================
#  Example Unfolding
# ==============================================================================

# ==============================================================================
#  Read in the data.
# ==============================================================================

ROOT.gStyle.SetOptStat(1111111)

chain = ROOT.TChain("Events")

for file in sys.argv[1:]:
        chain.AddFile(file)

hMC_true = TH1D("MC_true","Truth and measured: Top quark p_{t}", 40, 100,600)
hMC_meas = TH1D("MC_meas","Efficiency: Top quark p_{t}", 40, 100,600)
#hcsv = TH1D("CSV","CSV variable", 120, 0,1.2)
hcsv = []
for i in range(0,10):
    name = "hcsv%d" % (i)
    hcsv.append(TH1D(name,"CSV variable", 120, 0,1.2))

hnjets = TH1D("njets","njets", 10,-0.5,9.5)
htoppt = TH1D("toppt","toppt", 100,100.0,1100.0)

###############################################################################
# Assignment! 
# Fill these hisograms
###############################################################################
htop_ptmax = TH1D("htop_ptmax","Highest pt top", 100,-100,500.0)
htop_eta = TH1D("htop_eta","Eta for the top jets", 3,-1,1)
htop_phi = TH1D("htop_phi","Phi for the top jets", 3,-1,1)
htop_mass = TH1D("htop_mass","Mass for the top jets", 5,-5,200)
htop_nSubjets = TH1D("htop_nSubjets","Number of subjets for the top jets", 5,-5,5)
htop_minMass = TH1D("htop_minMass","Min mass for the top jets", 5,-5,100)

hcsvjet_ptmax = TH1D("hcsvjet_ptmax","Highest pt CSV jet", 100,-100.0,500.0)
hcsvjet_eta = TH1D("hcsvjet_eta","CSV jet eta",10,-5,5)
hcsvjet_phi = TH1D("hcsvjet_phi","CSV jet phi",10,-5,5)

hmuon_ptmax = TH1D("hmoun_ptmax","Highest pt Muon", 100,-100,500)
hmuon_eta = TH1D("hmuon_eta","Muon eta", 10,-5,5)
hmuon_phi = TH1D("hmuon_phi","Muon phi", 10,-5,5)

# Muon
muon_str = []
muon_str.append("floats_pfShyftTupleMuons_pt_ANA.obj")
muon_str.append("floats_pfShyftTupleMuons_eta_ANA.obj")
muon_str.append("floats_pfShyftTupleMuons_phi_ANA.obj")

# Top
top_str = []
top_str.append("floats_pfShyftTupleJetsLooseTopTag_pt_ANA.obj")
top_str.append("floats_pfShyftTupleJetsLooseTopTag_eta_ANA.obj")
top_str.append("floats_pfShyftTupleJetsLooseTopTag_phi_ANA.obj")
top_str.append("floats_pfShyftTupleJetsLooseTopTag_mass_ANA.obj")
top_str.append("floats_pfShyftTupleJetsLooseTopTag_nSubjets_ANA.obj")
top_str.append("floats_pfShyftTupleJetsLooseTopTag_minMass_ANA.obj")

# CSV jets
csvjet_str = []
csvjet_str.append("floats_pfShyftTupleJetsLoose_csv_ANA.obj")
csvjet_str.append("floats_pfShyftTupleJetsLoose_pt_ANA.obj")
csvjet_str.append("floats_pfShyftTupleJetsLoose_eta_ANA.obj")
csvjet_str.append("floats_pfShyftTupleJetsLoose_phi_ANA.obj")

#chain.SetBranchStatus('*', 1 )
chain.SetBranchStatus('*', 0 )
for s in muon_str:
    chain.SetBranchStatus(s, 1 )
for s in top_str:
    chain.SetBranchStatus(s, 1 )
for s in csvjet_str:
    chain.SetBranchStatus(s, 1 )

npossiblejets = 8

nev = chain.GetEntries()
print nev

'''
p4_meas.SetPtEtaPhiM(pt_meas,eta_meas,phi_meas,mass_meas);
#dR = np.sqrt((eta_meas-eta_truth)**2 + (phi_meas-phi_truth)**2)
dR0 = p4_meas.DeltaR(p4_truth);
'''


################################################################################
# Loop over the events
################################################################################
for n in xrange(nev):
    if n%10000==0:
        print "%d of %d" % (n,nev)

    chain.GetEntry(n)

    #pt_meas = chain.GetLeaf(top_str[0]).GetValue(0)
    #htoppt.Fill(pt_meas)

    #print "---------"
    top_ptmax = 0.0
    #top_eta = 0.0
    #top_phi = 0.0
    #top_mass = 0.0
    #top_nSubjets = 0.0
    #top_minMass = 0.0

    csvjet_ptmax = 0.0
    muon_ptmax = 0.0
    
    njets = 0
    
    for i in xrange(npossiblejets):
        #val = chain.GetLeaf(csvjet_str[0]).GetValue(i)
        top_pt = chain.GetLeaf(top_str[0]).GetValue(i)
        if top_pt > top_ptmax:
            top_ptmax = top_pt
        top_eta = chain.GetLeaf(top_str[1]).GetValue(i)
        top_phi = chain.GetLeaf(top_str[2]).GetValue(i)
        top_mass = chain.GetLeaf(top_str[3]).GetValue(i)
        top_nSubjets = chain.GetLeaf(top_str[4]).GetValue(i)
        top_minMass = chain.GetLeaf(top_str[5]).GetValue(i)
        
        csvjet_pt = chain.GetLeaf(csvjet_str[1]).GetValue(i)
        if csvjet_pt > csvjet_ptmax:
            csvjet_ptmax = csvjet_pt
        csvjet_eta = chain.GetLeaf(csvjet_str[2]).GetValue(i)
        csvjet_phi = chain.GetLeaf(csvjet_str[3]).GetValue(i)

        muon_pt = chain.GetLeaf(muon_str[0]).GetValue(i)
        if muon_pt > muon_ptmax:
            muon_ptmax = muon_pt
        muon_eta = chain.GetLeaf(muon_str[1]).GetValue(i)
        muon_phi = chain.GetLeaf(muon_str[2]).GetValue(i)

    htop_ptmax.Fill(top_ptmax)
    htop_eta.Fill(top_eta)
    htop_phi.Fill(top_phi)
    htop_mass.Fill(top_mass)
    htop_nSubjets.Fill(top_nSubjets)
    htop_minMass.Fill(top_minMass)

    hcsvjet_ptmax.Fill(csvjet_ptmax)
    hcsvjet_eta.Fill(csvjet_eta)
    hcsvjet_phi.Fill(csvjet_phi)

    hmuon_ptmax.Fill(muon_ptmax)
    hmuon_eta.Fill(muon_eta)
    hmuon_phi.Fill(muon_phi)

    '''
    if val>0.0:
        njets += 1
        #hcsv.Fill(val)
        for j in range(0,10):
            ptlo = 0 + j*100.0
            pthi = 0 + (j+1)*100.0
            if pt_meas>=ptlo and pt_meas<=pthi:
                hcsv[j].Fill(val)
    #print val
    '''
    #print "njets: ",njets
    #hnjets.Fill(njets)

################################################################################
# 
################################################################################
c0 = TCanvas( 'c0', 'Top pt', 10, 10, 1400, 800 )
c0.Divide(1,1)
c0.cd(1)
htop_ptmax.Draw()
c0.Update()

c1 = TCanvas( 'ctop_1', 'Top eta', 10, 10, 1400, 800 )
c1.Divide(1,1)
c1.cd(1)
htop_eta.Draw()
c1.Update()

c2 = TCanvas( 'ctop_2', 'Top phi', 10, 10, 1400, 800 )
c2.Divide(1,1)
c2.cd(1)
htop_phi.Draw()
c2.Update()

c3 = TCanvas( 'ctop_3', 'Top mass', 10, 10, 1400, 800 )
c3.Divide(1,1)
c3.cd(1)
htop_mass.Draw()
c3.Update()

c4 = TCanvas( 'ctop_4', 'Top nSubjets', 10, 10, 1400, 800 )
c4.Divide(1,1)
c4.cd(1)
htop_nSubjets.Draw()
c4.Update()

c5 = TCanvas( 'ctop_5', 'Top minMass', 10, 10, 1400, 800 )
c5.Divide(1,1)
c5.cd(1)
htop_minMass.Draw()
c5.Update()


ccsvjet = TCanvas( 'ccsvjet', 'CSV Jet pt', 10, 10, 1400, 800)
ccsvjet.Divide(1,1)
ccsvjet.cd(1)
hcsvjet_ptmax.Draw()
ccsvjet.Update()




'''
c1 = TCanvas( 'c1', 'MC', 10, 10, 1400, 800 )
c1.Divide(2,1)
c1.cd(1)
hnjets.Draw()
c1.cd(2)
htoppt.Draw()

c2 = TCanvas( 'c2', 'MC', 20, 20, 1400, 800 )
c2.Divide(5,2)
for i in range(0,10):
    c2.cd(i+1)
    hcsv[i].Draw()
'''

'''
hMC_true.SetLineColor(kBlack);  
hMC_true.Draw();  # MC raw 
c1.SaveAs("MC_true.png")
'''

#c1.Update()


################################################################################
if __name__=="__main__":
    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = raw_input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]

