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

from ROOT import gRandom, TH1, TH1D, cout, TCanvas, TLegend
from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import kRed,kBlack,kBlue
from ROOT import RooUnfoldSvd
#from ROOT import RooUnfoldTUnfold

# ==============================================================================
#  Gaussian smearing, systematic translation, and variable inefficiency
# ==============================================================================

def smear(xt):

  if xt<500.0:
    return None

  xeff= 0.3 + (1.0-0.3)/20*(xt/150.0);  #  efficiency
  x= gRandom.Rndm();

  if x>xeff: 
    return None

  xsmear= gRandom.Gaus(-100,50.0);     #  bias and smear

  return xt+xsmear;

# ==============================================================================
#  Example Unfolding
# ==============================================================================

print "==================================== TRAIN ===================================="
response= RooUnfoldResponse (40, 0.0, 1500.0);
hMC_true = TH1D("MC_true","MC: Exponential", 40, 0.0, 1500);
hMC_meas = TH1D("MC_meas","MC: Exponential", 40, 0.0, 1500);


'''
#  Train with a Breit-Wigner, mean 0.3 and width 2.5.
for i in xrange(100000):
  xt= gRandom.BreitWigner (0.3, 2.5);
  x= smear (xt);
  hMC_true.Fill(xt);
  if x!=None:
    response.Fill (x, xt);
    hMC_meas.Fill(x);
  else:
    response.Miss (xt);
'''

# Train with an exponential 
for i in xrange(10000):
    xt = 100+100*gRandom.Exp(2.0)  # paramter is tau, where exp(-t/tau)
    x = smear(xt)
    hMC_true.Fill(xt)
    if x!= None:
        response.Fill(x,xt);
        hMC_meas.Fill(x);
    else:
        response.Miss(xt);

print response

unfold0 = RooUnfoldBayes(response,hMC_meas,4);
#unfold0 = RooUnfoldSvd(response,hMC_meas, 20);  


# MC true, measured, and unfolded histograms 
c1 = TCanvas( 'c1', 'MC Unfolded', 200, 10, 700, 500 )


hMC_true.SetLineColor(kBlack);  
hMC_true.Draw();  # MC raw 
#c1.SaveAs("MC_true.png")

hMC_meas.SetLineColor(kBlue);
hMC_meas.Draw("SAME");  # MC measured
#c1.SaveAs("MC_meas.png")

hMC_reco = unfold0.Hreco();
hMC_reco.SetLineColor(kRed);
hMC_reco.Draw("SAME");        # MC unfolded 
#c1.SaveAs("MC_unfold.png")

c1.Update()


# MC efficiency (meas/raw)
#c2 = TCanvas( 'c2', 'MC_eff', 200, 10, 700, 500)

hMC_eff = hMC_meas.Clone();
hMC_eff.Divide(hMC_true);
#c2.SetLogy();
#hMC_eff.Draw();
#c2.SaveAs("MC_eff.png")

'''
c2.Update()

# MC true corrected by the efficiency 
c5 = TCanvas('c5', 'MC_meas divided by MC_eff', 200, 10, 700, 500)

hMC_meas_over_eff = hMC_meas.Clone()
hMC_meas_over_eff.Divide(hMC_eff);
hMC_meas_over_eff.Draw()
#c5.SaveAs("MC_truth_by_MC_eff.png")

c5.Update()
'''
tau = 1
while tau < 9:
    print "==================================== TEST ====================================="
    hTrue= TH1D ("true", "Toy Data: Exponential", 40, 0.0, 1500.0);
    hMeas= TH1D ("meas", "Toy Data: Exponential", 40, 0.0, 1500.0);

    # Test with an exponential 
    for i in xrange(10000):
        xt = 100 + 100*gRandom.Exp(tau)
        x = smear(xt)
        hTrue.Fill(xt)
        if x!= None:
            hMeas.Fill(x);


    '''
    #  Test with a Gaussian, mean 0 and width 2.
    for i in xrange(10000):
      xt= gRandom.Gaus (0.0, 2.0)
      x= smear (xt);
      hTrue.Fill(xt);
      if x!=None:
        hMeas.Fill(x);
    '''

    '''
    # Data efficiency (meas/raw)
    c4 = TCanvas( 'c4', 'Data_eff', 200, 10, 700, 500)

    hData_eff = hMeas.Clone();
    hData_eff.Divide(hTrue);
    c4.SetLogy();
    hData_eff.Draw();
    #c4.SaveAs("Data_eff.png")

    c4.Update()


    # Data measured corrected by the efficiency 
    #c6 = TCanvas('c6', 'Data measured divided by data_eff', 200, 10, 700, 500)

    #hData_truth = hMeas.Clone()
    #hData_truth.Divide(hData_eff);
    #hData_truth.Draw()
    #c6.SaveAs("Data_truth_by_eff.png")
    #
    #c6.Update()

    # Data truth = MC meas/MC data 
    c7 = TCanvas('c7', 'Data truth = Data corrected by MC eff', 200, 10, 700, 500)

    hData_truth_MC = hMeas.Clone()
    hData_truth_MC.SetName("Data corrected by naive MC efficiency")
    hData_truth_MC.SetTitle("Data corrected by naive MC efficiency")
    hData_truth_MC.Divide(hMC_eff);
    hData_truth_MC.Draw()
    #c7.SaveAs("Data_truth_by_MC.png")

    c7.Update()

    '''
    print "==================================== UNFOLD ==================================="
    unfold= RooUnfoldBayes     (response, hMeas, 4);    #  OR
    #unfold= RooUnfoldSvd     (response, hMeas, 20);   #  OR
    #unfold= RooUnfoldTUnfold (response, hMeas);


    # Data true, measured and unfolded histograms 
    c3 = TCanvas( 'c3', 'Data Unfolded', 200, 10, 700, 500 )

    hTrue.SetLineColor(kBlack);
    hTrue.Draw();     # Data raw
    #c3.SaveAs("Data_true.png")

    hMeas.SetLineColor(kBlue);
    hMeas.Draw("SAME");     # Data measured
    #c3.SaveAs("Data_meas.png")

    hReco= unfold.Hreco();
    unfold.PrintTable (cout, hTrue);
    hReco.SetLineColor(kRed);
    hReco.Draw("SAME");           # Data unfolded 
    #c3.SaveAs("Data_unfold.png")
    
    c3.SaveAs("Data_unfold_Tau%s.png" % tau)

    c3.Update()
    

#========================================================================================
    # Compare data truth, RooUnfold truth, and Naive correction truth 
    
    truth_compare = TCanvas('truth_compare','Comparison of Truth Histograms',200,10,700,500)

    hTruth_naive = hMeas.Clone()
    hTruth_naive.SetTitle("Comparison of Toy Data Truths")
    hTruth_naive.Divide(hMC_eff);
    hTruth_naive.SetLineColor(kBlue)
    hTruth_naive.Draw()

    hTrue.SetLineColor(kBlack)
    hTrue.Draw("SAME")

    hReco.SetLineColor(kRed)
    hReco.Draw("SAME")

    '''
    legend = TLegend(1,1,1,1)
    SetOwnership(legend,0)
    legend.SetFillColor(1)
    legend.AddEntry(hTruth_naive,"F")
    legend.Draw()
    '''

    truth_compare.SaveAs("Truth_Compare_Tau%s.png" % tau)
    truth_compare.Update()
    
    tau = tau*2

#================================================================================
#print "======================================Response matrix========================="
#print response
#c11 = TCanvas('c10','Response matrix',200,10,700,500)
#response.Mresponse().Draw()
################################################################################
if __name__=="__main__":
    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = raw_input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]

