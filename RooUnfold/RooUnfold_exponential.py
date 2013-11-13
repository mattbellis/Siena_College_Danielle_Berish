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
from ROOT import RooUnfoldBayes
from ROOT import kRed,kBlack,kBlue
#from ROOT import RooUnfoldSvd
#from ROOT import RooUnfoldTUnfold

lorange = 0
hirange = 1500
nbins = 15

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

MC_tau = 2
MC_tau_range = 5


data_unfolded_histos = []

while MC_tau < MC_tau_range:

    print "==================================== TRAIN ===================================="
    response= RooUnfoldResponse (nbins,lorange,hirange)
    hMC_true = TH1D("MC_true","MC: Exponential", nbins,lorange,hirange)
    hMC_meas = TH1D("MC_meas","MC: Exponential", nbins,lorange,hirange)


    # Train with an exponential 
    for i in xrange(10000):
        xt = 100+100*gRandom.Exp(MC_tau)  # paramter is tau, where exp(-t/tau)
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
    hMC_true.SetTitle("MC Truth, Measured, and Unfolded")
    hMC_true.Draw();  # MC raw 
    #c1.SaveAs("MC_true.png")

    hMC_meas.SetLineColor(kBlue);
    hMC_meas.Draw("SAME");  # MC measured
    #c1.SaveAs("MC_meas.png")

    hMC_reco = unfold0.Hreco();
    hMC_reco.SetLineColor(kRed);
    hMC_reco.Draw("SAME");        # MC unfolded
    #c1.SaveAs("MC_unfold.png")

    legend = TLegend(0.4,0.7,0.78,0.90)
    legend.SetFillColor(0)
    legend.AddEntry(hMC_true,"Truth information","l")
    legend.AddEntry(hMC_meas,"Raw information","l")
    legend.AddEntry(hMC_reco,"Unfolded","l")
    legend.Draw()

    c1.Update()


    #MC efficiency (meas/raw)
    c2 = TCanvas( 'c2', 'MC_eff', 200, 10, 700, 500)

    hMC_eff = hMC_meas.Clone();
    hMC_eff.Divide(hMC_true);
    hMC_eff.SetTitle("MC Efficiency")
    c2.SetLogy();
    hMC_eff.Draw();
    c2.SaveAs("MC_eff.png")
        
 
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


    
    data_tau = 2 
    data_tau_range = 3
    while data_tau < data_tau_range:
        print "==================================== TEST ====================================="
        hTrue= TH1D ("true", "Toy Data: Exponential", nbins,lorange,hirange)
        hMeas= TH1D ("meas", "Toy Data: Exponential", nbins,lorange,hirange)

        # Test with an exponential 
        for i in xrange(10000):
            xt = 100 + 100*gRandom.Exp(data_tau)
            x = smear(xt)
            hTrue.Fill(xt)
            if x!= None:
                hMeas.Fill(x);


        '''
        # Data efficiency (meas/raw)
        c4 = TCanvas( 'c4', 'Data_eff', 220,220, 700, 500)

        hData_eff = hMeas.Clone();
        hData_eff.Divide(hTrue);
        c4.SetLogy();
        hData_eff.Draw();
        #c4.SaveAs("Data_eff.png")

        c4.Update()


        # Data measured corrected by the efficiency 
        #c6 = TCanvas('c6', 'Data measured divided by data_eff', 240,240, 700, 500)

        #hData_truth = hMeas.Clone()
        #hData_truth.Divide(hData_eff);
        #hData_truth.Draw()
        #c6.SaveAs("Data_truth_by_eff.png")
        #
        #c6.Update()
        '''

        # Data truth = MC meas/MC data 
        c7 = TCanvas('c7', 'Data truth = Data corrected by MC eff', 250,250, 700, 500)

        hData_truth_MC = hMeas.Clone()
        hData_truth_MC.SetName("Data corrected by naive MC efficiency")
        hData_truth_MC.SetTitle("Data corrected by naive MC efficiency")
        hData_truth_MC.Divide(hMC_eff);
        hData_truth_MC.SetLineColor(kBlue)
        hData_truth_MC.SetLineWidth(3)
        hData_truth_MC.Draw()
        #c7.SaveAs("Data_truth_by_MC.png")

        hTrue.SetLineColor(kBlack)
        hTrue.SetLineWidth(3)
        hTrue.Draw("SAME")

        legend = TLegend(0.4,0.7,0.78,0.90)
        legend.SetFillColor(0)
        legend.AddEntry(hData_truth_MC,"Naive efficieny correction", "l")
        legend.AddEntry(hTrue,"Truth information","l")
        legend.Draw()
        
        c7.SaveAs("NaiveTruthCorrection.png")

        c7.Update()


        print "==================================== UNFOLD ==================================="
        unfold= RooUnfoldBayes     (response, hMeas, 4);    #  OR
        #unfold= RooUnfoldSvd     (response, hMeas, 20);   #  OR
        #unfold= RooUnfoldTUnfold (response, hMeas);


        # Data true, measured and unfolded histograms 
        c3 = TCanvas( 'c3', 'Data Unfolded', 250,250, 700, 500 )

        hTrue.SetLineColor(kBlack);
        hTrue.SetTitle("Data Truth, Measured, and Unfolded")
        hTrue.Draw();     # Data raw
        #c3.SaveAs("Data_true.png")

        hMeas.SetLineColor(kBlue);
        hMeas.SetLineWidth(3)
        hMeas.Draw("SAME");     # Data measured
        #c3.SaveAs("Data_meas.png")

        hReco= unfold.Hreco();
        unfold.PrintTable (cout, hTrue);
        hReco.SetLineColor(kRed);

        name = "hreco_MCtau%d_datatau%d" % (int(MC_tau),int(data_tau))
        hReco.SetName(name)
        data_unfolded_histos.append(hReco)

        #hReco.SetTitle("Data Truth, Measured, and Unfolded")
        hReco.Draw("SAME");           # Data unfolded 
        c3.SaveAs("Data_unfold_MCTau%s.png" % MC_tau)
       
        legend = TLegend(0.4,0.7,0.78,0.90)
        legend.SetFillColor(0)
        legend.AddEntry(hTrue,"Truth information","l")
        legend.AddEntry(hMeas,"Raw information","l")
        legend.AddEntry(hReco,"Unfolded","l")
        legend.Draw()
         
        c3.SaveAs("Data_unfold_Tau%s.png" % data_tau)

        c3.Update()
        
        #################
        reconstruct = TCanvas('reconstruct','Data reconstructed',250,250,700,500)
        hReco.Draw()
        reconstruct.Update()
        
        '''
        #========================================================================================
        # Compare data truth, RooUnfold truth, and Naive correction truth 
        
        truth_compare = TCanvas('truth_compare','Comparison of Truth Histograms',200,10,700,500)

        hTruth_naive = hMeas.Clone()
        hTruth_naive.SetTitle("Comparison of Toy Data Truths")
        hTruth_naive.Divide(hMC_eff);
        hTruth_naive.SetLineColor(kBlue)
        hTruth_naive.SetLineWidth(3)
        hTruth_naive.Draw()

        hTrue.SetLineColor(kBlack)
        hTrue.SetLineWidth(3)
        hTrue.Draw("SAME")

        hReco.SetLineColor(kRed)
        hReco.SetLineWidth(3)
        hReco.Draw("SAME")

        legend = TLegend(0.4,0.7,0.78,0.90)
        legend.SetFillColor(0)
        legend.AddEntry(hTrue,"Truth information","l")
        legend.AddEntry(hTruth_naive,"Naive efficiency correction","l")
        legend.AddEntry(hReco,"Unfolded","l")
        legend.Draw()

        truth_compare.SaveAs("TruthCompare.png")
        truth_compare.Update()
        '''

        data_tau += 1
    MC_tau += 1

# Print all the unfolded histos
print "HERE IS WHERE WE ARE GOING TO PRINT THEM ALL........"
canunfold = TCanvas("canunfold","All the unfolded histos",100,100,600,600)
canunfold.Divide(1,1)
colors = [2,3,4,5,6,7]
for i,h in enumerate(data_unfolded_histos):
    print h
    h.SetLineColor(colors[i])
    if i==0:
        h.Draw()
    else:
        h.Draw("same")
    canunfold.Update()

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

