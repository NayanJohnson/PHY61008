# Running this script:
# python script.py hists1.root hists2.root output.root

import sys
import Analysis_Funcs as funcs
import config
from ROOT import TFile, TH1F, TCanvas, TLegend, SetOwnership

HistFile1_name = sys.argv[1]
HistFile2_name = sys.argv[2]
MediaDir_name = sys.argv[3]

if MediaDir_name[-1] != '/':
    MediaDir_name = MediaDir_name+'/'

# Read hist files
HistFile1 = TFile(HistFile1_name)
HistFile2 = TFile(HistFile2_name)

HistDict1 = config.HistDict
HistDict2 = config.HistDict
# Hist1.GetListOfKeys() returns an object of type THashList
# key is of type TKey
for key in HistFile1.GetListOfKeys():

    # Clear canvas
    HistCan = TCanvas()
    HistCan.cd()
    
    # Get the name of the hist
    histname = key.GetName()
    histvar = histname.split('_')[-1]
    category = histname.split('_')[0:-1]
    category = "_".join(category)

    # Read the same hist in each file
    Hist1 = HistFile1.Get(histname+';1')
    Hist2 = HistFile2.Get(histname+';1')    

    if Hist1.GetDimension() == 1:
        
        for key, properties in HistDict1.items():
            properties['Hists'] = {}
        HistDict1[category]['Hists'][histvar] = Hist1
        for key, properties in HistDict2.items():
            properties['Hists'] = {}
        HistDict2[category]['Hists'][histvar] = Hist2


        funcs.HistLims(HistDict1, 1)
        funcs.HistLims(HistDict2, 2)

        # Setting universal hist options
        for hist in (Hist1, Hist2):
            # SetBins actually introduces an offset into the graph
            hist.SetStats(False)

        # Set diffent hist options
        Hist1.SetLineColor(4)
        Hist2.SetLineColor(2)
        # Force both to be drawn as hist and on the same canvas
        Hist1.Draw("HIST same")
        Hist2.Draw("HIST same")

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
        
        HistCan.SaveAs(MediaDir_name+histname+'.png')
