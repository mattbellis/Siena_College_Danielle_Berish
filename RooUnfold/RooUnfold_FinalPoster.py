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
from ROOT import kRed,kBlack,kBlue,kMagenta,kGreen,TPaveText
from ROOT import RooUnfoldSvd
#from ROOT import RooUnfoldTUnfold
from ROOT import gStyle

gStyle.SetOptStat(11)

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
hMeasLarge= TH1D ("MC A Reco", "Toy Data: Exponential", nbins,lorange,hirange)

# Test with an exponential 
for i in xrange(10000):
    xt = 200 + 5*gRandom.Exp(1.0/0.01266)
    x = smear(xt)
    hTrueLarge.Fill(xt)
    if x!= None:
        hMeasLarge.Fill(x);

# ==============================================================================
#  Example Unfolding
# ==============================================================================
MC_tau = .010
MC_tau_range = 0.015 

data_tau = 0
count = 0

data_truth_histosLarge = []
data_unfolded_histosLarge = []

MC_truth_histos = []
MC_reco_histos = []

sampleNum = 0

colors = [kRed,kMagenta+1,kGreen+1]

text = []

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

    print response

    #unfold0 = RooUnfoldBayes(response,hMC_meas,4);
    unfold0 = RooUnfoldSvd(response,hMC_meas, kreg);  

    # MC true, measured, and unfolded histograms 
    #c1 = TCanvas( 'c1', 'MC', 200, 10, 700, 500 )
    

    hMC_true.SetLineColor(colors[sampleNum]);  
    hMC_true.SetTitle("MC B;Boosted top p_{T} (GeV/c)")
    hMC_true.SetLineWidth(3)
    hMC_true.SetLineStyle(2)
    #hMC_true.Draw();  # MC raw 

    hMC_meas.SetLineColor(colors[sampleNum]);
    hMC_meas.SetLineWidth(3)
    hMC_meas.SetLineStyle(1)
    #hMC_meas.Draw();  # MC measured
    #hMC_meas.Draw("samee")

    hMC_true.SetMaximum(22000)
    #legend = TLegend(0.4,0.7,0.78,0.90)
    #legend.SetFillColor(0)
    #legend.AddEntry(hMC_true,"Truth MC B","l")
    #legend.AddEntry(hMC_meas,"Reco MC B","l")
    #legend.Draw()

    #t = TPaveText(0.0,0.8,0.5,0.99,"NDC")
    #t.AddText("WORK IN PROGRESS")
    #t.SetFillColor(0)
    #text.append(t)
    #t.Draw()

    name = "MC B"
    hMC_true.SetName(name)
    MC_truth_histos.append(hMC_true)
    hMC_meas.SetName(name)
    MC_reco_histos.append(hMC_meas)

    #c1.SaveAs("MC_tau%.3f.png" % float(MC_tau))

    #c1.Update()
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    data_tau = 0.01266 
    data_tau_range = 1 
    while data_tau < data_tau_range:
        print "==================================== TEST ====================================="

        print "==================================== UNFOLD ==================================="
        #unfold= RooUnfoldBayes (response, hMeas, 4);    #  OR
        unfoldLarge = RooUnfoldSvd (response, hMeasLarge,kreg);

        # Data true, measured and unfolded histograms 
        c3 = TCanvas( 'c3', 'MC A Unfolded', 250,250, 700, 500 )

        hTrueLarge.SetLineColor(kBlack);
        hTrueLarge.SetLineWidth(3)
        hTrueLarge.SetTitle('MC A Reconstructed;Boosted top p_{T} (GeV/c)')
        #hTrueLarge.Draw();     # Data truth

        hMeasLarge.SetLineColor(kBlue);
        hMeasLarge.SetTitle('MC A Reconstructed;Boosted top p_{T} (GeV/c)')
        hMeasLarge.SetLineWidth(3)
        hMeasLarge.Draw();     # Data reconstructed

        hMeasLarge.GetXaxis().SetRangeUser(400,1500)
        
        hRecoLarge = unfoldLarge.Hreco();
        unfoldLarge.PrintTable (cout, hTrueLarge);
        #hReco.SetLineColor(kRed);
        hRecoLarge.SetLineWidth(3)

        name = "MC A"
        hRecoLarge.SetName(name)
        data_unfolded_histosLarge.append(hRecoLarge)
        hTrueLarge.SetName(name)
        data_truth_histosLarge.append(hTrueLarge)
            
        t = TPaveText(0.0,0.92,0.2,0.99,"NDC")
        t.AddText("Work In Progress")
        t.SetFillColor(0)
        text.append(t)
        t.Draw()
                    
        gStyle.SetTitleFontSize(0.1)
        c3.SaveAs("DataLarge_MCTau%.3f_dataTau%.5f.png" % (float(MC_tau),float(data_tau)))

        c3.Update()
        
        data_tau += 2
    MC_tau += 0.002
    count += 1
    sampleNum += 1 

#===========================================================================================================
# Print all the unfolded histos
print "HERE IS WHERE WE ARE GOING TO PRINT THEM ALL........"
canunfold = TCanvas("canunfold","All the unfolded histos",200,10,700,500)
canunfold.Divide(1,1)
#colors = [2,3,6,7,8,9]
legend = TLegend(0.50,0.40,0.99,0.85)
legend.SetFillColor(0)
for i,h in enumerate(data_unfolded_histosLarge):
    print h
    h.SetLineColor(colors[i])
    if i==0:
        h.SetName('MC A Unfolded')
        h.SetTitle('MC A Unfolded ;Boosted top p_{T} (GeV/c)')
        h.GetXaxis().SetRangeUser(400,1500)
        h.Draw()
        legend.AddEntry(h,'MC A Unfolded, MC B #lambda = 0.010',"l")
    else:
        h.SetName('MC A Unfolded')
        if i == 1:
            SampleName = "#lambda = 0.012"
        elif i == 2:
            SampleName = "#lambda = 0.014"
        h.GetXaxis().SetRangeUser(400,1500)
        h.Draw("same")
        legend.AddEntry(h,'MC A Unfolded, MC B '+SampleName,"l")
    legend.Draw()
    h.SetMaximum(1400)
    h.GetXaxis().SetRangeUser(400,1500)
    canunfold.Update()

gStyle.SetTitleFontSize(0.1)
hdata = data_truth_histosLarge[0]
hdata.SetLineColor(kBlack)
hdata.SetName("MC A Unfolded")
hdata.Draw("same")
hdata.GetXaxis().SetRangeUser(400,1500)
legend.AddEntry(hdata,'MC A Truth',"l")
legend.Draw()

t = TPaveText(0.0,0.92,0.2,0.99,"NDC")
t.AddText("Work In Progress")
t.SetFillColor(0)
text.append(t)
t.Draw()
canunfold.Update()
canunfold.SaveAs("ComparisonUnfoldedData_DiffMC.png")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cMC = TCanvas("cMC","All the MC",200,10,700,500)
cMC.Divide(1,1)
legend = TLegend(0.65,0.30,0.99,0.85)
gStyle.SetLegendFont(60)
legend.SetFillColor(0)
for i,h in enumerate(MC_truth_histos):
    if i == 0:
        h.SetName('MC B')
        h.Draw()
        legend.AddEntry(h,'Truth, #lambda = 0.010','l')
        MC_reco_histos[0].Draw("same")
        legend.AddEntry(MC_reco_histos[0],'Reco, #lambda = 0.010','l')
    else:
        h.SetName('MC B')
        if i == 1:
            h.Draw("same")
            legend.AddEntry(h,'Truth, #lambda = 0.012','l')
            MC_reco_histos[1].Draw("same")
            legend.AddEntry(MC_reco_histos[1],'Reco, #lambda = 0.012','l')
        elif i == 2:
            h.Draw("same")
            legend.AddEntry(h,'Truth, #lambda = 0.014','l')
            MC_reco_histos[2].Draw("same")
            legend.AddEntry(MC_reco_histos[2],'Reco, #lambda = 0.014','l')
    legend.Draw()
    cMC.Update()
gStyle.SetTitleFontSize(0.1)
t = TPaveText(0.0,0.92,0.2,0.99,"NDC")
t.AddText("Work In Progress")
t.SetFillColor(0)
text.append(t)
t.Draw()
cMC.Update()
cMC.SaveAs("AllMC.png")


#================================================================================
print "======================================Response matrix========================="
print response
c11 = TCanvas('c10','Response matrix',200,10,700,500)
#responseM = response.Mresponse()
responseM = response.Hresponse()
responseM.SetTitle("Response;Boosted top truth p_{T} (GeV/c)")
responseM.GetYaxis().SetTitle("Boosted top reconstructed p_{T} (GeV/c)")
responseM.GetXaxis().SetRangeUser(400,1500)
responseM.Draw('colz')

t = TPaveText(0.0,0.92,0.2,0.99,"NDC")
t.AddText("Work In Progress")
t.SetFillColor(0)
text.append(t)
t.Draw()

response.SaveAs("ResponseMatrix.png")
c11.Update()
################################################################################
if __name__=="__main__":
    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = raw_input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]

