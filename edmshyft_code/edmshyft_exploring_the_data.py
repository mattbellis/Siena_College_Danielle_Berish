#!/usr/bin/env python
# ==============================================================================
# ==============================================================================

from ROOT import gRandom, TH1, TH1D, cout, TCanvas
from ROOT import kRed,kBlack,kBlue
from ROOT import TLorentzVector,TH2D

import ROOT

import sys

import numpy as np

tag = "ttbar_MC"
#tag = "data"

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
htoppt = TH1D("toppt","toppt", 70,100.0,800.0)

###############################################################################
#AK5 Assignment! 
# Fill these hisograms
###############################################################################
htop_eta = TH1D("htop_eta","Eta for the top jets", 50,-10,10)
htop_phi = TH1D("htop_phi","Phi for the top jets", 50,-10,10)
htop_mass = TH1D("htop_mass","Mass for the top jets", 50,-20,200)
htop_nSubjets = TH1D("htop_nSubjets","Number of subjets for the top jets", 11,-0.5,10.5)
htop_minMass = TH1D("htop_minMass","Min mass for the top jets", 50,-5,100)

hcsvjet_eta = TH1D("hcsvjet_eta","CSV jet eta",50,-5,5)
hcsvjet_phi = TH1D("hcsvjet_phi","CSV jet phi",50,-5,5)
hcsvjet_mass = TH1D("hcsvjet_mass","CSV jet mass",50,-200,200)

hmuon_eta = TH1D("hmuon_eta","Muon eta", 50,-5,5)
hmuon_phi = TH1D("hmuon_phi","Muon phi", 50,-5,5)

hmuon_ptmax = TH1D("hmuon_ptmax","Highest pt muon", 80,0.0,800.0)
htop_ptmax = TH1D("htop_ptmax","Highest pt top", 80,0,800.0)
hcsvjet_ptmax = TH1D("hcsvjet_ptmax","Highest pt CSV jet", 110,0.0,800.0)

hcsvjet_aftercuts = TH2D("hcsvjet_aftercuts","CSV vs. pt", 7,100,800,10,0,1.0)

htop_aftercuts = TH1D("htop_aftercuts","Top",100,-20,1100)
hcsvjet_oppositeHemisph = TH1D("hcsvjet_oppositeHemisph","Opposite Jet",50,-200,200)

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
    hdR.append(TH1D(name,title,65,0,6.5))


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
csvjet_str.append("floats_pfShyftTupleJetsLooseAK5_pt_ANA.obj")
csvjet_str.append("floats_pfShyftTupleJetsLooseAK5_eta_ANA.obj")
csvjet_str.append("floats_pfShyftTupleJetsLooseAK5_phi_ANA.obj")
csvjet_str.append("floats_pfShyftTupleJetsLooseAK5_mass_ANA.obj")
csvjet_str.append("floats_pfShyftTupleJetsLooseAK5_csv_ANA.obj")

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
    top_ptmax = 0.0
    csvjet_ptmax = 0.0
    muon_ptmax = 0.0

    top_etamax = 0.0
    csvjet_etamax = 0.0
    muon_etamax = 0.0

    top_phimax = 0.0
    csvjet_phimax = 0.0
    muon_phimax = 0.0

    top_massmax = 0.0
    csvjet_massmax = 0.0
    muon_massmax = 0.0

    csvjet_valmax = 0.0

    njets = 0
    
    top_nSubjetsmax = 0.0
    top_minMassmax = 0.0
    index = 0

    for i in xrange(npossiblejets):
        
        top_pt = chain.GetLeaf(top_str[0]).GetValue(i)
        if top_pt > top_ptmax:
            top_ptmax = top_pt
            top_etamax = chain.GetLeaf(top_str[1]).GetValue(i)
            top_phimax = chain.GetLeaf(top_str[2]).GetValue(i)
            top_massmax = chain.GetLeaf(top_str[3]).GetValue(i)
            top_nSubjetsmax = chain.GetLeaf(top_str[4]).GetValue(i)
            top_minMassmax = chain.GetLeaf(top_str[5]).GetValue(i)
            found_top = True

        csvjet_pt = chain.GetLeaf(csvjet_str[0]).GetValue(i)
        if csvjet_pt > csvjet_ptmax:
            index = i
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
    
    if top_ptmax>0:
        htop_ptmax.Fill(top_ptmax)
        htop_eta.Fill(top_etamax)
        htop_phi.Fill(top_phimax)
        htop_mass.Fill(top_massmax)
        htop_nSubjets.Fill(top_nSubjetsmax)
        htop_minMass.Fill(top_minMassmax)

    if csvjet_ptmax>0:
        hcsvjet_ptmax.Fill(csvjet_ptmax)
        hcsvjet_eta.Fill(csvjet_etamax)
        hcsvjet_phi.Fill(csvjet_phimax)

         
    if muon_ptmax>0:
        hmuon_ptmax.Fill(muon_ptmax)
        hmuon_eta.Fill(muon_etamax)
        hmuon_phi.Fill(muon_phimax)

    # If we have found a muon, top jet and a CSV jet, then
    # let's analyze this further. 
    if found_csvjet and found_top and found_muon:

        p4_top.SetPtEtaPhiM(top_ptmax,top_etamax,top_phimax,top_massmax);
        p4_csvjet.SetPtEtaPhiM(csvjet_ptmax,csvjet_etamax,csvjet_phimax,csvjet_massmax);
        p4_muon.SetPtEtaPhiM(muon_ptmax,muon_etamax,muon_phimax,muon_massmax);

        dR_top_muon = p4_top.DeltaR(p4_muon);
        dR_top_csvjet = p4_top.DeltaR(p4_csvjet);
        dR_muon_csvjet = p4_muon.DeltaR(p4_csvjet);


        if dR_top_csvjet>0.3:
            if top_ptmax>1.0:
                htop_ptmax.Fill(top_ptmax)
            if csvjet_ptmax>1.0:
                hcsvjet_ptmax.Fill(csvjet_ptmax)
            if muon_ptmax>1.0:
                hmuon_ptmax.Fill(muon_ptmax)

        if abs(dR_top_csvjet) > 1.0:
            hdR[0].Fill(dR_top_muon)
            hdR[1].Fill(dR_top_csvjet)
            hdR[2].Fill(dR_muon_csvjet)

        if abs(dR_top_muon-3.0)<1.0 and abs(dR_top_csvjet-3.0)<1.0 and abs(dR_muon_csvjet)<1.0:
            print top_ptmax,csvjet_valmax
            hcsvjet_aftercuts.Fill(top_ptmax,csvjet_valmax)
#~~~~~~~~~~~~~~~~~~~
        '''
        def findcsvjet_oppHem():
            csvjet_ptmax_new = 0.0
            for i in xrange(npossiblejets):
                csvjet_ptmax = chain.GetLeaf(csvjet_str[0]).GetValue(index)
                csvjet_pt = chain.GetLeaf(csvjet_str[0]).GetValue(i)
                if csvjet_pt > csvjet_ptmax_new and csvjet_pt != csvjet_ptmax:
                    csvjet_ptmax_new = csvjet_pt
                    csvjet_etamax_new = chain.GetLeaf(csvjet_str[1]).GetValue(i)
                    csvjet_phimax_new = chain.GetLeaf(csvjet_str[2]).GetValue(i)
                    csvjet_massmax_new = chain.GetLeaf(csvjet_str[3]).GetValue(i) # For now
                    csvjet_valmax_new = chain.GetLeaf(csvjet_str[4]).GetValue(i)
            return csvjet_ptmax_new,csvjet_etamax_new,csvjet_phimax_new,csvjet_massmax_new,csvjet_valmax_new
        '''
        
        if top_massmax > 140 and top_massmax < 250 and top_minMassmax > 50 and top_nSubjetsmax >=3:
            # found top
            htop_aftercuts.Fill(top_ptmax)
            
            #find b-jet in opp. hemisphere
            bjet_index = -1
            for i in xrange(npossiblejets):
                csvjet_pt = chain.GetLeaf(csvjet_str[0]).GetValue(i)
                if csvjet_pt > 1.0:
                    csvjet_etamax = chain.GetLeaf(csvjet_str[1]).GetValue(i)
                    csvjet_phimax = chain.GetLeaf(csvjet_str[2]).GetValue(i)
                    csvjet_massmax = chain.GetLeaf(csvjet_str[3]).GetValue(i)

                    p4_csvjet.SetPtEtaPhiM(csvjet_pt,csvjet_etamax,csvjet_phimax,csvjet_massmax);

                    dR = p4_top.DeltaR(p4_csvjet)

                    if csvjet_pt > csvjet_ptmax and dR > 0.8:
                        csvjet_ptmax = csvjet_pt
                        bjet_index = i
                        found_csvjet = True

                        p4_csvjet.SetPtEtaPhiM(csvjet_pt,csvjet_etamax,csvjet_phimax,csvjet_massmax);
                        csvjet_valmax = chain.GetLeaf(csvjet_str[4]).GetValue(i)

                        dR_top_csvjet = dR
            hcsvjet_oppositeHemisph.Fill(csvjet_ptmax)

            '''
            if dR_top_csvjet > 1.0:
                # found highest pt jet in opposite hemisphere
                hcsvjet_oppositeHemisph.Fill(csvjet_massmax)
            elif npossiblejets >= 2: 
                # find highest pt jet, then check if it's in the opposite hemisphere
                # remove the previous highest pt jet 
                csvjet_ptmax_new,csvjet_etamax_new,csvjet_phimax_new,csvjet_massmax_new,csvjet_valmax_new = findcsvjet_oppHem()
                
                #if csvjet_ptmax_new > 0.0:
                p4_csvjet.SetPtEtaPhiM(csvjet_ptmax_new,csvjet_etamax_new,csvjet_phimax_new,csvjet_massmax_new);
                dR_top_csvjet = p4_top.DeltaR(p4_csvjet);
                
                if dR_top_csvjet > 1.0:
                    # found highest pt jet in opposite hemisphere
                    hcsvjet_oppositeHemisph.Fill(csvjet_massmax_new)
                    
                elif npossiblejets >= 3:
                    csvjet_ptmax_new,csvjet_etamax_new,csvjet_phimax_new,csvjet_massmax_new,csvjet_valmax_new = findcsvjet_oppHem() 
                    # this will not work because we will find the original highest pt, we need a way to remove the old jets...  
                    if csvjet_ptmax_new > 0.0:
                        p4_csvjet.SetPtEtaPhiM(csvjet_ptmax_new,csvjet_etamax_new,csvjet_phimax_new,csvjet_massmax_new);
                        dR_top_csvjet = p4_top.DeltaR(p4_csvjet);

                        if dR_top_csvjet > 1.0:
                            # found highest pt jet in opposite hemisphere
                            hcsvjet_oppositeHemisph.Fill(csvjet_massmax_new)
              '''
################################################################################
# 
################################################################################
ctop = TCanvas( 'ctop', 'Top pt', 10, 10, 1400, 600 )
ctop.Divide(3,1)
for i in range(0,3):
    ctop.cd(1+i)
    if i==0:
        htop_ptmax.Draw()
        htop_ptmax.GetXaxis().SetTitle("Highest p_{T} top jet in the event")
    elif i==1:
        hcsvjet_ptmax.Draw()
        hcsvjet_ptmax.GetXaxis().SetTitle("Highest p_{T} CSV jet in the event")
    elif i==2:
        hmuon_ptmax.GetXaxis().SetTitle("Highest p_{T} muon in the event")
        hmuon_ptmax.Draw()
ctop.Update()
name = "Plots/pt_%s.png" % (tag)
ctop.SaveAs(name)


cdR = TCanvas( 'cdR', 'dR', 30, 30, 1400, 600)
cdR.Divide(3,1)
for i in range(0,3):
    cdR.cd(i+1)
    hdR[i].Draw()
    hdR[i].GetXaxis().SetTitle("dR")
cdR.Update()
name = "Plots/dR_%s.png" % (tag)
cdR.SaveAs(name)

ccsv2d = TCanvas( 'ccsv2d', 'csv2d', 30, 30, 900, 900)
ccsv2d.Divide(1,1)
ccsv2d.cd(i+1)
hcsvjet_aftercuts.GetYaxis().SetTitle("CSV discriminating variable")
hcsvjet_aftercuts.GetXaxis().SetTitle("p_{T} of top jet")
hcsvjet_aftercuts.Draw("COLZ")
hcsvjet_aftercuts.Draw("TEXT SAME")
ccsv2d.Update()
name = "Plots/csv_vs_pt_%s.png" % (tag)
ccsv2d.SaveAs(name)

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

#~~ 
c6 = TCanvas( 'ccsv_6', 'CSV jet eta', 10, 10, 1400, 800 )
c6.Divide(1,1)
c6.cd(1)
hcsvjet_eta.Draw()
c6.Update()

c7 = TCanvas( 'ccsv_7', 'CSV jet phi', 10, 10, 1400, 800 )
c7.Divide(1,1)
c7.cd(1)
hcsvjet_phi.Draw()
c7.Update()

'''
c8 = TCanvas( 'ccsv_8', 'CSV jet mass', 10, 10, 1400, 800 )
c8.Divide(1,1)
c8.cd(1)
hcsvjet_mass.Draw()
c8.Update()
'''

c9 = TCanvas( 'cmuon_9', 'Muon eta', 10, 10, 1400, 800 )
c9.Divide(1,1)
c9.cd(1)
hmuon_eta.Draw()
c9.Update()

c10 = TCanvas( 'cmuon_10', 'Muon phi', 10, 10, 1400, 800 )
c10.Divide(1,1)
c10.cd(1)
hmuon_phi.Draw()
c10.Update()

c11 = TCanvas('top_aftercuts', 'Top mass after cuts', 10,10,1400,800)
c11.Divide(1,1)
c11.cd(1)
htop_aftercuts.Draw()
c11.Update()

c12 = TCanvas('csvjet_oppositeHemisph', 'Highest pt csv jet in opposite Hemisphere', 10,10,1400,800)
c12.Divide(1,1)
c12.cd(1)
hcsvjet_oppositeHemisph.Draw()
c12.Update()

################################################################################
if __name__=="__main__":
    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = raw_input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]

