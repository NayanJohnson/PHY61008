# Running this script:
# python script.py output.root
from ROOT import TFile, TH1F, TMath

import config, requests, sys
import Loop_Funcs as LoopFuncs

# Initialising runs
LevelRuns = []
LoopRuns = []
EventRuns = []
AnalysisRuns =          {
    'MISSINGET'         :   [],
    'FINALBEAMELECTRON' :   [],
}

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
        AnalysisRuns[arg.split('_')[1]].append(arg.split('_')[2])

    # Should find the prefixes of hist files to be compared
    else:
        outfileprefix = arg


# If no run is given for a level, set the runs to default
if len(LevelRuns) == 0:
    LevelRuns = ['Generator', 'Detector']

if len(LoopRuns) == 0:
    LoopRuns = ['Cuts', 'NoCuts']

if len(EventRuns) == 0:
    EventRuns = ['Cuts', 'NoCuts']

if len(AnalysisRuns['MISSINGET']) == 0:
    AnalysisRuns['MISSINGET'] = ['Cuts', 'NoCuts']

if len(AnalysisRuns['FINALBEAMELECTRON']) == 0:
    AnalysisRuns['FINALBEAMELECTRON'] = ['Cuts', 'NoCuts']

# Load event file
myTree = LoopFuncs.LoadROOT('tag_1_delphes_events.root')

for LevelRun in LevelRuns:
    for LoopRun in LoopRuns:
        for EventRun in EventRuns:
            for MissingETRun in AnalysisRuns['MISSINGET']:
                for FinalBeamElectronRun in AnalysisRuns['FINALBEAMELECTRON']:
                    LoopFuncs.EventLoop(myTree, outfileprefix, LevelRun, LoopRun, EventRun, MissingETRun, FinalBeamElectronRun)
