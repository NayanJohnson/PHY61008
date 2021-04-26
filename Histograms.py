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

    elif arg.split('=')[0].upper() == 'TREE':
        Trees.append(arg.split('=')[1])

    # Dir arguements in the form
    elif arg.split('=')[0].upper() == 'ROOTDIR':
        RootDir = arg.split('=')[1]

    elif arg.split('=')[0].upper() == 'PREFIX':
        outfileprefix = arg.split('=')[1]

    # Looks for arguements passing the runs to compare
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

# Getting Xsec from config file 
Xsec = config.EventLoopParams[outfileprefix]['Xsec']

# Will recursively try to create each dir in RootDir path
if len(RootDir) > 0:
    for i in range(len(RootDir.split('/'))):
        gSystem.Exec('mkdir '+'/'.join(RootDir.split('/')[:i+1]))




for LoopRun in LoopRuns:
    gSystem.Exec('mkdir '+RootDir+'/Loop'+LoopRun)
    for EventRun in EventRuns:
        gSystem.Exec('mkdir '+RootDir+'/Loop'+LoopRun+'/Event'+EventRun)
        for AnalysisRun in AnalysisRuns:
            gSystem.Exec('mkdir '+RootDir+'/Loop'+LoopRun+'/Event'+EventRun+'/Analysis'+AnalysisRun)
            for LevelRun in LevelRuns:
                print('Started run:', RootDir+'/Loop'+LoopRun+'/Event'+EventRun+'/Analysis'+AnalysisRun)
                outfilename = RootDir+'/Loop'+LoopRun+'/Event'+EventRun+'/Analysis'+AnalysisRun+'/'+outfileprefix+LevelRun
                LoopFuncs.EventLoop(myTree, Xsec, outfilename, LevelRun, LoopRun, EventRun, AnalysisRun)
