import sys
import config, requests
import Particle_Funcs as ParticleFuncs
import Hist_Funcs as HistFuncs
import Loop_Funcs as LoopFuncs
from ROOT import gSystem, TFile, TH1F, gROOT

# Setting batch to True prevents TCanvas windows from opening
gROOT.SetBatch(True)

# Arguements passed to the script 
# (sys.argv[0] is the script itself)
LevelComparisons = []
LoopComparisons = []
EventComparisons = []
AnalysisComparisons = [] 

NormRuns = []

MediaDir = ''

RootDir = ('', '')
FileComparisons = []

# Parsing the arguments
"""
Arguments 


"""

for arg in sys.argv:
    # Should filter the python script
    if arg.split('.')[-1] == 'py':
        continue

    # Directory to store graphs
    # "MEDIADIRS=DIR"
    elif arg.split('=')[0].upper() == 'MEDIADIRS':
        RootDir = arg.split('=')[1]

    # File args
    # "ARG=FILE1ARG-FILE2ARG"
    elif arg.split('=')[0].upper() == 'ROOTDIRS':
        RootDir = (arg.split('=')[1].split('-')[0], arg.split('=')[1].split('-')[1])
     
    elif arg.split('=')[0].upper() == 'PREFIX':
        FileComparisons.append( (arg.split('=')[1].split('-')[0], arg.split('=')[1].split('-')[1]) )

    # Comparison args
    # "COMPARISON=COMP1-COMP2"
    elif arg.split('=')[0].upper() == 'LEVEL':
        LevelComparisons.append( (arg.split('=')[1].split('-')[0], arg.split('=')[1].split('-')[1]) )

    elif arg.split('=')[0].upper() == 'LOOP':
        LoopComparisons.append( (arg.split('=')[1].split('-')[0], arg.split('=')[1].split('-')[1]) )

    elif arg.split('=')[0].upper() == 'EVENT':
        EventComparisons.append( (arg.split('=')[1].split('-')[0], arg.split('=')[1].split('-')[1]) )

    elif arg.split('=')[0].upper() == 'ANALYSIS':
        AnalysisComparisons.append( (arg.split('=')[1].split('-')[0], arg.split('=')[1].split('-')[1]) )

    # Whether to do a run of normalised graphs or not.
    # "NORM=True/False"
    elif arg.split('=')[0].upper() == 'NORM':
        NormRuns.append( arg.split('=')[1] )


# Will recursively try to create each dir in MediaDir path
if len(MediaDir) > 0:
    for i in range(len(MediaDir.split('/'))):
        gSystem.Exec('mkdir '+'/'.join(MediaDir.split('/')[:i+1]))



# If no run is given for a level, set the runs to default
if len(FileComparisons) == 0:
    FileComparisons = [('','')]

if len(LevelComparisons) == 0:
    LevelComparisons = [('Generator', 'Detector'), ('Generator', 'Generator'), ('Detector', 'Detector')]

if len(LoopComparisons) == 0:
    LoopComparisons = [('Cuts', 'NoCuts'), ('Cuts', 'Cuts'), ('NoCuts', 'NoCuts')]

if len(EventComparisons) == 0:
    EventComparisons =  [('Cuts', 'NoCuts'), ('Cuts', 'Cuts'), ('NoCuts', 'NoCuts')]

if len(AnalysisComparisons) == 0:
    AnalysisComparisons = [('Cuts', 'NoCuts'), ('Cuts', 'Cuts'), ('NoCuts', 'NoCuts')]

if len(NormRuns) == 0:
    NormRuns = [True, False]   

# Keeps track of number of runs
loopnum = 0

# Loops through all combinations of each run
for FilePair in FileComparisons:
    for LevelRunPair in LevelComparisons:
        for LoopRunPair in LoopComparisons:
            for EventRunPair in EventComparisons:
                for AnalysisRunPair in AnalysisComparisons:
                    for Norm in NormRuns:
                        
                        loopnum += 1
                        print('Loop:', loopnum)

                        # Initialising varibles for Hist1 and Hist2 for this run
                        HistFile1_RootDir = RootDir[0]
                        HistFile1_Prefix = FilePair[0]
                        HistFile1_LevelRun = LevelRunPair[0]
                        HistFile1_LoopRun = LoopRunPair[0]
                        HistFile1_EventRun = EventRunPair[0]
                        HistFile1_AnalysisRun = AnalysisRunPair[0]
                        HistFile1_Name = HistFile1_RootDir+'/Loop'+HistFile1_LoopRun+'/Event'+HistFile1_EventRun+'/Analysis'+HistFile1_AnalysisRun+'/'+HistFile1_Prefix+HistFile1_LevelRun+'.root'

                        HistFile2_RootDir = RootDir[1]
                        HistFile2_Prefix = FilePair[1]
                        HistFile2_LevelRun = LevelRunPair[1]
                        HistFile2_LoopRun = LoopRunPair[1]
                        HistFile2_EventRun = EventRunPair[1]
                        HistFile2_AnalysisRun = AnalysisRunPair[1]
                        HistFile2_Name = HistFile2_RootDir+'/Loop'+HistFile2_LoopRun+'/Event'+HistFile2_EventRun+'/Analysis'+HistFile2_AnalysisRun+'/'+HistFile2_Prefix+HistFile2_LevelRun+'.root'

                        # Norm == True
                        if Norm:
                            Comparison = 'Norm'
                        # Norm == False
                        else:
                            Comparison = 'Rel'
                        
                        # Removes dir of previous version of this run 
                        gSystem.Exec('rm -R '+MediaDir+Comparison+HistFile1_Prefix+HistFile2_Prefix+'/Loop'+HistFile1_LoopRun+'-'+HistFile2_LoopRun+'/Event'+HistFile1_EventRun+'-'+HistFile2_EventRun+'/Analysis'+HistFile1_AnalysisRun+'-'+HistFile2_AnalysisRun+'/'+HistFile1_LevelRun+'-'+HistFile2_LevelRun+'Level/')
                        # Makes the dir for this run
                        gSystem.Exec('mkdir '+MediaDir+Comparison+HistFile1_Prefix+HistFile2_Prefix)
                        gSystem.Exec('mkdir '+MediaDir+Comparison+HistFile1_Prefix+HistFile2_Prefix+'/Loop'+HistFile1_LoopRun+'-'+HistFile2_LoopRun)
                        gSystem.Exec('mkdir '+MediaDir+Comparison+HistFile1_Prefix+HistFile2_Prefix+'/Loop'+HistFile1_LoopRun+'-'+HistFile2_LoopRun+'/Event'+HistFile1_EventRun+'-'+HistFile2_EventRun)
                        gSystem.Exec('mkdir '+MediaDir+Comparison+HistFile1_Prefix+HistFile2_Prefix+'/Loop'+HistFile1_LoopRun+'-'+HistFile2_LoopRun+'/Event'+HistFile1_EventRun+'-'+HistFile2_EventRun+'/Analysis'+HistFile1_AnalysisRun+'-'+HistFile2_AnalysisRun+'/')
                        gSystem.Exec('mkdir '+MediaDir+Comparison+HistFile1_Prefix+HistFile2_Prefix+'/Loop'+HistFile1_LoopRun+'-'+HistFile2_LoopRun+'/Event'+HistFile1_EventRun+'-'+HistFile2_EventRun+'/Analysis'+HistFile1_AnalysisRun+'-'+HistFile2_AnalysisRun+'/'+HistFile1_LevelRun+'-'+HistFile2_LevelRun+'Level/')

                        print('Current run:', MediaDir+Comparison+HistFile1_Prefix+HistFile2_Prefix+'/Loop'+HistFile1_LoopRun+'-'+HistFile2_LoopRun+'/Event'+HistFile1_EventRun+'-'+HistFile2_EventRun+'/Analysis'+HistFile1_AnalysisRun+'-'+HistFile2_AnalysisRun+'/'+HistFile1_LevelRun+'-'+HistFile2_LevelRun+'Level/')

                        # Read hist files and setup dict for each file using previously defined variables
                        HistFiles = {
                            1               :   {
                                'Prefix'        :   HistFile1_Prefix,
                                'LevelRun'      :   HistFile1_LevelRun,
                                'LoopRun'       :   HistFile1_LoopRun,
                                'EventRun'      :   HistFile1_EventRun,
                                'AnalysisRun'   :   HistFile1_AnalysisRun,
                                'Name'          :   HistFile1_Name,

                                'File'          :   TFile(HistFile1_Name)
                            },

                            2   :   {
                                'Prefix'        :   HistFile2_Prefix,
                                'LevelRun'      :   HistFile2_LevelRun,
                                'LoopRun'       :   HistFile2_LoopRun,
                                'EventRun'      :   HistFile2_EventRun,
                                'AnalysisRun'   :   HistFile2_AnalysisRun,
                                'Name'          :   HistFile2_Name,

                                'File'          :   TFile(HistFile2_Name)
                            },
                        }    

                        # Dict of requested hists generated from the Histograms.py script 
                        HistDict = requests.HistDict
                        # Dict of requested histogram comparisons
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

                                    HistFuncs.CompareHist(HistProps, MediaDir)
                                    HistFuncs.SigBack(HistProps, MediaDir)

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

                                HistFuncs.CompareHist(HistProps, MediaDir)
                                HistFuncs.SigBack(HistProps, MediaDir)

