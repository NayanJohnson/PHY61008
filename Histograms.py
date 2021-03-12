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

ParticleKeywords = config.ParticleKeywords
HistDict = congig.HistDict

# Get scaling factor for histograms
Scale = funcs.GetScale('tag_1_pythia.log', myTree['NEvents'])

# Initialise requested hists from HistDict
HistDict = funcs.MakeHists(HistDict, Scale)

# Looping through events
for n in range(myTree['NEvents']):

    # Reset particle list for the new event
    for _, dictionary in HistDict.items():
        dictionary['Particles'] = []
        
    # Reset ParticeDict for this event
    ParticleDict = {}
    for keyword in ParticleKeywords:
        ParticleDict = funcs.AddParticle(keyword, ParticleDict)

    # Particle loop with cuts
    EventDict = funcs.ParticleLoop(myTree, n)

    # Adding BeamElectron and BeamQuark
    ParticleDict = funcs.AddParticle('BeamElectron', ParticleDict, EventDict['BeamElectron'].P4())
    ParticleDict = funcs.AddParticle('BeamQuark', ParticleDict, EventDict['BeamQuark'].P4())

    # FinalElectron
    numbElectrons = EventDict['Count']['Electrons']
    for i in range(0, numbElectrons):
        # Checking that there is at least one electron present
        if numbElectrons != 0:
            LeadingElectron = EventDict['PTSorted']['Electron'][-1][1]
            ParticleDict = funcs.AddParticle('FinalBeamElectron', ParticleDict, LeadingElectron.P4())

    # Leading and SubLeading muons
    numbMuons = EventDict['Count']['Muons']
    for i in range(0, numbMuons):

        # Checking that there is at least one muon present
        if numbMuons != 0:
            Muon = EventDict['PTSorted']['Muon'][i][1]
            # Leading Muon
            if i == numbMuons - 1:
                ParticleDict = funcs.AddParticle('LeadingMuon', ParticleDict, Muon.P4(), Muon.PID)

            # SubLeading Muon
            elif i == numbMuons - 2 and 0 <= numbMuons - 2:
                ParticleDict = funcs.AddParticle('SubLeadingMuon', ParticleDict, Muon.P4(), Muon.PID)


    # WPlus and WMinus hists
    # Leading and SubLeading muons will always be from the W bosons 
    # (in this process) so I seperate them by charge to determine which
    # boson they came from

    # Will only run if that muon is present
    Muon = ParticleDict['LeadingMuon']
    if Muon['Check']:    
        if Muon['PID'] == 13:
            ParticleDict = funcs.AddParticle('WMinusMuon', ParticleDict, Muon['P4'])
        elif Muon['PID'] == -13:
            ParticleDict = funcs.AddParticle('WPlusMuon', ParticleDict, Muon['P4'])

    Muon = ParticleDict['SubLeadingMuon']
    if Muon['Check']:  
        if Muon['PID'] == 13:
            ParticleDict = funcs.AddParticle('WMinusMuon', ParticleDict, Muon['P4'])
        elif Muon['PID'] == -13:
            ParticleDict = funcs.AddParticle('WPlusMuon', ParticleDict, Muon['P4'])

    # Jets
    numbJets = EventDict['Count']['Jets']
    for i in range(0, numbJets):
        
        # Checking that there is at least one jet present
        if numbJets != 0:
            Jet = EventDict['PTSorted']['Jet'][i][1]

            # Selecting the leading jet
            if i == numbJets - 1:
                ParticleDict = funcs.AddParticle('LeadingJet', ParticleDict, Jet.P4(), isJet=True)
                ParticleDict = funcs.AddParticle('BeamJet', ParticleDict, Jet.P4(), isJet=True)
            # Selecting and checking for the subleading jet
            elif i == numbJets - 2 and numbJets - 2 >= 0:
                ParticleDict = funcs.AddParticle('SubLeadingJet', ParticleDict, Jet.P4(), isJet=True)
            # Selecting and checking for the third jet 
            elif i == numbJets - 3 and numbJets - 3 >= 0:
                ParticleDict = funcs.AddParticle('ThirdJet', ParticleDict, Jet.P4(), isJet=True)
            # Selecting and checking for the fourth jet
            elif i == numbJets - 4 and numbJets - 4 >= 0:
                ParticleDict = funcs.AddParticle('FourthJet', ParticleDict, Jet.P4(), isJet=True)
            # Any extra jets
            else:
                ParticleDict = funcs.AddParticle(str(i+1)+'Jet', ParticleDict, Jet.P4(), isJet=True)

    # MissingET
    ParticleDict = funcs.AddParticle('MissingET', ParticleDict, EventDict['MissingET_P'])

    # MuonSum
    MuonSum = None 
    if ParticleDict['LeadingMuon']['Check'] and ParticleDict['SubLeadingMuon']['Check']:
        MuonSum = ParticleDict['LeadingMuon']['P4'] + ParticleDict['SubLeadingMuon']['P4']
        ParticleDict = funcs.AddParticle('MuonSum', ParticleDict, MuonSum)

    # Count hists
    HistDict['Electrons']['Count'] = numbElectrons
    HistDict['Muons']['Count'] = numbMuons
    HistDict['Jets']['Count'] = numbJets

    # Filling HistDict with particles then filling the hists
    HistDict = funcs.RequestParticles(HistDict, ParticleDict)
    funcs.FillHists(HistDict)

# Rescaling hist lims
funcs.HistLims(HistDict)

# Writing and closing file
outfile.Write()
outfile.Close()