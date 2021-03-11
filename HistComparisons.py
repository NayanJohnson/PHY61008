# Running this script:
# python script.py hists1.root hists2.root output.root

import sys

HistFile1_name = sys.argv[1]
HistFile2_name = sys.argv[2]
outfile_name = sys.argv[3]

from ROOT import TFile, TH1F, TCanvas, TLegend, SetOwnership

# Open output
outfile = TFile(outfile_name,"RECREATE")

# Read hist files
HistFile1 = TFile(HistFile1_name)
HistFile2 = TFile(HistFile2_name)

# Hist1.GetListOfKeys() returns an object of type THashList
# key is of type TKey
for key in HistFile1.GetListOfKeys():

    # Clear canvas
    HistCan = TCanvas()
    HistCan.cd()
    
    # Get the name of the hist
    histname = key.GetName()

    # Read the same hist in each file
    Hist1 = HistFile1.Get(histname+';1')
    Hist2 = HistFile2.Get(histname+';1')    

    # Get the index of the min/max bin and the read off the value of the 
    # low edge
    BinMax1 = Hist1.GetBinLowEdge(Hist1.FindLastBinAbove())
    BinMin1 = Hist1.GetBinLowEdge(Hist1.FindFirstBinAbove())
    BinMax2 = Hist2.GetBinLowEdge(Hist2.FindLastBinAbove())
    BinMin2 = Hist2.GetBinLowEdge(Hist2.FindFirstBinAbove())    
    # Max/min = BinMax/min +- 5% +- 5 (prevents max=min for BinMax/Min=0)
    XMax1 = BinMax1 + abs(BinMax1/20) + 5
    XMin1 = BinMin1 - abs(BinMin1/20) - 5
    XMax2 = BinMax2 + abs(BinMax2/20) + 5
    XMin2 = BinMin2 - abs(BinMin2/20) - 5    

    # max frequency
    Max1 = Hist1.GetMaximum() + Hist1.GetMaximum()/10
    Max2 = Hist2.GetMaximum() + Hist2.GetMaximum()/10

    # Max/min is the max/min of the two hists
    XMax = max(XMax1, XMax2)
    XMin = min(XMin1, XMin2)
    Max = max(Max1, Max2)
    # Take the large Nbin value
    NBins = max(Hist1.GetNbinsX(), Hist2.GetNbinsX())

    # Setting universal hist options
    for hist in (Hist1, Hist2):
        hist.SetBins(NBins, XMin, XMax)
        hist.SetMaximum(Max)
        hist.SetStats(False)

    # Set diffent hist options
    Hist1.SetLineColor(4)
    Hist2.SetLineColor(2)
    # Force both to be drawn as hist and on the same canvas
    Hist1.Draw("hist same")
    Hist2.Draw("hist same")

    # Legend properties
    LegendX1 = .8
    LegendX_interval = 0.15
    LegendY1 = .95
    LegendY_interval = 0.1

    Legend1 = TLegend(LegendX1, LegendY1 , LegendX1+LegendX_interval, LegendY1-LegendY_interval)
    # Stops legend overwriting canvas
    SetOwnership(Legend1,False)
    Legend1.SetBorderSize(1)
    Legend1.SetShadowColor(2)
    Legend1.SetHeader("Cuts")
    # Entries
    Legend1.AddEntry("entries","Entries: "+str(int(Hist1.GetEntries())))
    Legend1.AddEntry(Hist1, "Line Color", "l")
    Legend1.SetTextSize(0.025)
    Legend1.SetTextColor(1)
    # Seperation is small, but will be maximised to the bounds of the TLegend
    # box
    Legend1.SetEntrySeparation(.1)
    Legend1.Draw("same")

    Legend2 = TLegend(LegendX1, LegendY1-LegendY_interval , LegendX1+LegendX_interval, LegendY1-2*LegendY_interval)
    # Stops legend overwriting canvas    
    SetOwnership(Legend2,False)
    Legend2.SetBorderSize(1)
    Legend2.SetShadowColor(2)
    Legend2.SetHeader("No Cuts")
    # Entries
    Legend2.AddEntry("entries","Entries: "+str(int(Hist2.GetEntries())))
    Legend2.AddEntry(Hist2, "Line Color", "l")
    Legend2.SetTextSize(0.025)
    Legend2.SetTextColor(1)
    # Seperation is small, but will be maximised to the bounds of the TLegend
    # box    
    Legend2.SetEntrySeparation(.1)
    Legend2.Draw("same")

    # Update canvas
    HistCan.Update()
    # Write canvas to outfile, needs the name for some reason.
    outfile.WriteObject(HistCan, histname)

# Closing file
outfile.Close()