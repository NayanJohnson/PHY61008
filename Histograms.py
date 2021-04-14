# Running this script:
# python script.py output.root
from ROOT import gSystem, TFile, TH1F, TMath

import config, requests, sys
import Loop_Funcs as LoopFuncs

# Initialising runs
LevelRuns = []
LoopRuns = []
EventRuns = []
AnalysisRuns = []

Runs = ['01']
MediaDir = ''

for arg in sys.argv:
    # Should filter the python script
    if arg.split('.')[-1] == 'py':
        continue

    # Dir arguements in the form "DIR=RUNDIR-MEDIADIR"
    elif arg.split('=')[0].upper() == 'RUNS':
        Runs = arg.split('=')[1].split('-')

    # Dir arguements in the form "DIR=RUNDIR-MEDIADIR"
    elif arg.split('=')[0].upper() == 'MEDIA':
        MediaDir = arg.split('=')[1]


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

# run folders => "run_x/"
Runs = ['run_'+run+'/' for run in Runs]

# Looping through the cross section of all runs and taking an average
XsecList = []
for run in Runs:
    with open(run+'tag_1_pythia.log', 'r') as file:
        lines = file.read().splitlines()
        # Xsec is the last element of the last line
        XsecList.append( float(lines[-1].split()[-1]) )

Xsec = sum(XsecList)/len(XsecList)

# Loading all runs at once
myTree = LoopFuncs.LoadROOT(Runs)

# Will recursively try to create each dir in RootDir path
if MediaDir:
    for i in range(len(MediaDir.split('/'))):
        gSystem.Exec('mkdir '+'/'.join(MediaDir.split('/')[:i+1]))

    # Load event file

for LevelRun in LevelRuns:
    for LoopRun in LoopRuns:
        for EventRun in EventRuns:
            for AnalysisRun in AnalysisRuns:
                LoopFuncs.EventLoop(myTree, Xsec, MediaDir, outfileprefix, LevelRun, LoopRun, EventRun, AnalysisRun)
