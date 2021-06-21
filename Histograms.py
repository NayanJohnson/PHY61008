# Running this script:
# python script.py output.root
from ROOT import gSystem, TFile, TH1F, TMath

import config, requests, sys
import Loop_Funcs as LoopFuncs

Trees = []

# Initialising runs
LevelRuns = []
LoopRuns = []
EventRuns = []
AnalysisRuns = []

Runs = 1
RootDir = ''
outfileprefix = ''

for arg in sys.argv:
    # Should filter the python script
    if arg.split('.')[-1] == 'py':
        continue

    # The filename of the data set stored as a .root TTree
    # Recognised as "tree=TREE"
    elif arg.split('=')[0].upper() == 'TREE':
        Trees.append(arg.split('=')[1])

    # The directory of the data set
    # Recognised as "rootdir=DIR"
    elif arg.split('=')[0].upper() == 'ROOTDIR':
        RootDir = arg.split('=')[1]

    # Prefix added to the .root file containing the histograms
    # Also used as an identifier of the dataset being used
    # (used as an index in config.py when looking for NEvents/XSec/Cuts)

    # The config.py part is the main function, so maybe this variable name should 
    # be changed to indicate that

    # Recognised as "prefix=PREFIX"
    elif arg.split('=')[0].upper() == 'PREFIX':
        outfileprefix = arg.split('=')[1]

    # What cuts to run
    # Recognised as "run=RUN" 
    
    # RUN is used as an index in config.py so should generally == "Cuts" OR "NoCuts"
    # This could of course be changed by adding new types of runs to config.py
    elif arg.split('=')[0].upper() == 'LEVEL':
        LevelRuns.append(arg.split('=')[1])

    elif arg.split('=')[0].upper() == 'LOOP':
        LoopRuns.append(arg.split('=')[1])

    elif arg.split('=')[0].upper() == 'EVENT':
        EventRuns.append(arg.split('=')[1])

    elif arg.split('=')[0].upper() == 'ANALYSIS':
        AnalysisRuns.append(arg.split('=')[1])

# If no run is given for a level, set the runs to default
if len(LevelRuns) == 0:
    LevelRuns = ['Generator', 'Detector']

if len(LoopRuns) == 0:
    LoopRuns = ['Cuts', 'NoCuts']

if len(AnalysisRuns) == 0:
    AnalysisRuns = ['Cuts', 'NoCuts']

if len(EventRuns) == 0:
    EventRuns = ['Cuts', 'NoCuts']

# Loading Trees
myTree = LoopFuncs.LoadTrees(Trees, outfileprefix)

# Getting Xsec from config.py 
Xsec = config.EventLoopParams[outfileprefix]['Xsec']

# Will recursively try to create each dir in RootDir path
if len(RootDir) > 0:
    for i in range(len(RootDir.split('/'))):
        gSystem.Exec('mkdir '+'/'.join(RootDir.split('/')[:i+1]))



# Loops through each combination of runs
# Makes a seperate directory for each combination
for LoopRun in LoopRuns:
    gSystem.Exec('mkdir '+RootDir+'/Loop'+LoopRun)
    for EventRun in EventRuns:
        gSystem.Exec('mkdir '+RootDir+'/Loop'+LoopRun+'/Event'+EventRun)
        for AnalysisRun in AnalysisRuns:
            gSystem.Exec('mkdir '+RootDir+'/Loop'+LoopRun+'/Event'+EventRun+'/Analysis'+AnalysisRun)
            for LevelRun in LevelRuns:
                print('Started run:', RootDir+'/Loop'+LoopRun+'/Event'+EventRun+'/Analysis'+AnalysisRun)
                # Makes outfilename from directories and prefix
                outfilename = RootDir+'/Loop'+LoopRun+'/Event'+EventRun+'/Analysis'+AnalysisRun+'/'+outfileprefix+LevelRun
                # Main loop
                LoopFuncs.EventLoop(myTree, Xsec, outfilename, LevelRun, LoopRun, EventRun, AnalysisRun)
