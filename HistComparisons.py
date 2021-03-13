# Running this script:
# python script.py hists1.root hists2.root output.root

import sys
import Analysis_Funcs as funcs
import config
from ROOT import TFile, TH1F

HistFile1_name = sys.argv[1]
HistFile2_name = sys.argv[2]
MediaDir_name = sys.argv[3]

if MediaDir_name[-1] != '/':
    MediaDir_name = MediaDir_name+'/'

# Read hist files
HistFile1 = TFile(HistFile1_name)
HistFile2 = TFile(HistFile2_name)

HistDict = config.HistDict

# Hist1.GetListOfKeys() returns an object of type THashList
# key is of type TKey
for name, properties in HistDict.items():

    for var in properties['Requests']['Vars']:
        # If the hist is 2D
        if type(var) == tuple and len(var) == 2:
            histvar = var[0]+'_'+var[1]
            histname = name+'_'+histvar
        else:
            histvar = var
            histname = name+'_'+histvar

        # Read the same hist in each file
        Hist1 = HistFile1.Get(histname+';1')
        Hist2 = HistFile2.Get(histname+';1')  
        print(histname)  
        Hist2.ls()  
        
        funcs.CompareHist(Hist1, Hist2, HistDict, histname, histname, MediaDir_name)

