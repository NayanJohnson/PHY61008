# Running this script:
# python script.py output.root
import sys
import Analysis_Funcs as funcs
import config
from ROOT import TFile, TH1F, TMath

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
myTree = funcs.LoadROOT("tag_1_delphes_events.root")

def EventLoop(myTree, outfileprefix, LoopRun, EventRun, BackgroundRun):
    '''
    '''

    outfilename = outfileprefix+'_Loop'+LoopRun+'Event'+EventRun+'Background'+BackgroundRun+'.root'

    # Open output
    outfile = TFile(outfilename,"RECREATE")

    HistDict = config.HistDict

    # Initialise requested hists from HistDict
    HistDict = funcs.MakeHists(HistDict)

    EventCuts = config.EventLoopParams['Level']['Event'][EventRun]
    BackgroundCuts = config.EventLoopParams['Level']['Background'][BackgroundRun] 
    
    Zdecays = config.EventLoopParams['Z']['Decays']
    WPlusdecays = config.EventLoopParams['WPlus']['Decays']
    WMinusdecays = config.EventLoopParams['WMinus']['Decays']
    
    EventCutNum = 0
    # Looping through events
    for EventNum in range(myTree['NEvents']):

        HistDict, ParticleDict, EventDict = funcs.GetParticles(myTree, LoopRun, HistDict, EventNum)

        FinalBeamElectron_Sorted = list(EventDict['PTSorted']['Electron'])

        # print('before:', len(FinalBeamElectron_Sorted))
        # print([(x, x[1].P4().Eta()) for x in FinalBeamElectron_Sorted])
        # i = 0
        

        # Cuts out electrons in the PTSorted list and then takes the leading result as the beam electron
        for particle in EventDict['PTSorted']['Electron']:
            # print(particle)
            # i+=1
            # print(i)
            if BackgroundCuts['BeamElectron']['Eta'][0] <= particle[1].P4().Eta() <= BackgroundCuts['BeamElectron']['Eta'][1]:
                # print('Pass')
                continue
            else:
                FinalBeamElectron_Sorted.remove(particle)
                # print('Remove')

        # print('after:', len(FinalBeamElectron_Sorted))
        # print([(x, x[1].P4().Eta()) for x in FinalBeamElectron_Sorted])

        if len(FinalBeamElectron_Sorted) != 0:
            ParticleDict = funcs.AddParticle('FinalBeamElectron', ParticleDict, FinalBeamElectron_Sorted[-1][1].P4())
        else:
            continue


        # Event level selection for WWEmJ_WW_Muons
        if EventDict['Count']['Electrons'] >= EventCuts['Electrons'] and EventDict['Count']['Muons'] >= EventCuts['Muons'] and EventDict['Count']['Jets'] >= EventCuts['Jets']:
            
            EventCutNum += 1
            for Zdecay in Zdecays:
                if Zdecay == None:
                    continue
                elif Zdecays[0] == Zdecays[1]:
                    continue
                else:
                    ParticleDict, EventDict = funcs.InvMassCheck(Zdecay, 'Z', ParticleDict, EventDict)

            for WPlusdecay in WPlusdecays:
                if WPlusdecay == None:
                    continue
                elif WPlusdecays[0] == WPlusdecays[1]:
                    continue            
                elif WPlusdecay == 'Jets':
                    ParticleDict, EventDict = funcs.InvMassCheck(WPlusdecay, 'WPlus', ParticleDict, EventDict)
                else:
                    particlesList = [ParticleDict['Leading'+WPlusdecay[0:-1]], ParticleDict['SubLeading'+WPlusdecay[0:-1]]]
                    for Lepton in particlesList:
                        if Lepton['Check']:
                            if Lepton['PID'] == -13:
                                ParticleDict = funcs.AddParticle('WPlus'+WPlusdecay[0:-1], ParticleDict, Lepton['P4'])

            for WMinusdecay in WMinusdecays:
                if WMinusdecay == None:
                    continue
                elif WMinusdecays[0] == WMinusdecays[1]:
                    continue            
                elif WMinusdecay == 'Jets':
                    ParticleDict, EventDict = funcs.InvMassCheck(WMinusdecay, 'WMinus', ParticleDict, EventDict)
                else:
                    particlesList = [ParticleDict['Leading'+WMinusdecay[0:-1]], ParticleDict['SubLeading'+WMinusdecay[0:-1]]]
                    for Lepton in particlesList:
                        if Lepton['Check']:
                            if Lepton['PID'] == 13:
                                ParticleDict = funcs.AddParticle('WMinus'+WMinusdecay[0:-1], ParticleDict, Lepton['P4'])

            if len(EventDict['PTSorted']['Jet']) != 0:
                ParticleDict = funcs.AddParticle('FinalBeamJet', ParticleDict, EventDict['PTSorted']['Jet'][-1][1].P4())

            # Filling HistDict with particles then filling the hists
            HistDict = funcs.RequestParticles(HistDict, ParticleDict)
            funcs.FillHists(HistDict)

    # Get scaling factor for histograms
    Scale = funcs.GetScale('tag_1_pythia.log', myTree['NEvents'])

    # Scaling and altering hist lims
    for category, properties in HistDict.items():
        for var, hist in properties['Hists'].items():
            hist = funcs.HistLims(hist, var, Scale=Scale)[0]
    # Writing and closing file
    outfile.Write()
    outfile.Close()

for LoopRun in LoopRuns:
    for EventRun in EventRuns:
        for BackgroundRun in BackgroundRuns:
            EventLoop(myTree, outfileprefix, LoopRun, EventRun, BackgroundRun)
