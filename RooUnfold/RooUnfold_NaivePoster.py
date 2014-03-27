#!/usr/bin/env python
# ==============================================================================
#  File and Version Information:
#       $Id: RooUnfoldExample.py 302 2011-09-30 20:39:20Z T.J.Adye $
#
#  Description:
#       Simple example usage of the RooUnfold package using toy MC.
#
#  Author: Tim Adye <T.J.Adye@rl.ac.uk>
#
# ==============================================================================

from ROOT import gRandom, TH1, TH1D, cout, TCanvas, TLegend, TFile
from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
#from ROOT import RooUnfoldBayes
from ROOT import kRed,kBlack,kBlue,kGreen
from ROOT import RooUnfoldSvd
#from ROOT import RooUnfoldTUnfold

lorange = -10
hirange = 10
nbins = 40
kreg = 20

# ==============================================================================
#  Gaussian smearing, systematic translation, and variable inefficiency
# ==============================================================================

def smear(xt):

    #if xt<500.0:
    #return None

  xeff= 0.3 + (1.0-0.3)/20*(xt+10.0);  #  efficiency
  x= gRandom.Rndm();

  if x>xeff: 
    return None

  xsmear= gRandom.Gaus(-2.5,0.2);     #  bias and smear
  #xsmear = gRandom.Gaus(1.1212,0.008379);

  return xt+xsmear;
###################################################################################
# ==============================================================================
#  Example Unfolding
# ==============================================================================
# Monte Carlo - BW

print "==================================== TRAIN ===================================="
response= RooUnfoldResponse (nbins,lorange,hirange)
hMC_true = TH1D("MC","MC: Exponential", nbins,lorange,hirange)
hMC_meas = TH1D("MC_meas","MC: Exponential", nbins,lorange,hirange)

# Train with an BW 
for i in xrange(100000):
    xt = gRandom.BreitWigner(0.3,2.5)  
    x = smear(xt)
    hMC_true.Fill(xt)
    if x!= None:
        response.Fill(x,xt);
        hMC_meas.Fill(x);
    else:
        response.Miss(xt);


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MC true, measured, and unfolded histograms 
c1 = TCanvas( 'c1', 'MC', 200, 10, 700, 500 )


hMC_true.SetLineColor(kBlack);  
hMC_true.SetTitle('MC Sample A: Breit Wigner')
hMC_true.SetLineWidth(3)
hMC_true.Draw();  # MC raw 

hMC_meas.SetLineColor(kBlue);
hMC_meas.SetLineWidth(3)
hMC_meas.Draw("SAME");  # MC measured

legend = TLegend(0.70,0.6,0.98,0.75)
legend.SetFillColor(0)
legend.AddEntry(hMC_true,"Truth MC","l")
legend.AddEntry(hMC_meas,"Reconstructed MC","l")
legend.Draw()
c1.SaveAs("MC_BW.png")

c1.Update()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#MC efficiency (meas/raw)
c2 = TCanvas( 'c2', 'MC_eff', 200, 10, 700, 500)

hMC_eff = hMC_meas.Clone();
hMC_eff.Divide(hMC_true);
hMC_eff.SetTitle("MC Efficiency")
hMC_eff.SetLineColor(kGreen+2)
c2.SetLogy();
hMC_eff.Draw();
c2.SaveAs("MCEff_BW.png")

c2.Update()

#===============================================================================================
# Monte Carlo - Gaussian

print "==================================== TRAIN ===================================="
responseG = RooUnfoldResponse (nbins,lorange,hirange)
hMC_trueG = TH1D("MC","MC: Exponential", nbins,lorange,hirange)
hMC_measG = TH1D("MC_meas","MC: Exponential", nbins,lorange,hirange)

# Train with an Gaussian 
for i in xrange(100000):
    xt = gRandom.Gaus(0.3,2.5)  
    x = smear(xt)
    hMC_trueG.Fill(xt)
    if x!= None:
        responseG.Fill(x,xt);
        hMC_measG.Fill(x);
    else:
        responseG.Miss(xt);


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MC true, measured, and unfolded histograms 
c3 = TCanvas( 'c3', 'MC', 200, 10, 700, 500 )


hMC_trueG.SetLineColor(kBlack);  
hMC_trueG.SetTitle('MC Sample B: Gaussian')
hMC_trueG.SetLineWidth(3)
hMC_trueG.Draw();  # MC raw 

hMC_measG.SetLineColor(kBlue);
hMC_measG.SetLineWidth(3)
hMC_measG.Draw("SAME");  # MC measured

legendG = TLegend(0.7,0.6,0.98,0.75)
legendG.SetFillColor(0)
legendG.AddEntry(hMC_trueG,"Truth MC","l")
legendG.AddEntry(hMC_measG,"Reconstructed MC","l")
legendG.Draw()
c3.SaveAs("MC_G.png")

c3.Update()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#MC efficiency (meas/raw)
c4 = TCanvas( 'c4', 'MC_eff', 200, 10, 700, 500)

hMC_effG = hMC_measG.Clone();
hMC_effG.Divide(hMC_trueG);
hMC_effG.SetTitle("MC Efficiency")
hMC_effG.SetLineColor(kGreen+2)
c4.SetLogy();
hMC_effG.Draw();
c4.SaveAs("MCEff_G.png")

c4.Update()




#===================================================================================================
# "Data"

print "==================================== TEST ====================================="
hTrue= TH1D ("true", "Toy Data: Exponential", nbins,lorange,hirange)
hMeas= TH1D ("meas", "Toy Data: Exponential", nbins,lorange,hirange)

# Test with an gaussian 
for i in xrange(10000):
    xt = gRandom.Gaus(0.3,2.5)
    x = smear(xt)
    hTrue.Fill(xt)
    if x!= None:
        hMeas.Fill(x);


# Reconstructed data
c6 = TCanvas('c6','Data Reconstructed',200,10,700,500)

hMeas.SetTitle('"Data" Reconstructed')
hMeas.SetLineWidth(3)
hMeas.SetLineColor(kBlue)
hMeas.Draw()

c6.SaveAs("DataReconstructed.png")
c6.Update()

# Naively corrected data - BW 
c7 = TCanvas('c7', 'Data truth = Data corrected by MC eff', 200,10, 700, 500)

hData_truth_MC = hMeas.Clone()
hData_truth_MC.SetName("Acceptance Correction")
hData_truth_MC.SetTitle("Acceptance Correction")
hData_truth_MC.Divide(hMC_eff);
hData_truth_MC.SetLineColor(kRed)
hData_truth_MC.SetLineWidth(3)
hData_truth_MC.Draw()

hTrue.SetLineColor(kBlack)
hTrue.SetLineWidth(3)
hTrue.Draw("SAME")

legend = TLegend(0.7,0.6,0.98,0.75)
legend.SetFillColor(0)
legend.AddEntry(hData_truth_MC,"Acceptance correction", "l")
legend.AddEntry(hTrue,"Data Truth","l")
legend.Draw()

c7.SaveAs("NaiveDataTruthCorrectionBW.png")

c7.Update()


# Naively corrected data - G 
c8 = TCanvas('c8', 'Data truth = Data corrected by MC eff', 200,10, 700, 500)

hData_truth_MCG = hMeas.Clone()
hData_truth_MCG.SetName("Acceptance Correction")
hData_truth_MCG.SetTitle("Acceptance Correction")
hData_truth_MCG.Divide(hMC_effG);
hData_truth_MCG.SetLineColor(kRed)
hData_truth_MCG.SetLineWidth(3)
hData_truth_MCG.SetMaximum(1200)
hData_truth_MCG.Draw()

hTrue.SetLineColor(kBlack)
hTrue.SetLineWidth(3)
hTrue.Draw("SAME")

legend = TLegend(0.7,0.6,0.98,0.75)
legend.SetFillColor(0)
legend.AddEntry(hData_truth_MCG,"Acceptance correction", "l")
legend.AddEntry(hTrue,"Data Truth","l")
legend.Draw()

c8.SaveAs("NaiveDataTruthCorrectionG.png")

c8.Update()
################################################################################
if __name__=="__main__":
    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = raw_input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]

