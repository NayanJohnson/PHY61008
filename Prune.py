# Running this script:
# python script.py output.root
from ROOT import gSystem, TFile, TH1F, TMath

import config, requests, sys
import Loop_Funcs as LoopFuncs
import Prune_Funcs as PruneFuncs

# Initialising runs
LevelRuns = []
LoopRuns = []
EventRuns = []
AnalysisRuns = []

NRuns = 1
RootDir = ''
outfileprefix = ''

for arg in sys.argv:
    # Should filter the python script
    if arg.split('.')[-1] == 'py':
        continue

    # Dir arguements in the form "DIR=RUNDIR-MEDIADIR"
    elif arg.split('=')[0].upper() == 'RUNS':
        NRuns = int(arg.split('=')[1])

    # Dir arguements in the form "DIR=RUNDIR-MEDIADIR"
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

RunDirs = []
for run in range(NRuns):
    runstr = 'run_'+'{:02d}'.format(run+1)+'/'
    RunDirs.append(runstr)

# Looping through the cross section of all runs and taking an average
XsecList = []
for run in RunDirs:
    with open(run+'tag_1_pythia.log', 'r') as file:
        lines = file.read().splitlines()
        # Xsec is the last element of the last line
        XsecList.append( float(lines[-1].split()[-1]) )
Xsec = sum(XsecList)/len(XsecList)

RunTrees = [x+'tag_1_delphes_events.root' for x in RunDirs]
# Loading all runs at once
TreeDict = LoopFuncs.LoadTrees(RunTrees)

# Will recursively try to create each dir in RootDir path
if RootDir:
    for i in range(len(RootDir.split('/'))):
        gSystem.Exec('mkdir '+'/'.join(RootDir.split('/')[:i+1]))

for LoopRun in LoopRuns:
    gSystem.Exec('mkdir '+RootDir+'Loop'+LoopRun)
    for EventRun in EventRuns:
        gSystem.Exec('mkdir '+RootDir+'Loop'+LoopRun+'/Event'+EventRun)
        for AnalysisRun in AnalysisRuns:
            gSystem.Exec('mkdir '+RootDir+'Loop'+LoopRun+'/Event'+EventRun+'/Analysis'+AnalysisRun)
            for LevelRun in LevelRuns:
                PruneFuncs.EventLoop(TreeDict, Xsec, RootDir, outfileprefix, LevelRun, LoopRun, EventRun, AnalysisRun)
