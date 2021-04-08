# Running this script:
# python script.py output.root
from ROOT import TFile, TH1F, TMath

import config, requests, sys
import Loop_Funcs as LoopFuncs

# Initialising runs
LoopRuns = []
BackgroundRuns = []
EventRuns = []

for arg in sys.argv:
    # Should filter the python script
    if arg.split('.')[-1] == 'py':
        continue

    # Looks for arguements passing the runs to compare
    elif arg.split('_')[0].upper() == 'LOOP':
        LoopRuns.append(arg.split('_')[1])

    elif arg.split('_')[0].upper() == 'ANALYSIS':
        BackgroundRuns.append(arg.split('_')[1])

    elif arg.split('_')[0].upper() == 'EVENT':
        EventRuns.append(arg.split('_')[1])

    # Should find the prefixes of hist files to be compared
    else:
        outfileprefix = arg

# If no run is given for a level, set the runs to default
for Run in (LoopRuns, BackgroundRuns, EventRuns):
    if len(LoopRuns) == 0:
        Run = ['Cuts', 'NoCuts']

# Load event file
myTree = LoopFuncs.LoadROOT("tag_1_delphes_events.root")

for LoopRun in LoopRuns:
    for EventRun in EventRuns:
        for BackgroundRun in BackgroundRuns:
            LoopFuncs.EventLoop(myTree, outfileprefix, LoopRun, EventRun, BackgroundRun)
