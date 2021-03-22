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
    'Event'     :   {},
    'Particle'  :   {},
    'RelScale'  :   {}
} 

FileList = []
for arg in sys.argv:
    # Should filter the python script
    if arg.split('.')[-1] == 'py':
        continue

    # Looks for arguements passing the runs to compare
    elif arg.split('_')[0] == 'Event' or arg.split('_')[0] == 'Particle':
        level = arg.split('_')[0]
        run = arg.split('_')[1]
        Runs[level][run] = True

    elif arg.split('=')[0] == 'Rel' or arg.split('=')[0] == 'Norm':
        ScaleType = arg.split('=')[0]
        Switch = arg.split('=')[1]
        Runs['RelScale'][ScaleType] = Switch

    # Should find the prefixes of hist files to be compared
    else:
        FileList.append(arg)

if len(Runs['Event']) == 0:
    Runs['Event'] = {
        'Cuts'      :   True,
        'NoCuts'    :   True
    }

if len(Runs['Particle']) == 0:
    Runs['Particle'] = {
        'Cuts'      :   True,
        'NoCuts'    :   True
    }

if len(Runs['RelScale']) == 0:
    Runs['RelScale'] = {
        'Rel'       :   True,
        'Norm'      :   True
    }
     

# Finds all unique combinations of files
if len(FileList) == 1:
    FileCombinations = [(FileList[0], FileList[0])]
else:
    FileCombinations = list(itertools.combinations_with_replacement(FileList, 2))

EventRunList = [x for x, _ in Runs['Event'].items()]


ParticleRunList = [x for x, _ in Runs['Particle'].items()]

if len(EventRunList) == 1:
    EventRunCombinations = [(EventRunList[0], EventRunList[0])]
else:
    EventRunCombinations = list(itertools.combinations_with_replacement(EventRunList, 2))



if len(ParticleRunList) == 1:
    ParticleRunCombinations = [(ParticleRunList[0], ParticleRunList[0])]
else:
    ParticleRunCombinations = list(itertools.combinations_with_replacement(ParticleRunList, 2))

loopnum = 0

for RelScale, _ in Runs['RelScale'].items():
    for FilePair in FileCombinations:
        for EventRunPair in EventRunCombinations:
            for ParticleRunPair in ParticleRunCombinations:
                
                loopnum += 1
                print('Loop:', loopnum)

                HistFile1_Prefix = FilePair[0]
                HistFile1_EventRun = EventRunPair[0]
                HistFile1_ParticleRun = ParticleRunPair[0]
                HistFile1_Name = HistFile1_Prefix+'_'+'Event'+HistFile1_EventRun+'Particle'+HistFile1_ParticleRun

                HistFile2_Prefix = FilePair[1]
                HistFile2_EventRun = EventRunPair[1]
                HistFile2_ParticleRun = ParticleRunPair[1]
                HistFile2_Name = HistFile2_Prefix+'_'+'Event'+HistFile2_EventRun+'Particle'+HistFile2_ParticleRun
                
                gSystem.Exec('mkdir '+RelScale+'_'+HistFile1_Prefix+'-'+HistFile2_Prefix)
                gSystem.Exec('mkdir '+RelScale+'_'+HistFile1_Prefix+'-'+HistFile2_Prefix+'/Event'+HistFile1_EventRun+'-'+HistFile2_EventRun)
                gSystem.Exec('mkdir '+RelScale+'_'+HistFile1_Prefix+'-'+HistFile2_Prefix+'/Event'+HistFile1_EventRun+'-'+HistFile2_EventRun+'/Particle'+HistFile1_ParticleRun+'-'+HistFile2_ParticleRun+'/')

                # Read hist files
                HistFiles = {
                    1               :   {
                        'Prefix'        :   HistFile1_Prefix,
                        'EventRun'      :   HistFile1_EventRun,
                        'ParticleRun'   :   HistFile1_ParticleRun,
                        'Name'          :   HistFile1_Name,

                        'File'          :   TFile(HistFile1_Name+'.root')
                    },

                    2   :   {
                        'Prefix'        :   HistFile2_Prefix,
                        'EventRun'      :   HistFile2_EventRun,
                        'ParticleRun'   :   HistFile2_ParticleRun,
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
                                
                                'RelScale'      :   RelScale
                            }

                            funcs.CompareHist(HistProps)

                if HistFile1_Name == HistFile2_Name:
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
                                    
                                'RelScale'      :   RelScale 
                            }

                            funcs.CompareHist(HistProps)``

