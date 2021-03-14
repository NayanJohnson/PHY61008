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

    # Setting FinalBeamElectron
    ParticleDict['FinalBeamElectron'] = ParticleDict['LeadingElectron']
    
    # Seperating out boson muons 
    # Only attempt this if all muons are present
    ZMuonInvMassList = []
    if ParticleDict['LeadingMuon']['Check'] and ParticleDict['SubLeadingMuon']['Check'] and ParticleDict['ThirdMuon']['Check']:  
        MuonPermutations = [
            (ParticleDict['LeadingMuon'], ParticleDict['SubLeadingMuon'], ParticleDict['ThirdMuon']),
            (ParticleDict['LeadingMuon'], ParticleDict['ThirdMuon'], ParticleDict['SubLeadingMuon']),
            (ParticleDict['SubLeadingMuon'], ParticleDict['ThirdMuon'], ParticleDict['LeadingMuon'])
        ]

        # Calculating InvMass of the three different muon pairs
        for MuonPair in MuonPermutations:
            ZMuonInvMassList.append(funcs.GetParticleVariable('InvMass', MuonPair[0:2]))

        # Find the closest InvMass to the Z mass
        ZMuonPairInvMass = min(ZMuonInvMassList, key=lambda x:abs(x-91.1876))
        ZMuonPairIndex = ZMuonInvMassList.index(ZMuonPairInvMass)
        if MuonPermutations[ZMuonPairIndex][0]['Pt'] < MuonPermutations[ZMuonPairIndex][1]['Pt']:
            ParticleDict['ZLeadingMuon'] = MuonPermutations[ZMuonPairIndex][1]
            ParticleDict['ZSubLeadingMuon'] = MuonPermutations[ZMuonPairIndex][0]
        else:        
            ParticleDict['ZSubLeadingMuon'] = MuonPermutations[ZMuonPairIndex][1]
            ParticleDict['ZLeadingMuon'] = MuonPermutations[ZMuonPairIndex][0]
        ParticleDict['WPlusMuon'] = MuonPermutations[ZMuonPairIndex][2]

    # Filling HistDict with particles then filling the hists
    HistDict = funcs.RequestParticles(HistDict, ParticleDict)
    funcs.FillHists(HistDict)

# Rescaling hist lims
funcs.HistLims(HistDict)

# Writing and closing file
outfile.Write()
outfile.Close()