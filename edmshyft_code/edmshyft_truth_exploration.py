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

################################################################################
# Try to see if two particles have roughly the same angular component of their
# momentum. 
################################################################################
def truth_matching(p0, p1, max_dR=0.8):

    # p[0] = pT
    # p[1] = eta
    # p[2] = phi

    # dR = sqrt((delta eta)**2 + (delta phi**2))
    dR = np.sqrt((p0[1]-p1[1])**2 + (p0[2]-p1[2])**2)

    if dR<max_dR:
        return True
    else:
        return False



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

hHadrTop = TH1D("HadrTop","pT Distribution of the hadronically decaying top",80,0,800)

top_histos = []
jet_histos = []

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
top_all = []
jet_all = []

binNum = 20
while binNum < 820:
    nameTop = "htop_%d" % (binNum)
    nameJet = "hjet_%d" % (binNum)
    top_all.append(TH1D(nameTop,"pT Distribution of the hadronically decaying top",80,0,800))
    jet_all.append(TH1D(nameJet,"pT Distribution of the top jet",80,0,800))
    binNum += 20


###################################################################################
# Top Truth
truth_str = []
truth_str.append("floats_pfShyftTupleGenParticles_pdgId_ANA.obj")
truth_str.append("floats_pfShyftTupleGenParticles_status_ANA.obj")
truth_str.append("floats_pfShyftTupleGenParticles_pt_ANA.obj")
truth_str.append("floats_pfShyftTupleGenParticles_eta_ANA.obj")
truth_str.append("floats_pfShyftTupleGenParticles_phi_ANA.obj")

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

#pT_low = 550
#pT_high = 650
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
    top_antitop_eta = []
    top_antitop_phi = []

    #print '---------------------'
    for i in xrange(32):
        pdg = chain.GetLeaf(truth_str[0]).GetValue(i)
        #status = chain.GetLeaf(truth_str[1]).GetValue(i)
        pt = chain.GetLeaf(truth_str[2]).GetValue(i)
        eta = chain.GetLeaf(truth_str[3]).GetValue(i)
        phi = chain.GetLeaf(truth_str[4]).GetValue(i)


        if pdg == 6:
            htop_pt.Fill(pt)
            top_antitop_pt.append(pt)
            top_antitop_eta.append(eta)
            top_antitop_phi.append(phi)
            flag_tops += 1
        elif pdg == -6:
            hantiTop_pt.Fill(pt)
            top_antitop_pt.append(pt)
            top_antitop_eta.append(eta)
            top_antitop_phi.append(phi)
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
    classif = []
    if len(decay) > 0:
        classif = classify(decay[0],decay[1],decay[2],decay[3])
        
        #count how many Ws decay hadronically vs. leptonically
        if classif[0] == 0:
            hadron_count += 1
        elif classif[1] == 0:
            hadron_count += 1
        elif classif[0] == 1:
            lepton_count += 1
        elif classif[1] == 1:
            lepton_count += 1

        #plot semi-leptonically decaying events
        if classif == [0,1]:
            htop_lepton.Fill(top_antitop_pt[1])
            htop_hadron.Fill(top_antitop_pt[0])
            semi_lepton_count += 1
        elif classif == [1,0]:
            htop_lepton.Fill(top_antitop_pt[0])
            htop_hadron.Fill(top_antitop_pt[1])
            semi_lepton_count += 1
        else:
            not_semi_lepton_count += 1

    
    pT_low = 0
    pT_high = 20
    histo = 0

    while pT_high < 900:
        
        top_pt = 0
        if classif == [0,1] and top_antitop_pt[0] < pT_high and top_antitop_pt[0] > pT_low:
            hHadrTop.Fill(top_antitop_pt[0])
            #top_histos.append(hHadrTop)
            top_all[histo].Fill(top_antitop_pt[0])
            for i in xrange(2):
                top_pt = chain.GetLeaf(top_str[0]).GetValue(i)
                top_eta = chain.GetLeaf(top_str[1]).GetValue(i)
                top_phi = chain.GetLeaf(top_str[2]).GetValue(i)

                is_truth_matched = truth_matching([top_antitop_pt[0],top_antitop_eta[0],top_antitop_phi[0]],[top_pt,top_eta,top_phi])

                if top_pt>0 and is_truth_matched:
                    htop_jet.Fill(top_pt)
                    #jet_histos.append(htop_jet)

                    jet_all[histo].Fill(top_pt)

        elif classif == [1,0] and top_antitop_pt[1] < pT_high and top_antitop_pt[1] > pT_low:
            hHadrTop.Fill(top_antitop_pt[1])
            #top_histos.append(hHadrTop)
            top_all[histo].Fill(top_antitop_pt[1])
            for i in xrange(2):
                top_pt = chain.GetLeaf(top_str[0]).GetValue(i)
                top_eta = chain.GetLeaf(top_str[1]).GetValue(i)
                top_phi = chain.GetLeaf(top_str[2]).GetValue(i)

                is_truth_matched = truth_matching([top_antitop_pt[1],top_antitop_eta[1],top_antitop_phi[1]],[top_pt,top_eta,top_phi])

                if top_pt > 0 and is_truth_matched:
                    htop_jet.Fill(top_pt)
                    #jet_histos.append(htop_jet)
                    
                    jet_all[histo].Fill(top_pt)

        pT_high += 20
        pT_low += 20
        histo += 1



print "Hadronically decaying W: ", hadron_count    # W bosons that decay hadronically
print "Leptonically decaying W: ", lepton_count    # W bosons that decay leptonically
print "Semi_leptonically decaying ttbar events: ", semi_lepton_count  # Events in which one W decays hadronically and one W decays leptonically
print "Not Semi_leptonically decaying ttbar events: ", not_semi_lepton_count
################################################################################
# Histograms of the pT distribution of the truth top and antitop 
################################################################################
ctop = TCanvas('ctop','Top pt', 10, 10, 1400, 1000)
print "===================================="
print "Top exponential"
htop_pt.Fit("expo","","",115,650)
#fitparam = htop_pt.GetFunction("expo")
#const = fitparam.GetParameter(0)
#constError = fitparam.GetParError(0)
#slope = fitparam.GetParameter(1)
#slopeError = fitparam.GetParError(1)
htop_pt.Draw()
ctop.Update()

#print "PRINTING PARAMETER"
#print const, "+/-", constError
#print slope, "+/-", slopeError

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

creco = TCanvas('creco', 'Hadronically decayed tops',10,10,1400,1000)
creco.Divide(2,1,0.02,0.02)
creco.cd(1)
hHadrTop.Draw()
creco.cd(2)
htop_jet.Draw()
creco.Update()


#############################################################################################################
f = open("Gaussian_Params.dat","w")
#############################################################################################################
cTopsJets100 = TCanvas('cTopsJets100','Hadronically Decayed Tops and Reco Jets',10,10,1400,1000)
cTopsJets100.Divide(2,5,0.02,0.02)

i = 0
space = 1

while i <= 4:
    cTopsJets100.cd(space)
    top_all[i].Draw()
    cTopsJets100.cd(space+1)
    #jet_all[i].Fit("gaus","","",150,300)
    jet_all[i].Fit("gaus")
    
    params = jet_all[i].GetFunction("gaus")
    mean = params.GetParameter(1)
    meanError = params.GetParError(1)
    sigma = params.GetParameter(2)
    sigmaError = params.GetParError(2)
    output = "%f %f %f %f\n" % (mean, meanError, sigma, sigmaError)
    f.write(output)
    
    jet_all[i].Draw()
    
    i += 1
    space += 2
cTopsJets100.Update()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cTopsJets200 = TCanvas('cTopsJets200','Hadronically Decayed Tops and Reco Jets',10,10,1400,1000)
cTopsJets200.Divide(2,5,0.02,0.02)

i = 5
space = 1
xRange = 0

while i <= 9:
    cTopsJets200.cd(space)
    top_all[i].Draw()
    cTopsJets200.cd(space+1)
    #jet_all[i].Fit("gaus","","",150,300)
    jet_all[i].Fit("gaus")
    
    params = jet_all[i].GetFunction("gaus")
    mean = params.GetParameter(1)
    meanError = params.GetParError(1)
    sigma = params.GetParameter(2)
    sigmaError = params.GetParError(2)
    output = "%f %f %f %f\n" % (mean, meanError, sigma, sigmaError)
    f.write(output)
    
    jet_all[i].Draw()
    
    i += 1
    space += 2
    xRange += 20
cTopsJets200.Update()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cTopsJets300 = TCanvas('cTopsJets300','Hadronically Decayed Tops and Reco Jets',10,10,1400,1000)
cTopsJets300.Divide(2,5,0.02,0.02)

i = 10
space = 1

while i <= 14:
    cTopsJets300.cd(space)
    top_all[i].Draw()
    cTopsJets300.cd(space+1)
    #jet_all[i].Fit("gaus","","",150,400)
    fit = jet_all[i].Fit("gaus")
    
    params = jet_all[i].GetFunction("gaus")
    mean = params.GetParameter(1)
    meanError = params.GetParError(1)
    sigma = params.GetParameter(2)
    sigmaError = params.GetParError(2)
    output = "%f %f %f %f\n" % (mean, meanError, sigma, sigmaError)
    f.write(output)
    
    jet_all[i].Draw()
    
    i += 1
    space += 2
cTopsJets300.Update()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cTopsJets400 = TCanvas('cTopsJets400','Hadronically Decayed Tops and Reco Jets',10,10,1400,1000)
cTopsJets400.Divide(2,5,0.02,0.02)

i = 15
space = 1

while i <= 19:
    cTopsJets400.cd(space)
    top_all[i].Draw()
    cTopsJets400.cd(space+1)
    #jet_all[i].Fit("gaus","","",150,400)
    jet_all[i].Fit("gaus")
    
    params = jet_all[i].GetFunction("gaus")
    mean = params.GetParameter(1)
    meanError = params.GetParError(1)
    sigma = params.GetParameter(2)
    sigmaError = params.GetParError(2)
    output = "%f %f %f %f\n" % (mean, meanError, sigma, sigmaError)
    f.write(output)
    
    jet_all[i].Draw()
    
    i += 1
    space += 2
cTopsJets400.Update()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cTopsJets500 = TCanvas('cTopsJets500','Hadronically Decayed Tops and Reco Jets',10,10,1400,1000)
cTopsJets500.Divide(2,5,0.02,0.02)

i = 20
space = 1

while i <= 24:
    cTopsJets500.cd(space)
    top_all[i].Draw()
    cTopsJets500.cd(space+1)
    #jet_all[i].Fit("gaus","","",200,600)
    jet_all[i].Fit("gaus")
    
    params = jet_all[i].GetFunction("gaus")
    mean = params.GetParameter(1)
    meanError = params.GetParError(1)
    sigma = params.GetParameter(2)
    sigmaError = params.GetParError(2)
    output = "%f %f %f %f\n" % (mean, meanError, sigma, sigmaError)
    f.write(output)
    
    jet_all[i].Draw()
    
    i += 1
    space += 2
cTopsJets500.Update()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cTopsJets600 = TCanvas('cTopsJets600','Hadronically Decayed Tops and Reco Jets',10,10,1400,1000)
cTopsJets600.Divide(2,5,0.02,0.02)

i = 25
space = 1

while i <= 29:
    cTopsJets600.cd(space)
    top_all[i].Draw()
    cTopsJets600.cd(space+1)
    #jet_all[i].Fit("gaus","","",400,700)
    jet_all[i].Fit("gaus")
    
    params = jet_all[i].GetFunction("gaus")
    mean = params.GetParameter(1)
    meanError = params.GetParError(1)
    sigma = params.GetParameter(2)
    sigmaError = params.GetParError(2)
    output = "%f %f %f %f\n" % (mean, meanError, sigma, sigmaError)
    f.write(output)
    
    jet_all[i].Draw()
    
    i += 1
    space += 2
cTopsJets600.Update()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cTopsJets700 = TCanvas('cTopsJets700','Hadronically Decayed Tops and Reco Jets',10,10,1400,1000)
cTopsJets700.Divide(2,5,0.02,0.02)

i = 30
space = 1

while i <= 34:
    cTopsJets700.cd(space)
    top_all[i].Draw()
    cTopsJets700.cd(space+1)
    #jet_all[i].Fit("gaus","","",150,400)
    jet_all[i].Fit("gaus")
    
    params = jet_all[i].GetFunction("gaus")
    mean = params.GetParameter(1)
    meanError = params.GetParError(1)
    sigma = params.GetParameter(2)
    sigmaError = params.GetParError(2)
    output = "%f %f %f %f\n" % (mean, meanError, sigma, sigmaError)
    f.write(output)
    
    jet_all[i].Draw()
    
    i += 1
    space += 2
cTopsJets700.Update()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cTopsJets800 = TCanvas('cTopsJets800','Hadronically Decayed Tops and Reco Jets',10,10,1400,1000)
cTopsJets800.Divide(2,5,0.02,0.02)

i = 35
space = 1

while i <= 39:
    cTopsJets800.cd(space)
    top_all[i].Draw()
    cTopsJets800.cd(space+1)
    #jet_all[i].Fit("gaus","","",150,400)
    jet_all[i].Fit("gaus")
    
    params = jet_all[i].GetFunction("gaus")
    mean = params.GetParameter(1)
    meanError = params.GetParError(1)
    sigma = params.GetParameter(2)
    sigmaError = params.GetParError(2)
    output = "%f %f %f %f\n" % (mean, meanError, sigma, sigmaError)
    f.write(output)
    
    jet_all[i].Draw()
    
    i += 1
    space += 2
cTopsJets800.Update()
#######################################################################
f.close()

########################################################################################################
'''
ctopjet = TCanvas('ctopjet', 'Tops jets', 10, 10, 1400, 600)
htop_jet.Draw()
ctopjet.Update()

cHadrTop = TCanvas('cHadrTop', 'Hadronic Tops in Semi-Lep. Events', 10, 10, 1400, 600)
hHadrTop.Draw()
cHadrTop.Update()
'''
################################################################################
if __name__=="__main__":
    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = raw_input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]

