# Running this script:
# python script.py hists1.root hists2.root output.root

import sys, itertools
import Analysis_Funcs as funcs
import config
from ROOT import gSystem, TFile, TH1F, gROOT

# Setting batch to True prevents TCanvas windows from opening
gROOT.SetBatch(True)

# Arguements passed to the script 
# (sys.argv[0] is the script itself)
Runs = {
    'LOOP'  :   {},
    'EVENT'     :   {},
    'BACKGROUND':   {},
    'NORM'      :   {},
} 

FileList = []
for arg in sys.argv:
    # Should filter the python script
    if arg.split('.')[-1] == 'py':
        continue

    # Looks for arguements passing the runs to compare
    elif arg.split('_')[0].upper() == 'LOOP' or arg.split('_')[0].upper() == 'EVENT' or arg.split('_')[0].upper() == 'BACKGROUND':
        level = arg.split('_')[0].upper()
        run = arg.split('_')[1]
        Runs[level][run] = True

    elif arg.split('=')[0].upper() == 'NORM':
        if arg.split('=')[1].upper() == 'TRUE': 
            Runs['Norm'] = True
        else:
            Runs['Norm'] = False


    # Should find the prefixes of hist files to be compared
    else:
        FileList.append(arg)

if len(Runs['LOOP']) == 0:
    Runs['LOOP'] = {
        'Cuts'      :   True,
        'NoCuts'    :   True
    }

if len(Runs['EVENT']) == 0:
    Runs['EVENT'] = {
        'Cuts'      :   True,
        'NoCuts'    :   True
    }

if len(Runs['BACKGROUND']) == 0:
    Runs['BACKGROUND'] = {
        'Cuts'      :   True,
        'NoCuts'    :   True
    }
     

# Finds all unique combinations of files
if len(FileList) == 1:
    FileCombinations = [(FileList[0], FileList[0])]
else:
    FileCombinations = list(itertools.combinations_with_replacement(FileList, 2))


LoopRunList = [x for x, _ in Runs['LOOP'].items()]
if len(LoopRunList) == 1:
    LoopRunCombinations = [(LoopRunList[0], LoopRunList[0])]
else:
    LoopRunCombinations = list(itertools.combinations_with_replacement(LoopRunList, 2))

EventRunList = [x for x, _ in Runs['EVENT'].items()]
if len(EventRunList) == 1:
    EventRunCombinations = [(EventRunList[0], EventRunList[0])]
else:
    EventRunCombinations = list(itertools.combinations_with_replacement(EventRunList, 2))

BackgroundRunList = [x for x, _ in Runs['BACKGROUND'].items()]
if len(BackgroundRunList) == 1:
    BackgroundRunCombinations = [(BackgroundRunList[0], BackgroundRunList[0])]
else:
    BackgroundRunCombinations = list(itertools.combinations_with_replacement(BackgroundRunList, 2))

loopnum = 0

# Setting the CompRuns
if len(Runs['NORM']) == 0:
    CompRuns = ['Norm', 'Rel']
elif Runs['NORM']:
    CompRuns = ['Norm']
else:
    CompRuns = ['Rel']

for Comparison in CompRuns:
    for FilePair in FileCombinations:
        for LoopRunPair in LoopRunCombinations:
            for EventRunPair in EventRunCombinations:
                for BackgroundRunPair in BackgroundRunCombinations:
                
                    loopnum += 1
                    print('Loop:', loopnum)

                    HistFile1_Prefix = FilePair[0]
                    HistFile1_LoopRun = LoopRunPair[0]
                    HistFile1_EventRun = EventRunPair[0]
                    HistFile1_BackgroundRun = BackgroundRunPair[0]
                    HistFile1_Name = HistFile1_Prefix+'_'+'Loop'+HistFile1_LoopRun+'Event'+HistFile1_EventRun+'Background'+HistFile1_BackgroundRun

                    HistFile2_Prefix = FilePair[1]
                    HistFile2_LoopRun = LoopRunPair[1]
                    HistFile2_EventRun = EventRunPair[1]
                    HistFile2_BackgroundRun = BackgroundRunPair[1]
                    HistFile2_Name = HistFile2_Prefix+'_'+'Loop'+HistFile2_LoopRun+'Event'+HistFile2_EventRun+'Background'+HistFile2_BackgroundRun
                    
                    gSystem.Exec('mkdir '+Comparison+'_'+HistFile1_Prefix+'-'+HistFile2_Prefix)
                    gSystem.Exec('mkdir '+Comparison+'_'+HistFile1_Prefix+'-'+HistFile2_Prefix+'/Loop'+HistFile1_LoopRun+'-'+HistFile2_LoopRun)
                    gSystem.Exec('mkdir '+Comparison+'_'+HistFile1_Prefix+'-'+HistFile2_Prefix+'/Loop'+HistFile1_LoopRun+'-'+HistFile2_LoopRun+'/Event'+HistFile1_EventRun+'-'+HistFile2_EventRun+'/')
                    gSystem.Exec('mkdir '+Comparison+'_'+HistFile1_Prefix+'-'+HistFile2_Prefix+'/Loop'+HistFile1_LoopRun+'-'+HistFile2_LoopRun+'/Event'+HistFile1_EventRun+'-'+HistFile2_EventRun+'/Background'+HistFile1_BackgroundRun+'-'+HistFile2_BackgroundRun+'/')


                    # Read hist files
                    HistFiles = {
                        1               :   {
                            'Prefix'        :   HistFile1_Prefix,
                            'LoopRun'       :   HistFile1_LoopRun,
                            'EventRun'      :   HistFile1_EventRun,
                            'BackgroundRun' :   HistFile1_BackgroundRun,
                            'Name'          :   HistFile1_Name,

                            'File'          :   TFile(HistFile1_Name+'.root')
                        },

                        2   :   {
                            'Prefix'        :   HistFile2_Prefix,
                            'LoopRun'       :   HistFile2_LoopRun,
                            'EventRun'      :   HistFile2_EventRun,
                            'BackgroundRun' :   HistFile2_BackgroundRun,
                            'Name'          :   HistFile2_Name,

                            'File'          :   TFile(HistFile2_Name+'.root')
                        },
                    }    

                    HistDict = config.HistDict
                    HistCompDict = config.HistComparisonDict

                    # if False:
                    if HistFile1_Name != HistFile2_Name:
                        for name, properties in HistDict.items():

                            for var in properties['Requests']['Vars']:

                                # If the hist is 2D
                                # 2D hists break the code for some reason
                                if type(var) == tuple and len(var) == 2:
                                    continue
                                else:
                                    HistVar = var
                                    HistName = name

                                # Read the hist in each file
                                Hist1 = HistFiles[1]['File'].Get(HistName+'_'+HistVar+';1')
                                Hist2 = HistFiles[2]['File'].Get(HistName+'_'+HistVar+';1')  
                                                            
                                HistProps = {
                                    'Hist1'     :   {
                                        'Hist'      :   Hist1,
                                        'HistName'  :   HistName,
                                        'HistVar'   :   HistVar,
                                        'FileDict'  :   HistFiles[1]
                                    },

                                    'Hist2'     :   {
                                        'Hist'      :   Hist2,
                                        'HistName'  :   HistName,
                                        'HistVar'   :   HistVar,
                                        'FileDict'  :   HistFiles[2]

                                    },
                                    
                                    'Comparison'      :   Comparison
                                }

                                funcs.CompareHist(HistProps)

                    for key, properties in HistCompDict.items():

                        for var in properties['Var']:
                            # If the hist is 2D
                            if type(var) == tuple and len(var) == 2:
                                HistVar = var[0]+'_'+var[1]
                            else:
                                HistVar = var
                            
                            Hist1Name = properties['Hist1']['Name']
                            Hist2Name = properties['Hist2']['Name']


                            # Read the hist in each file
                            Hist1 = HistFiles[1]['File'].Get(Hist1Name+'_'+HistVar+';1')
                            Hist2 = HistFiles[2]['File'].Get(Hist2Name+'_'+HistVar+';1')  

                            HistProps = {
                                'Hist1'     :   {
                                    'Hist'      :   Hist1,
                                    'HistName'  :   Hist1Name,
                                    'HistVar'   :   HistVar,
                                    'FileDict'  :   HistFiles[1]
                                },

                                'Hist2'     :   {
                                    'Hist'      :   Hist2,
                                    'HistName'  :   Hist2Name,
                                    'HistVar'   :   HistVar,
                                    'FileDict'  :   HistFiles[2]
                                },
                                    
                                'Comparison'      :   Comparison 
                            }

                            funcs.CompareHist(HistProps)

