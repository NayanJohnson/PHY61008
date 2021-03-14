# Running this script:
# python script.py output.root
import sys
import Analysis_Funcs as funcs
import config
from ROOT import TFile, TH1F, TMath

# sys.argv[1] returns the first argument passed to the python script
outfilename = sys.argv[1]

# Open output
outfile = TFile(outfilename,"RECREATE")

# Load event file
myTree = funcs.LoadROOT("tag_1_delphes_events.root")


HistDict = config.HistDict

# Get scaling factor for histograms
Scale = funcs.GetScale('tag_1_pythia.log', myTree['NEvents'])

# Initialise requested hists from HistDict
HistDict = funcs.MakeHists(HistDict, Scale)

# Looping through events
for EventNum in range(myTree['NEvents']):

    HistDict, ParticleDict = funcs.GetParticles(myTree, HistDict, EventNum)

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

# Rescaling hist lims
funcs.HistLims(HistDict)

# Writing and closing file
outfile.Write()
outfile.Close()