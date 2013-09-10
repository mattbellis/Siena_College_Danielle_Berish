#!/usr/bin/env python
# ==============================================================================
# ==============================================================================

from ROOT import gRandom, TH1, TH1D, cout, TCanvas
from ROOT import kRed,kBlack,kBlue
from ROOT import TLorentzVector,TH2D

import ROOT

import sys

import numpy as np

# ==============================================================================
#  Example Unfolding
# ==============================================================================

# ==============================================================================
#  Read in the data.
# ==============================================================================

ROOT.gStyle.SetOptStat(111111111)

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
htop_ptmax = TH1D("htop_ptmax","Highest pt top", 110,50,1150.0)
hcsvjet_ptmax = TH1D("hcsvjet_ptmax","Highest pt CSV jet", 110,50.0,1150.0)
hmuon_ptmax = TH1D("hmuon_ptmax","Highest pt muon", 110,50.0,1150.0)

hcsvjet_aftercuts = TH2D("hcsvjet_aftercuts","CSV vs. pt", 10,100,1100,10,0,1.0)

hdR = []
for i in range(0,3):
    name = "hdR%d" % (i)
    title = ""
    if i==0:
        title = "Top vs. muon"
    elif i==1:
        title = "Top vs. CSV jet"
    elif i==2:
        title = "Muon vs. CSV jet"
    hdR.append(TH1D(name,title,100,-7,7))


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

# CSV jets
csvjet_str = []
csvjet_str.append("floats_pfShyftTupleJetsLoose_pt_ANA.obj")
csvjet_str.append("floats_pfShyftTupleJetsLoose_eta_ANA.obj")
csvjet_str.append("floats_pfShyftTupleJetsLoose_phi_ANA.obj")
csvjet_str.append("floats_pfShyftTupleJetsLoose_mass_ANA.obj")
csvjet_str.append("floats_pfShyftTupleJetsLoose_csv_ANA.obj")

p4_muon = TLorentzVector()
p4_top = TLorentzVector()
p4_csvjet = TLorentzVector()

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


################################################################################
# Loop over the events
################################################################################
for n in xrange(nev):
    if n%10000==0:
        print "%d of %d" % (n,nev)

    chain.GetEntry(n)
    found_muon = False
    found_csvjet = False
    found_top = False

    #pt_meas = chain.GetLeaf(top_str[0]).GetValue(0)
    #htoppt.Fill(pt_meas)

    #print "---------"
    top_ptmax = 1.0
    csvjet_ptmax = 1.0
    muon_ptmax = 1.0

    top_etamax = 1.0
    csvjet_etamax = 1.0
    muon_etamax = 1.0

    top_phimax = 1.0
    csvjet_phimax = 1.0
    muon_phimax = 1.0

    top_massmax = 1.0
    csvjet_massmax = 1.0
    muon_massmax = 1.0

    csvjet_valmax = 1.0

    njets = 0

    for i in xrange(npossiblejets):
        
        top_pt = chain.GetLeaf(top_str[0]).GetValue(i)
        if top_pt > top_ptmax:
            top_ptmax = top_pt
            top_etamax = chain.GetLeaf(top_str[1]).GetValue(i)
            top_phimax = chain.GetLeaf(top_str[2]).GetValue(i)
            top_massmax = chain.GetLeaf(top_str[3]).GetValue(i)
            found_top = True

        csvjet_pt = chain.GetLeaf(csvjet_str[0]).GetValue(i)
        if csvjet_pt > csvjet_ptmax:
            csvjet_ptmax = csvjet_pt
            csvjet_etamax = chain.GetLeaf(csvjet_str[1]).GetValue(i)
            csvjet_phimax = chain.GetLeaf(csvjet_str[2]).GetValue(i)
            csvjet_massmax = chain.GetLeaf(csvjet_str[3]).GetValue(i) # For now
            csvjet_valmax = chain.GetLeaf(csvjet_str[4]).GetValue(i)
            found_csvjet = True

        muon_pt = chain.GetLeaf(muon_str[0]).GetValue(i)
        if muon_pt > muon_ptmax:
            muon_ptmax = muon_pt
            muon_etamax = chain.GetLeaf(muon_str[1]).GetValue(i)
            muon_phimax = chain.GetLeaf(muon_str[2]).GetValue(i)
            muon_massmax = 0.105 # For now
            found_muon = True

    htop_ptmax.Fill(top_ptmax)
    hcsvjet_ptmax.Fill(csvjet_ptmax)
    hmuon_ptmax.Fill(muon_ptmax)

    # If we have found a muon, top jet and a CSV jet, then
    # let's analyze this further. 
    if found_csvjet and found_top and found_muon:

        p4_top.SetPtEtaPhiM(top_ptmax,top_etamax,top_phimax,top_massmax);
        p4_csvjet.SetPtEtaPhiM(csvjet_ptmax,csvjet_etamax,csvjet_phimax,csvjet_massmax);
        p4_muon.SetPtEtaPhiM(muon_ptmax,muon_etamax,muon_phimax,muon_massmax);

        dR_top_muon = p4_top.DeltaR(p4_muon);
        dR_top_csvjet = p4_top.DeltaR(p4_csvjet);
        dR_muon_csvjet = p4_muon.DeltaR(p4_csvjet);

        if abs(dR_top_csvjet) > 1.0:
            hdR[0].Fill(dR_top_muon)
            hdR[1].Fill(dR_top_csvjet)
            hdR[2].Fill(dR_muon_csvjet)

        if abs(dR_top_muon-3.0)<1.0 and abs(dR_top_csvjet-3.0)<1.0 and abs(dR_muon_csvjet)<1.0:
            print top_ptmax,csvjet_valmax
            hcsvjet_aftercuts.Fill(top_ptmax,csvjet_valmax)







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
ctop = TCanvas( 'ctop', 'Top pt', 10, 10, 1400, 600 )
ctop.Divide(3,1)
for i in range(0,3):
    ctop.cd(1+i)
    if i==0:
        htop_ptmax.Draw()
    elif i==1:
        hcsvjet_ptmax.Draw()
    elif i==2:
        hmuon_ptmax.Draw()
ctop.Update()


cdR = TCanvas( 'cdR', 'dR', 30, 30, 1400, 600)
cdR.Divide(3,1)
for i in range(0,3):
    cdR.cd(i+1)
    hdR[i].Draw()
cdR.Update()

ccsv2d = TCanvas( 'ccsv2d', 'csv2d', 30, 30, 900, 900)
ccsv2d.Divide(1,1)
ccsv2d.cd(i+1)
hcsvjet_aftercuts.Draw("COLZ")
hcsvjet_aftercuts.Draw("TEXT SAME")
ccsv2d.Update()

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

