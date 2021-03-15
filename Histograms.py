# Running this script:
# python script.py output.root
import sys
import Analysis_Funcs as funcs
import config
from ROOT import TFile, TH1F, TMath

# sys.argv[1] returns the first argument passed to the python script
outfileprefix = sys.argv[1]
Runs = sys.argv[2:]
ParticleRuns = [x.split('_')[1]for x in Runs if x.split('_')[0]=='Particle']
EventRuns = [x.split('_')[1] for x in Runs if x.split('_')[0]=='Event']

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

    EventCuts = config.EventLoopParams['EventLevel'][EventRun]
    # Looping through events
    for EventNum in range(myTree['NEvents']):

        HistDict, ParticleDict, EventDict = funcs.GetParticles(myTree, ParticleRun, HistDict, EventNum)

        # Event level selection for WWEmJ_WW_Muons
        if EventDict['Count']['Electrons'] >= EventCuts['Electrons'] and EventDict['Count']['Muons'] >= EventCuts['Muons'] and EventDict['Count']['Jets'] >= EventCuts['Jets']:
            ParticleDict['FinalBeamElectron'] = ParticleDict['LeadingElectron']
            
            # WPlus and WMinus hists
            # Leading and SubLeading muons will always be from the W bosons 
            # (in this process) so I seperate them by charge to determine which
            # boson they came from

            # Will only run if that muon is present
            for Muon in [ParticleDict['LeadingMuon'], ParticleDict['SubLeadingMuon']]:
                if Muon['Check']:    
                    if Muon['PID'] == 13:
                        ParticleDict = funcs.AddParticle('WMinusMuon', ParticleDict, Muon['P4'])
                    elif Muon['PID'] == -13:
                        ParticleDict = funcs.AddParticle('WPlusMuon', ParticleDict, Muon['P4'])


            # Filling HistDict with particles then filling the hists
            HistDict = funcs.RequestParticles(HistDict, ParticleDict)
            funcs.FillHists(HistDict)

    # Get scaling factor for histograms
    Scale = funcs.GetScale('tag_1_pythia.log', myTree['NEvents'])

    # Scaling and altering hist lims
    funcs.HistLims(HistDict, Scale)

    # Writing and closing file
    outfile.Write()
    outfile.Close()
for EventRun in EventRuns:
    for ParticleRun in ParticleRuns:
        EventLoop(myTree, outfileprefix, EventRun, ParticleRun)