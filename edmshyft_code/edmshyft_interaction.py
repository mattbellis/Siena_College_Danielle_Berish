#!/usr/bin/env python
# ==============================================================================
# ==============================================================================

from ROOT import gRandom, TH1, TH1D, cout, TCanvas
from ROOT import kRed,kBlack,kBlue
from ROOT import TLorentzVector,TH2D

import ROOT

import sys

import numpy as np

##tag = "ttbar_MC"
tag = "data"

# ==============================================================================
#  Read in the data.
# ==============================================================================

#ROOT.gStyle.SetOptStat(111111111)
ROOT.gStyle.SetOptStat(1)

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
# Assignment! 
# Fill these hisograms
###############################################################################
htop_ptmax = TH1D("htop_ptmax","Highest p_{T} top jet", 80,0,800.0)
hcsvjet_ptmax = TH1D("hcsvjet_ptmax","Highest p_{T} b-jet", 110,0.0,800.0)
hmuon_ptmax = TH1D("hmuon_ptmax","Highest p_{T} muon", 80,0.0,800.0)

hcsvjet_aftercuts = TH2D("hcsvjet_aftercuts","CSV variable vs. top p_{T}", 7,100,800,10,0,1.0)

hdR = []
for i in range(0,3):
    name = "hdR%d" % (i)
    title = ""
    if i==0:
        title = "Top jet vs. muon"
    elif i==1:
        title = "Top jet vs. b-jet"
    elif i==2:
        title = "Muon vs. b-jet"
    hdR.append(TH1D(name,title,65,0,6.5))


# Muon
muon_str = []
muon_str.append("floats_pfShyftTupleMuons_pt_ANA.obj")
muon_str.append("floats_pfShyftTupleMuons_eta_ANA.obj")
muon_str.append("floats_pfShyftTupleMuons_phi_ANA.obj")

# Top Truth
top_truth_str = []
top_truth_str.append("floats_pfShyftTupleTopQuarks_pt_ANA.obj")
top_truth_str.append("floats_pfShyftTupleTopQuarks_eta_ANA.obj")
top_truth_str.append("floats_pfShyftTupleTopQuarks_phi_ANA.obj")
top_truth_str.append("floats_pfShyftTupleTopQuarks_mass_ANA.obj")

# Top
top_str = []
top_str.append("floats_pfShyftTupleJetsLooseTopTag_pt_ANA.obj")
top_str.append("floats_pfShyftTupleJetsLooseTopTag_eta_ANA.obj")
top_str.append("floats_pfShyftTupleJetsLooseTopTag_phi_ANA.obj")
top_str.append("floats_pfShyftTupleJetsLooseTopTag_mass_ANA.obj")
top_str.append("floats_pfShyftTupleJetsLooseTopTag_nSubjets_ANA.obj")
top_str.append("floats_pfShyftTupleJetsLooseTopTag_minMass_ANA.obj") # pairwise mass close to the W mass (minMass >50)

# From Jim Dolen.
#The default top tag selection is to require:
#140< jet mass <250
#minMass > 50
#nSubjets >=3

# CSV jets
csvjet_str = []
csvjet_str.append("floats_pfShyftTupleJetsLooseAK5_pt_ANA.obj")
csvjet_str.append("floats_pfShyftTupleJetsLooseAK5_eta_ANA.obj")
csvjet_str.append("floats_pfShyftTupleJetsLooseAK5_phi_ANA.obj")
csvjet_str.append("floats_pfShyftTupleJetsLooseAK5_mass_ANA.obj")
csvjet_str.append("floats_pfShyftTupleJetsLooseAK5_csv_ANA.obj")

p4 = TLorentzVector()
p4_muon = TLorentzVector()
p4_top = TLorentzVector()
p4_csvjet = TLorentzVector()

p4_top_truth = []
p4_top_truth.append(TLorentzVector())
p4_top_truth.append(TLorentzVector())

#chain.SetBranchStatus('*', 1 )
chain.SetBranchStatus('*', 0 )
for s in muon_str:
    chain.SetBranchStatus(s, 1 )
for s in top_str:
    chain.SetBranchStatus(s, 1 )
for s in csvjet_str:
    chain.SetBranchStatus(s, 1 )
if tag != "data":
    for s in top_truth_str:
        chain.SetBranchStatus(s, 1 )

npossiblejets = 4

nev = chain.GetEntries()
print nev

outfilename = "output_for_response_matrix_%s.dat" % (tag)
outfile = open(outfilename,"w+") 

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

    top_nsubjetsmax = 1.0
    top_minmassmax = 1.0

    csvjet_valmax = -1.0

    njets = 0

    top_index = -1

    if tag != "data":
        # Get the top truth info
        for i in xrange(2):
            pt = chain.GetLeaf(top_truth_str[0]).GetValue(i)
            eta = chain.GetLeaf(top_truth_str[1]).GetValue(i)
            phi = chain.GetLeaf(top_truth_str[2]).GetValue(i)
            mass = chain.GetLeaf(top_truth_str[3]).GetValue(i)

            #print "pt: ",pt
            p4_top_truth[i].SetPtEtaPhiM(pt,eta,phi,mass);


    # Find the top jet!
    for i in xrange(npossiblejets):
        
        top_pt = chain.GetLeaf(top_str[0]).GetValue(i)
        if top_pt > top_ptmax:
            top_ptmax = top_pt
            top_index = i

    if top_index>=0:
        top_ptmax = chain.GetLeaf(top_str[0]).GetValue(top_index)
        top_etamax = chain.GetLeaf(top_str[1]).GetValue(top_index)
        top_phimax = chain.GetLeaf(top_str[2]).GetValue(top_index)
        top_massmax = chain.GetLeaf(top_str[3]).GetValue(top_index)
        top_nsubjetsmax = chain.GetLeaf(top_str[4]).GetValue(top_index)
        top_minmassmax = chain.GetLeaf(top_str[5]).GetValue(top_index)
        found_top = True

        #print top_ptmax
        p4_top.SetPtEtaPhiM(top_ptmax,top_etamax,top_phimax,top_massmax);

    # Find the b-jet in the opposite hemisphere!
    bjet_index = -1
    for i in xrange(npossiblejets):
        csvjet_pt = chain.GetLeaf(csvjet_str[0]).GetValue(i)
        if csvjet_pt > 1.0:
            csvjet_etamax = chain.GetLeaf(csvjet_str[1]).GetValue(i)
            csvjet_phimax = chain.GetLeaf(csvjet_str[2]).GetValue(i)
            csvjet_massmax = chain.GetLeaf(csvjet_str[3]).GetValue(i) # For now

            #print csvjet_pt
            p4.SetPtEtaPhiM(csvjet_pt,csvjet_etamax,csvjet_phimax,csvjet_massmax);
            #print "SET!"

            dR = p4_top.DeltaR(p4);

            # Is this right?
            if csvjet_pt > csvjet_ptmax and dR>0.8:
                csvjet_ptmax = csvjet_pt
                bjet_index = i
                found_csvjet = True

                p4_csvjet.SetPtEtaPhiM(csvjet_pt,csvjet_etamax,csvjet_phimax,csvjet_massmax);
                csvjet_valmax = chain.GetLeaf(csvjet_str[4]).GetValue(i)

                dR_top_csvjet = dR


    # Find the b-jet in the opposite hemisphere!
    muon_index = -1
    for i in xrange(npossiblejets):
        muon_pt = chain.GetLeaf(muon_str[0]).GetValue(i)
        if muon_pt > muon_ptmax:
            muon_ptmax = muon_pt
            muon_etamax = chain.GetLeaf(muon_str[1]).GetValue(i)
            muon_phimax = chain.GetLeaf(muon_str[2]).GetValue(i)
            muon_massmax = 0.105 # For now

            found_muon = True
            p4_muon.SetPtEtaPhiM(muon_ptmax,muon_etamax,muon_phimax,muon_massmax);

    #print "----------------------"
    top_criteria = True
    #print top_criteria
    top_criteria *= 140<top_massmax
    #print 140,top_massmax
    #print top_criteria
    #print 250,top_massmax 
    top_criteria *= 250>top_massmax 
    #print top_criteria
    #print top_minmassmax
    top_criteria *= top_minmassmax>50
    #print top_criteria
    #print top_nsubjetsmax
    top_criteria *= top_nsubjetsmax>=3
    #print top_criteria

    # If we have found a muon, top jet and a CSV jet, then
    # let's analyze this further. 
    found_the_event = False
    if found_csvjet and found_top and found_muon and top_criteria:

        #p4_top.SetPtEtaPhiM(top_ptmax,top_etamax,top_phimax,top_massmax);
        #p4_csvjet.SetPtEtaPhiM(csvjet_ptmax,csvjet_etamax,csvjet_phimax,csvjet_massmax);

        dR_top_muon = p4_top.DeltaR(p4_muon);
        dR_top_csvjet = p4_top.DeltaR(p4_csvjet);
        dR_muon_csvjet = p4_muon.DeltaR(p4_csvjet);

        #if dR_top_csvjet>0.3:
        if 1:
            if top_ptmax>1.0:
                htop_ptmax.Fill(top_ptmax)
            if csvjet_ptmax>1.0:
                hcsvjet_ptmax.Fill(csvjet_ptmax)
            if muon_ptmax>1.0:
                hmuon_ptmax.Fill(muon_ptmax)

        #if abs(dR_top_csvjet) > 1.0:
        if 1:
            hdR[0].Fill(dR_top_muon)
            hdR[1].Fill(dR_top_csvjet)
            hdR[2].Fill(dR_muon_csvjet)

        #if abs(dR_top_muon-3.0)<1.0 and abs(dR_top_csvjet-3.0)<1.0 and abs(dR_muon_csvjet)<1.0:
        #if abs(dR_top_csvjet-3.0)<1.0:
        if dR_top_muon>1.5:
            print top_ptmax,csvjet_valmax
            hcsvjet_aftercuts.Fill(top_ptmax,csvjet_valmax)
            found_the_event = True



    if tag != "data":
        for i in xrange(2):
            output = "%f " % (p4_top_truth[i].Pt())
            if found_the_event == True:
                dR = p4_top.DeltaR(p4_top_truth[i]);
                if dR<0.8 and csvjet_valmax>0.8:
                    output += "%f\n" % (p4_top.Pt())
                else:
                    output += "-1\n"
            else:
                output += "-1\n"

        outfile.write(output)




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

outfile.close()
################################################################################
# 
################################################################################
ctop = TCanvas( 'ctop', 'Top pt', 10, 10, 1400, 600 )
ctop.Divide(3,1)
for i in range(0,3):
    ctop.cd(1+i)
    if i==0:
        htop_ptmax.Draw()
        htop_ptmax.GetXaxis().SetTitle("Highest p_{T} top jet")
    elif i==1:
        hcsvjet_ptmax.Draw()
        hcsvjet_ptmax.GetXaxis().SetTitle("Highest p_{T} b-jet opposite hemisphere top jet")
    elif i==2:
        hmuon_ptmax.GetXaxis().SetTitle("Highest p_{T} muon")
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


################################################################################
if __name__=="__main__":
    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = raw_input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]

