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

hTrueLarge= TH1D ("trueLarge", "Toy Data: Exponential", nbins,lorange,hirange)
hMeasLarge= TH1D ("measLarge", "Toy Data: Exponential", nbins,lorange,hirange)

# Test with an exponential 
for i in xrange(10000):
    xt = 200 + 5*gRandom.Exp(1.0/0.01266)
    x = smear(xt)
    hTrueLarge.Fill(xt)
    if x!= None:
        hMeasLarge.Fill(x);

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
hTrueSmall= TH1D ("trueSmall", "Toy Data: Exponential", nbins,lorange,hirange)
hMeasSmall= TH1D ("measSmall", "Toy Data: Exponential", nbins,lorange,hirange)

# Test with an exponential 
for i in xrange(2000):
    xt = 200 + 5*gRandom.Exp(1.0/0.01266)
    x = smear(xt)
    hTrueSmall.Fill(xt)
    if x!= None:
        hMeasSmall.Fill(x);

# ==============================================================================
#  Example Unfolding
# ==============================================================================
MC_tau = .010
MC_tau_range = 0.015 

data_tau = 0
count = 0

data_truth_histosLarge = []
data_unfolded_histosLarge = []

data_truth_histosSmall = []
data_unfolded_histosSmall = []

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
    hMC_true.SetLineStyle(2)
    hMC_true.Draw();  # MC raw 

    hMC_meas.SetLineColor(kBlue);
    hMC_meas.SetLineWidth(3)
    hMC_meas.SetLineStyle(2)
    hMC_meas.Draw("SAME");  # MC measured
    
    hMC_true.SetMaximum(22000)
    legend = TLegend(0.4,0.7,0.78,0.90)
    legend.SetFillColor(0)
    legend.AddEntry(hMC_true,"Truth MC","l")
    legend.AddEntry(hMC_meas,"Reconstructed MC","l")
    legend.Draw()
    c1.SaveAs("MC_tau%.3f.png" % float(MC_tau))

    c1.Update()
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    data_tau = 0.01266 
    data_tau_range = 1 
    while data_tau < data_tau_range:
        print "==================================== TEST ====================================="

        print "==================================== UNFOLD ==================================="
        #unfold= RooUnfoldBayes (response, hMeas, 4);    #  OR
        unfoldSmall = RooUnfoldSvd (response, hMeasSmall, kreg);   #  OR
        unfoldLarge = RooUnfoldSvd (response, hMeasLarge,kreg);
        #unfold= RooUnfoldTUnfold (response, hMeas);

        # Data true, measured and unfolded histograms 
        c3 = TCanvas( 'c3', 'Data Unfolded', 250,250, 700, 500 )

        hTrueLarge.SetLineColor(kBlack);
        hTrueLarge.SetLineWidth(3)
        hTrueLarge.SetTitle('"Data";Boosted top p_T (GeV/c)')
        hTrueLarge.Draw();     # Data truth
        #c3.SaveAs("Data_true.png")

        hMeasLarge.SetLineColor(kBlue);
        hMeasLarge.SetLineWidth(3)
        hMeasLarge.Draw("SAME");     # Data reconstructed
        #c3.SaveAs("Data_meas.png")
        
        hRecoLarge = unfoldLarge.Hreco();
        unfoldLarge.PrintTable (cout, hTrueLarge);
        #hReco.SetLineColor(kRed);
        hRecoLarge.SetLineWidth(3)

        #if data_tau == 2:
        if 1:
            name = "Data"
            hRecoLarge.SetName(name)
            data_unfolded_histosLarge.append(hRecoLarge)
            hTrueLarge.SetName(name)
            data_truth_histosLarge.append(hTrueLarge)

        #hReco.SetTitle("Data Truth, Reconstructed, and Unfolded")
        #hReco.Draw("SAME");           # Data unfolded 

        legend = TLegend(0.4,0.7,0.78,0.90)
        legend.SetFillColor(0)
        legend.AddEntry(hTrueLarge,'"Data" Truth',"l")
        legend.AddEntry(hMeasLarge,'"Data" Reconstructed',"l")
        #legend.AddEntry(hReco,"Data Unfolded","l")
        legend.Draw()
         
        c3.SaveAs("DataLarge_MCTau%.3f_dataTau%.5f.png" % (float(MC_tau),float(data_tau)))

        c3.Update()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        c4 = TCanvas( 'c4', 'Data Unfolded Small', 250,250, 700, 500 )

        hTrueSmall.SetLineColor(kBlack);
        hTrueSmall.SetLineWidth(3)
        hTrueSmall.SetTitle('"Data";Boosted top p_T (GeV/c)')
        hTrueSmall.Draw();     # Data truth

        hMeasSmall.SetLineColor(kBlue);
        hMeasSmall.SetLineWidth(3)
        hMeasSmall.Draw("SAME");     # Data reconstructed
        #c4.SaveAs("Data_meas.png")
        
        hRecoSmall = unfoldSmall.Hreco();
        unfoldSmall.PrintTable (cout, hTrueSmall);
        #hReco.SetLineColor(kRed);
        hRecoSmall.SetLineWidth(3)

        #if data_tau == 2:
        if 1:
            name = "Data"
            hRecoSmall.SetName(name)
            data_unfolded_histosSmall.append(hRecoSmall)
            hTrueSmall.SetName(name)
            data_truth_histosSmall.append(hTrueSmall)

        #hReco.SetTitle("Data Truth, Reconstructed, and Unfolded")
        #hReco.Draw("SAME");           # Data unfolded 

        legend = TLegend(0.4,0.7,0.78,0.90)
        legend.SetFillColor(0)
        legend.AddEntry(hTrueSmall,'"Data" Truth',"l")
        legend.AddEntry(hMeasSmall,'"Data" Reconstructed',"l")
        #legend.AddEntry(hReco,"Data Unfolded","l")
        legend.Draw()
         
        c4.SaveAs("DataSmall_MCTau%.3f_dataTau%.5f.png" % (float(MC_tau),float(data_tau)))

        c4.Update()
        data_tau += 2
    MC_tau += 0.002
    count += 1
    sampleNum += 1 

#===========================================================================================================
# Print all the unfolded histos
print "HERE IS WHERE WE ARE GOING TO PRINT THEM ALL........"
canunfold = TCanvas("canunfold","All the unfolded histos",200,10,700,500)
canunfold.Divide(1,1)
colors = [2,3,6,7,8,9]
legend = TLegend(0.48,0.70,0.78,0.90)
legend.SetFillColor(0)
MC_tau = MC_tau - count 
for i,h in enumerate(data_unfolded_histosLarge):
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
    #h.SetAxisRange(1000,1500)
    canunfold.Update()

hdata = data_truth_histosLarge[0]
hdata.SetLineColor(kBlack)
hdata.SetName("Data Unfolded")
hdata.Draw("same")
legend.AddEntry(hdata,'"Data truth',"l")

canunfold.Update()
canunfold.SaveAs("ComparisonUnfoldedData_DiffMC.png")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Print all the unfolded histos
print "HERE IS WHERE WE ARE GOING TO PRINT THEM ALL........"
canunfoldSmall = TCanvas("canunfoldSmall","All the unfolded histos",200,10,700,500)
canunfoldSmall.Divide(1,1)
colors = [2,3,6,7,8,9]
legend = TLegend(0.48,0.70,0.78,0.90)
legend.SetFillColor(0)
for i,h in enumerate(data_unfolded_histosSmall):
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
    h.SetMaximum(700)
    #h.SetAxisRange(200,1500)
    canunfoldSmall.Update()

hdataSmall = data_truth_histosSmall[0]
hdataSmall.SetLineColor(kBlack)
hdataSmall.SetName("Data Unfolded")
hdataSmall.Draw("same")
legend.AddEntry(hdataSmall,'"Data truth',"l")

canunfoldSmall.Update()
canunfoldSmall.SaveAs("ComparisonUnfoldedData_DiffMCSmall.png")
#================================================================================
print "======================================Response matrix========================="
print response
c11 = TCanvas('c10','Response matrix',200,10,700,500)
responseM = response.Mresponse()
responseM.Draw()
response.SaveAs("ResponseMatrix.png")
################################################################################
if __name__=="__main__":
    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = raw_input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]

