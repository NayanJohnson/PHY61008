# Running this script:
# python script.py hists1.root hists2.root output.root

import sys, itertools
import config, requests, itertools
import Particle_Funcs as ParticleFuncs
import Hist_Funcs as HistFuncs
import Loop_Funcs as LoopFuncs
from ROOT import gSystem, TFile, TH1F, gROOT

# Setting batch to True prevents TCanvas windows from opening
gROOT.SetBatch(True)

# Arguements passed to the script 
# (sys.argv[0] is the script itself)
LevelRuns = []
LoopRuns = []
EventRuns = []
AnalysisRuns = [] 

CompRuns = []

FileList = []
for arg in sys.argv:
    # Should filter the python script
    if arg.split('.')[-1] == 'py':
        continue

    # Looks for arguements passing the runs to compare
    elif arg.split('_')[0].upper() == 'LEVEL':
        LevelRuns.append(arg.split('_')[1])

    elif arg.split('_')[0].upper() == 'LOOP':
        LoopRuns.append(arg.split('_')[1])

    elif arg.split('_')[0].upper() == 'EVENT':
        EventRuns.append(arg.split('_')[1])

    elif arg.split('_')[0].upper() == 'ANALYSIS':
        AnalysisRuns.append(arg.split('_')[1])

    elif arg.split('=')[0].upper() == 'NORM':
        CompRuns.append(arg.split('_')[1])

    # Should find the prefixes of hist files to be compared
    else:
        FileList.append(arg)


# If no run is given for a level, set the runs to default
if len(LevelRuns) == 0:
    LevelRuns = ['Generator', 'Detector']

if len(LoopRuns) == 0:
    LoopRuns = ['Cuts', 'NoCuts']

if len(EventRuns) == 0:
    EventRuns = ['Cuts', 'NoCuts']

if len(AnalysisRuns) == 0:
    AnalysisRuns = ['Cuts', 'NoCuts']

if len(CompRuns) == 0:
    CompRuns = [True, False]    

# Finds all unique combinations of files
if len(FileList) == 1:
    FileCombinations = [(FileList[0], FileList[0])]
else:
    FileCombinations = list(itertools.combinations_with_replacement(FileList, 2))


if len(LevelRuns) == 1:
    LevelRunCombinations = [(LevelRuns[0], LevelRuns[0])]
else:
    LevelRunCombinations = list(itertools.combinations_with_replacement(LevelRuns, 2))

if len(LoopRuns) == 1:
    LoopRunCombinations = [(LoopRuns[0], LoopRuns[0])]
else:
    LoopRunCombinations = list(itertools.combinations_with_replacement(LoopRuns, 2))

if len(EventRuns) == 1:
    EventRunCombinations = [(EventRuns[0], EventRuns[0])]
else:
    EventRunCombinations = list(itertools.combinations_with_replacement(EventRuns, 2))

if len(AnalysisRuns) == 1:
    AnalysisRunCombinations = [(AnalysisRuns[0], AnalysisRuns[0])]
else:
    AnalysisRunCombinations = list(itertools.combinations_with_replacement(AnalysisRuns, 2))

loopnum = 0


for FilePair in FileCombinations:
    for LevelRunPair in LevelRunCombinations:
        for LoopRunPair in LoopRunCombinations:
            for EventRunPair in EventRunCombinations:
                for AnalysisRunPair in AnalysisRunCombinations:
                    for Norm in CompRuns:

                        loopnum += 1
                        print('Loop:', loopnum)

                        HistFile1_Prefix = FilePair[0]
                        HistFile1_LevelRun = LevelRunPair[0]
                        HistFile1_LoopRun = LoopRunPair[0]
                        HistFile1_EventRun = EventRunPair[0]
                        HistFile1_AnalysisRun = AnalysisRunPair[0]
                        HistFile1_Name = HistFile1_Prefix+'_'+HistFile1_LevelRun+'Level_Loop'+HistFile1_LoopRun+'Event'+HistFile1_EventRun+'Analysis'+HistFile1_AnalysisRun

                        HistFile2_Prefix = FilePair[1]
                        HistFile2_LevelRun = LevelRunPair[1]
                        HistFile2_LoopRun = LoopRunPair[1]
                        HistFile2_EventRun = EventRunPair[1]
                        HistFile2_AnalysisRun = AnalysisRunPair[1]
                        HistFile2_Name = HistFile2_Prefix+'_'+HistFile2_LevelRun+'Level_Loop'+HistFile2_LoopRun+'Event'+HistFile2_EventRun+'Analysis'+HistFile2_AnalysisRun
                        
                        if Norm:
                            Comparison = 'Norm'
                        else:
                            Comparison = 'Rel'

                        gSystem.Exec('mkdir '+Comparison+'_'+HistFile1_Prefix+'-'+HistFile2_Prefix)
                        gSystem.Exec('mkdir '+Comparison+'_'+HistFile1_Prefix+'-'+HistFile2_Prefix+'/'+HistFile1_LevelRun+'-'+HistFile2_LevelRun+'Level/')
                        gSystem.Exec('mkdir '+Comparison+'_'+HistFile1_Prefix+'-'+HistFile2_Prefix+'/'+HistFile1_LevelRun+'-'+HistFile2_LevelRun+'Level/Loop'+HistFile1_LoopRun+'-'+HistFile2_LoopRun)
                        gSystem.Exec('mkdir '+Comparison+'_'+HistFile1_Prefix+'-'+HistFile2_Prefix+'/'+HistFile1_LevelRun+'-'+HistFile2_LevelRun+'Level/Loop'+HistFile1_LoopRun+'-'+HistFile2_LoopRun+'/Event'+HistFile1_EventRun+'-'+HistFile2_EventRun+'/')
                        gSystem.Exec('mkdir '+Comparison+'_'+HistFile1_Prefix+'-'+HistFile2_Prefix+'/'+HistFile1_LevelRun+'-'+HistFile2_LevelRun+'Level/Loop'+HistFile1_LoopRun+'-'+HistFile2_LoopRun+'/Event'+HistFile1_EventRun+'-'+HistFile2_EventRun+'/Analysis'+HistFile1_AnalysisRun+'-'+HistFile2_AnalysisRun+'/')


                        # Read hist files
                        HistFiles = {
                            1               :   {
                                'Prefix'        :   HistFile1_Prefix,
                                'LevelRun'      :   HistFile1_LevelRun,
                                'LoopRun'       :   HistFile1_LoopRun,
                                'EventRun'      :   HistFile1_EventRun,
                                'AnalysisRun'   :   HistFile1_AnalysisRun,
                                'Name'          :   HistFile1_Name,

                                'File'          :   TFile(HistFile1_Name+'.root')
                            },

                            2   :   {
                                'Prefix'        :   HistFile2_Prefix,
                                'LevelRun'      :   HistFile2_LevelRun,
                                'LoopRun'       :   HistFile2_LoopRun,
                                'EventRun'      :   HistFile2_EventRun,
                                'AnalysisRun' :   HistFile2_AnalysisRun,
                                'Name'          :   HistFile2_Name,

                                'File'          :   TFile(HistFile2_Name+'.root')
                            },
                        }    

                        HistDict = requests.HistDict
                        HistCompDict = requests.HistComparisonDict

                        # if False:
                        if HistFile1_Name != HistFile2_Name:
                            for name, properties in HistDict.items():

                                for var in properties['Requests']['Vars']:

                                    # If the hist is 2D
                                    # 2D hists break the code for some reason
                                    if type(var) == list and len(var) == 2:
                                        continue
                                    else:
                                        HistVar = var
                                        HistName = name

                                    # print(HistName, HistVar)
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
                                        
                                        'Norm'      :   Norm
                                    }

                                    HistFuncs.CompareHist(HistProps)

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
                                        
                                    'Norm'      :   Norm 
                                }

                                HistFuncs.CompareHist(HistProps)

