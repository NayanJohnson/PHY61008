# Running this script:
# python script.py output.root
import sys
import Analysis_Funcs as funcs
import config
from ROOT import TFile, TH1F, TMath

EventRuns = []
ParticleRuns = []

for arg in sys.argv:
    # Should filter the python script
    if arg.split('.')[-1] == 'py':
        continue

    # Looks for arguements passing the runs to compare
    elif arg.split('_')[0] == 'Event':
        EventRuns.append(arg.split('_')[1])

    elif arg.split('_')[0] == 'Particle':
        ParticleRuns.append(arg.split('_')[1])

    # Should find the prefixes of hist files to be compared
    else:
        outfileprefix = arg

# Load event file
myTree = funcs.LoadROOT("tag_1_delphes_events.root")

def EventLoop(myTree, outfileprefix, EventRun, ParticleRun):
    '''
    '''

    outfilename = outfileprefix+'_'+'Event'+EventRun+'Particle'+ParticleRun+'.root'

    # Open output
    outfile = TFile(outfilename,"RECREATE")

    HistDict = config.HistDict

    # Initialise requested hists from HistDict
    HistDict = funcs.MakeHists(HistDict)

    EventCuts = config.EventLoopParams['Runs']['EventLevel'][EventRun]
    
    Zdecays = config.EventLoopParams['Z']['Decays']
    WPlusdecays = config.EventLoopParams['WPlus']['Decays']
    WMinusdecays = config.EventLoopParams['WMinus']['Decays']
    
    EventCutNum = 0
    # Looping through events
    for EventNum in range(myTree['NEvents']):

        HistDict, ParticleDict, EventDict = funcs.GetParticles(myTree, ParticleRun, HistDict, EventNum)
        
        # print(EventDict['Count']['Electrons'], EventCuts['Electrons'], EventDict['Count']['Muons'], EventCuts['Muons'],  EventDict['Count']['Jets'], EventCuts['Jets'])
        
        # Event level selection for WWEmJ_WW_Muons
        if EventDict['Count']['Electrons'] >= EventCuts['Electrons'] and EventDict['Count']['Muons'] >= EventCuts['Muons'] and EventDict['Count']['Jets'] >= EventCuts['Jets']:
            
            ParticleDict['FinalBeamElectron'] = ParticleDict['LeadingElectron']
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
                    particlesList = [ParticleDict['Leading'+ 
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
            hist = HistLims(hist, var, Scale=Scale)
    # Writing and closing file
    outfile.Write()
    outfile.Close()

for EventRun in EventRuns:
    for ParticleRun in ParticleRuns:
        EventLoop(myTree, outfileprefix, EventRun, ParticleRun)
