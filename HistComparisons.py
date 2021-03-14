# Running this script:
# python script.py hists1.root hists2.root output.root

import sys
import Analysis_Funcs as funcs
import config
from ROOT import TFile, TH1F

# Arguements passed to the script 
# (sys.argv[0] is the script itself)
HistFile1_name = sys.argv[1]
HistFile2_name = sys.argv[2]


# Read hist files
HistFiles = {
    1   :   {
        'File'  :   TFile(HistFile1_name),
        'Name'  :   HistFile1_name
    },

    2   :   {
        'File'  :   TFile(HistFile2_name),
        'Name'  :   HistFile2_name
    }
}    

HistDict = config.HistDict
HistCompDict = config.HistComparisonDict

for name, properties in HistDict.items():

    for var in properties['Requests']['Vars']:
        # If the hist is 2D
        if type(var) == tuple and len(var) == 2:
            HistVar = var[0]+'_'+var[1]
            HistName = name
        else:
            HistVar = var
            HistName = name

        Hist1Name = HistName
        Hist2Name = HistName

        # Read the hist in each file
        Hist1 = HistFiles[1]['File'].Get(Hist1Name+'_'+HistVar+';1')
        Hist2 = HistFiles[2]['File'].Get(Hist1Name+'_'+HistVar+';1')  
        
        HistProps = {
            'Hist1'     :   {
                'Hist'      :   Hist1,
                'HistName'  :   Hist1Name,
                'HistVar'   :   HistVar,
                'HistFileName'  
                # Take the name without the .root
                            :   HistFiles[1]['Name'].split('.')[0] 
            },

            'Hist2'     :   {
                'Hist'      :   Hist2,
                'HistName'  :   Hist2Name,
                'HistVar'   :   HistVar,
                'HistFileName'  
                # Take the name without the .root
                            :   HistFiles[2]['Name'].split('.')[0] 
            }
        }

        funcs.CompareHist(HistProps, HistDict)

for key, properties in HistCompDict.items():

    for var in properties['Var']:
        # If the hist is 2D
        if type(var) == tuple and len(var) == 2:
            HistVar = var[0]+'_'+var[1]
        else:
            HistVar = var
        
        Hist1Name = properties['Hist1']['Name']
        Hist2Name = properties['Hist2']['Name']

        Hist1FileIndex = properties['Hist1']['File']
        Hist2FileIndex = properties['Hist2']['File']

        # Read the hist in each file
        Hist1 = HistFiles[Hist1FileIndex]['File'].Get(Hist1Name+'_'+HistVar+';1')
        Hist2 = HistFiles[Hist2FileIndex]['File'].Get(Hist2Name+'_'+HistVar+';1')  
        
        HistProps = {
            'Hist1'     :   {
                'Hist'      :   Hist1,
                'HistName'  :   Hist1Name,
                'HistVar'   :   HistVar,
                'HistFileName'  
                            :   HistFiles[Hist1FileIndex]['Name'].split('.')[0]    
            },

            'Hist2'     :   {
                'Hist'      :   Hist2,
                'HistName'  :   Hist2Name,
                'HistVar'   :   HistVar,
                'HistFileName'  
                            :   HistFiles[Hist2FileIndex]['Name'].split('.')[0]    
            }
        }

        funcs.CompareHist(HistProps, HistDict)

