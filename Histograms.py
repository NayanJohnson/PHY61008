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

myTree = LoopFuncs.LoadTrees(Trees)
Xsec = config.EventLoopParams['Xsec']

# If no run is given for a level, set the runs to default
if len(LevelRuns) == 0:
    LevelRuns = ['Generator', 'Detector']

if len(LoopRuns) == 0:
    LoopRuns = ['Cuts', 'NoCuts']

if len(AnalysisRuns) == 0:
    AnalysisRuns = ['Cuts', 'NoCuts']

if len(EventRuns) == 0:
    EventRuns = ['Cuts', 'NoCuts']

# Will recursively try to create each dir in RootDir path
if RootDir:
    for i in range(len(RootDir.split('/'))):
        gSystem.Exec('mkdir '+'/'.join(RootDir.split('/')[:i+1]))

# Load event file
for LevelRun in LevelRuns:
    for LoopRun in LoopRuns:
        for EventRun in EventRuns:
            for AnalysisRun in AnalysisRuns:
                LoopFuncs.EventLoop(myTree, Xsec, RootDir, outfileprefix, LevelRun, LoopRun, EventRun, AnalysisRun)
