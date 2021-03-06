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
from ROOT import kRed,kBlack,kBlue
from ROOT import RooUnfoldSvd
#from ROOT import RooUnfoldTUnfold

lorange = 200
hirange = 1500
nbins = 15
kreg = 10

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

  #xsmear= gRandom.Gaus(-100,50.0);     #  bias and smear
  xsmear = gRandom.Gaus(1.1212,0.008379);

  return xt+xsmear;
###################################################################################

hTrue= TH1D ("true", "Toy Data: Exponential", nbins,lorange,hirange)
hMeas= TH1D ("meas", "Toy Data: Exponential", nbins,lorange,hirange)

# Test with an exponential 
for i in xrange(10000):
    xt = 200 + 5*gRandom.Exp(1.0/0.01266)
    x = smear(xt)
    hTrue.Fill(xt)
    if x!= None:
        hMeas.Fill(x);
# ==============================================================================
#  Example Unfolding
# ==============================================================================
MC_tau = .010
MC_tau_range = 0.015 

data_tau = 0
count = 0

data_truth_histos = []
data_unfolded_histos = []

sampleNum = 0

while MC_tau < MC_tau_range:

    print "==================================== TRAIN ===================================="
    response= RooUnfoldResponse (nbins,lorange,hirange)
    hMC_true = TH1D("MC","MC: Exponential", nbins,lorange,hirange)
    hMC_meas = TH1D("MC_meas","MC: Exponential", nbins,lorange,hirange)

    #MC_tau = 1.0/MC_tau


    # Train with an exponential 
    for i in xrange(100000):
        xt = 200+5*gRandom.Exp(1.0/MC_tau)  # paramter is tau, where exp(-t/tau)
        x = smear(xt)
        hMC_true.Fill(xt)
        if x!= None:
            response.Fill(x,xt);
            hMC_meas.Fill(x);
        else:
            response.Miss(xt);

        #print xt
        #print x

    #exit()
    print response

    #unfold0 = RooUnfoldBayes(response,hMC_meas,4);
    unfold0 = RooUnfoldSvd(response,hMC_meas, kreg);  

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if sampleNum == 0:
        sampleName = "A"
    elif sampleNum == 1:
        sampleName = "B"
    elif sampleNum == 2:
        sampleName = "C"

    # MC true, measured, and unfolded histograms 
    c1 = TCanvas( 'c1', 'MC', 200, 10, 700, 500 )
    

    hMC_true.SetLineColor(kBlack);  
    hMC_true.SetTitle("MC Sample "+sampleName+';Boosted top p_T (GeV/c)')
    hMC_true.SetLineWidth(3)
    hMC_true.Draw();  # MC raw 
    #c1.SaveAs("MC_truth.png")

    hMC_meas.SetLineColor(kBlue);
    hMC_meas.SetLineWidth(3)
    hMC_meas.Draw("SAME");  # MC measured
    #c1.SaveAs("MC_reconstructed.png")

    #hMC_reco = unfold0.Hreco();
    #hMC_reco.SetLineColor(kRed);
    #hMC_reco.Draw("SAME");        # MC unfolded
    #c1.SaveAs("MC_unfold.png")
    
    hMC_true.SetMaximum(22000)
    legend = TLegend(0.4,0.7,0.78,0.90)
    legend.SetFillColor(0)
    legend.AddEntry(hMC_true,"Truth MC","l")
    legend.AddEntry(hMC_meas,"Reconstructed MC","l")
    #legend.AddEntry(hMC_reco,"Unfolded MC","l")
    legend.Draw()
    c1.SaveAs("MC_tau%.3f.png" % float(MC_tau))

    c1.Update()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''
    #MC efficiency (meas/raw)
    c2 = TCanvas( 'c2', 'MC_eff', 200, 10, 700, 500)

    hMC_eff = hMC_meas.Clone();
    hMC_eff.Divide(hMC_true);
    hMC_eff.SetTitle("MC Efficiency")
    c2.SetLogy();
    hMC_eff.Draw();
    c2.SaveAs("MC_eff_MCTau%.3f.png" % float(MC_tau))
    '''    
 
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


    
    data_tau = 0.01266 
    data_tau_range = 1 
    while data_tau < data_tau_range:
        print "==================================== TEST ====================================="
        '''
        hTrue= TH1D ("true", "Toy Data: Exponential", nbins,lorange,hirange)
        hMeas= TH1D ("meas", "Toy Data: Exponential", nbins,lorange,hirange)

        # Test with an exponential 
        for i in xrange(10000):
            xt = 200 + 5*gRandom.Exp(1.0/data_tau)
            x = smear(xt)
            hTrue.Fill(xt)
            if x!= None:
                hMeas.Fill(x);
        '''

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
        '''
        # Naively corrected data  
        c7 = TCanvas('c7', 'Data truth = Data corrected by MC eff', 250,250, 700, 500)

        hData_truth_MC = hMeas.Clone()
        hData_truth_MC.SetName("Data corrected by MC efficiency (Naive Correction)")
        hData_truth_MC.SetTitle("Data corrected by MC efficiency (Naive Correction), MCTau: %.3f, DataTau: %.5f;Boosted top p_T (GeV/c)" %(float(MC_tau),float(data_tau)))
        hData_truth_MC.Divide(hMC_eff);
        hData_truth_MC.SetLineColor(kBlue)
        hData_truth_MC.SetLineWidth(3)
        hData_truth_MC.SetMaximum(4000)
        hData_truth_MC.Draw()
        #c7.SaveAs("Data_truth_by_MC.png")

        hTrue.SetLineColor(kBlack)
        hTrue.SetLineWidth(3)
        hTrue.Draw("SAME")

        legend = TLegend(0.4,0.7,0.78,0.90)
        legend.SetFillColor(0)
        legend.AddEntry(hData_truth_MC,"Naive efficieny correction", "l")
        legend.AddEntry(hTrue,"Data Truth","l")
        legend.Draw()
        
        c7.SaveAs("NaiveDataTruthCorrection_MCTau%.3f_DataTau%.5f.png" % (float(MC_tau),float(data_tau)))

        c7.Update()

        '''

        print "==================================== UNFOLD ==================================="
        #unfold= RooUnfoldBayes     (response, hMeas, 4);    #  OR
        unfold= RooUnfoldSvd     (response, hMeas, kreg);   #  OR
        #unfold= RooUnfoldTUnfold (response, hMeas);

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Data true, measured and unfolded histograms 
        c3 = TCanvas( 'c3', 'Data Unfolded', 250,250, 700, 500 )

        hTrue.SetLineColor(kBlack);
        hTrue.SetLineWidth(3)
        hTrue.SetTitle('"Data";Boosted top p_T (GeV/c)')
        hTrue.Draw();     # Data truth
        #c3.SaveAs("Data_true.png")

        hMeas.SetLineColor(kBlue);
        hMeas.SetLineWidth(3)
        hMeas.Draw("SAME");     # Data reconstructed
        #c3.SaveAs("Data_meas.png")
        
        hReco= unfold.Hreco();
        unfold.PrintTable (cout, hTrue);
        #hReco.SetLineColor(kRed);
        hReco.SetLineWidth(3)

        #if data_tau == 2:
        if 1:
            name = "Data"
            hReco.SetName(name)
            data_unfolded_histos.append(hReco)
            hTrue.SetName(name)
            data_truth_histos.append(hTrue)

        #hReco.SetTitle("Data Truth, Reconstructed, and Unfolded")
        #hReco.Draw("SAME");           # Data unfolded 

        legend = TLegend(0.4,0.7,0.78,0.90)
        legend.SetFillColor(0)
        legend.AddEntry(hTrue,'"Data" Truth',"l")
        legend.AddEntry(hMeas,'"Data" Reconstructed',"l")
        #legend.AddEntry(hReco,"Data Unfolded","l")
        legend.Draw()
         
        c3.SaveAs("Data_MCTau%.3f_dataTau%.5f.png" % (float(MC_tau),float(data_tau)))

        c3.Update()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
        #################
        '''
        reconstruct = TCanvas('reconstruct','Data reconstructed',250,250,700,500)
        print "Number unfolded: ", hReco.GetEntries()
        print hReco.GetEffectiveEntries()
        hReco.Draw()
        reconstruct.Update()
        '''
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

        data_tau += 2
    MC_tau += 0.002
    count += 1
    sampleNum += 1 

# Print all the unfolded histos
print "HERE IS WHERE WE ARE GOING TO PRINT THEM ALL........"
canunfold = TCanvas("canunfold","All the unfolded histos",200,10,700,500)
canunfold.Divide(1,1)
colors = [2,3,4,5,6,7,8,9]
legend = TLegend(0.48,0.70,0.78,0.90)
legend.SetFillColor(0)
MC_tau = MC_tau - count 
#data_tau = 2
#print data_unfolded_histos
#print len(data_unfolded_histos)
for i,h in enumerate(data_unfolded_histos):
    print h
    h.SetLineColor(colors[i])
    if i==0:
        h.SetName('Data Unfolded')
        h.SetTitle('"Data" Unfolded ;Boosted top p_T (GeV/c)')
        h.Draw()
        legend.AddEntry(h,'"Data" Unfolded, MC Sample A',"l")
    else:
        h.SetName('Data Unfolded')
        if i == 1:
            SampleName = "B"
        elif i == 2:
            SampleName = "C"
        h.Draw("same")
        legend.AddEntry(h,'"Data" Unfolded, MC Sample '+SampleName,"l")
    legend.Draw()
    #h.SetMinimum(-10)
    h.SetMaximum(2100)
    canunfold.Update()

hdata = data_truth_histos[0]
hdata.SetLineColor(kBlack)
hdata.SetName("Data Unfolded")
hdata.Draw("same")
legend.AddEntry(hdata,'"Data truth',"l")

canunfold.Update()
canunfold.SaveAs("ComparisonUnfoldedData_DiffMC.png")

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

