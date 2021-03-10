# Dictionary that will contain all info needed to produce histograms.
# Vars list can be used to request specific histograms
# Var keywords that are recognised:
# ['Count', 'Eta', 'Phi', 'Rapidity', 'Pt', 'Et', 'q', 
# 'dEta', 'dPhi', 'dRapidity', 'dR_Eta', 'dR_Rap', 'InvMass']
HistDict = {
    'Electrons'     :   {
        'Vars'      :   ['Count'],
    },
    'Muons'         :   {
        'Vars'      :   ['Count'],
    },
    'Jets'          :   {
        'Vars'      :   ['Count'],
    },
    'FinalElectron' :   {
        'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
    },
    'LeadingMuon'   :   {
        'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
    },
    'SubLeadingMuon':   {
        'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
    },
    'WPlusMuon'     :   {
        'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
    },
    'WMinusMuon'    :   {
        'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
    },
    'AllJets'       :   {
        'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
    },
    'LeadingJet'    :   {
        'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
    },
    'SubLeadingJet' :   {
        'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
    },
    'ThirdJet'      :   {
        'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
    },
    'FourthJet'     :   {
        'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
    },
    'MissingET'     :   {
        'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', 'Et'],
    },
    'q_Lepton'      :   {
        'Vars'      :   ['q'],
    },
    'q_Quark'       :   {
        'Vars'      :   ['q'],
    },
    'q_eMethod'     :   {
        'Vars'      :   ['q'],
    },
    'FinalElectronLeadingMuon'  :   {
        'Vars'      :   ['dEta', 'dPhi'],
    },
    'FinalElectronSubLeadingMuon'  :   {
        'Vars'      :   ['dEta', 'dPhi'],
    },
    'FinalElectronLeadingJet'   :   {
        'Vars'      :   ['dEta', 'dPhi', 'dRapidity', 'dR_Eta', 'dR_Rap', 'InvMass'],
    },
    'MuonMuon'      :   {
        'Vars'      :   ['dEta', 'dPhi', 'dRapidity', 'dR_Eta', 'dR_Rap', 'InvMass'],
    },
    'LeadingMuonLeadingJet'  :   {
        'Vars'      :   ['dEta', 'dPhi'],
    },
    'SubLeadingMuonLeadingJet'  :   {
        'Vars'      :   ['dEta', 'dPhi'],
    },
    'MissingETFinalElectron'    :   {
        'Vars'      :   ['dPhi', 'InvMass'],
    },
    'MissingETLeadingJet'  :   {
        'Vars'      :   ['dPhi', 'InvMass'],
    },
    'MissingETLeadingMuon'  :   {
        'Vars'      :   ['dPhi', 'InvMass'],
    },
    'MissingETSubLeadingMuon'   :   {
        'Vars'      :   ['dPhi', 'InvMass'],
    },
    'MissingETMuonSum'      :   {
        'Vars'      :   ['dPhi', 'InvMass'],
    },
}

# Add empty particle list and hist dictionary to HistDict
for _, dictionary in HistDict.items():
    dictionary['Particles'] = []
    dictionary['Hists'] = {}


import Analysis_Funcs as funcs

# Load event file
myTree = funcs.LoadROOT("tag_1_delphes_events.root")

from ROOT import TFile, TH1F, TMath

import sys

# Open output
# sys.argv[1] returns the first argument passed to the python script
outfile = TFile(sys.argv[1],"RECREATE")

# Get scaling factor for histograms
Scale = funcs.GetScale('tag_1_pythia.log', myTree['NEvents'])

# Initialise requested hists from HistDict
HistDict = funcs.MakeHists(HistDict, Scale)

# Looping through events
for n in range(myTree['NEvents']):

    # Reset particle list for the new event
    for _, dictionary in HistDict.items():
        dictionary['Particles'] = []

    # Variables for checking if the particle has been detected in this event
    FinalElectronCheck = False
    LeadingMuonCheck = False
    SubLeadingMuonCheck = False
    LeadingJetCheck = False
    SubLeadingJetCheck = False

    # Particle loop with cuts
    EventDict = funcs.ParticleLoop(myTree, n)

    # Reset ParticeDict for this event
    ParticleDict = {}

    # Adding BeamElectron and BeamQuark
    ParticleDict = funcs.AddParticle('BeamElectron', EventDict['BeamElectron'].PID, EventDict['BeamElectron'].P4(), ParticleDict)
    ParticleDict = funcs.AddParticle('BeamQuark', EventDict['BeamQuark'].PID, EventDict['BeamQuark'].P4(), ParticleDict)

    # FinalElectron
    numbElectrons = EventDict['Count']['Electrons']
    for i in range(0, numbElectrons):
        # Checking that there is at least one electron present
        if numbElectrons != 0:
            FinalElectronCheck = True
            Electron = EventDict['PTSorted']['Electron'][-1][1]
            ParticleDict = funcs.AddParticle('FinalElectron', Electron.PID, Electron.P4(), ParticleDict)
            # FinalElectron hists
            HistDict['FinalElectron']['Particles'].append(ParticleDict['FinalElectron'])

    # Leading and SubLeading muons
    numbMuons = EventDict['Count']['Muons']
    for i in range(0, numbMuons):

        # Checking that there is at least one muon present
        if numbMuons != 0:
            Muon = EventDict['PTSorted']['Muon'][i][1]
            # Leading Muon
            if i == numbMuons - 1:
                LeadingMuonCheck = True
                ParticleDict = funcs.AddParticle('LeadingMuon', Muon.PID, Muon.P4(), ParticleDict)
                # LeadingMuon hists
                HistDict['LeadingMuon']['Particles'].append(ParticleDict['LeadingMuon'])

            # SubLeading Muon
            elif i == numbMuons - 2 and 0 <= numbMuons - 2:
                SubLeadingMuonCheck = True
                ParticleDict = funcs.AddParticle('SubLeadingMuon', Muon.PID, Muon.P4(), ParticleDict)
                # SubLeadingMuon hists
                HistDict['SubLeadingMuon']['Particles'].append(ParticleDict['SubLeadingMuon'])


    # WPlus and WMinus hists
    # Leading and SubLeading muons will always be from the W bosons 
    # (in this process) so I seperate them by charge to determine which
    # boson they came from

    # Will only run if that muon is present
    if LeadingMuonCheck:    
        if ParticleDict['LeadingMuon']['PID'] == 13:
            HistDict['WMinusMuon']['Particles'].append(ParticleDict['LeadingMuon'])

        elif ParticleDict['LeadingMuon']['PID'] == -13:
            HistDict['WPlusMuon']['Particles'].append(ParticleDict['LeadingMuon'])

    if SubLeadingMuonCheck:  
        if ParticleDict['SubLeadingMuon']['PID'] == 13:
            HistDict['WMinusMuon']['Particles'].append(ParticleDict['SubLeadingMuon'])
        
        elif ParticleDict['SubLeadingMuon']['PID'] == -13:
            HistDict['WPlusMuon']['Particles'].append(ParticleDict['SubLeadingMuon'])
    
    # Jets
    numbJets = EventDict['Count']['Jets']
    for i in range(0, numbJets):
        
        # Checking that there is at least one jet present
        if numbJets != 0:
            Jet = EventDict['PTSorted']['Jet'][i][1]

            # Selecting the leading jet
            if i == numbJets - 1:
                LeadingJetCheck = True
                ParticleDict = funcs.AddParticle('LeadingJet', None, Jet.P4(), ParticleDict)
                # LeadingJet and AllJet hists
                HistDict['LeadingJet']['Particles'].append(ParticleDict['LeadingJet'])
                HistDict['AllJets']['Particles'].append(ParticleDict['LeadingJet'])


            # Selecting and checking for the subleading jet
            elif i == numbJets - 2 and numbJets - 2 >= 0:
                SubLeadingJetCheck = True
                ParticleDict = funcs.AddParticle('SubLeadingJet', None, Jet.P4(), ParticleDict)
                # SubLeadingJet and AllJet hists                
                HistDict['SubLeadingJet']['Particles'].append(ParticleDict['SubLeadingJet'])
                HistDict['AllJets']['Particles'].append(ParticleDict['SubLeadingJet'])
            
            # Selecting and checking for the third jet 
            elif i == numbJets - 3 and numbJets - 3 >= 0:
                ParticleDict = funcs.AddParticle('ThirdJet', None, Jet.P4(), ParticleDict)
                # ThirdJet and AllJet hists                
                HistDict['ThirdJet']['Particles'].append(ParticleDict['ThirdJet'])
                HistDict['AllJets']['Particles'].append(ParticleDict['ThirdJet'])

            # Selecting and checking for the fourth jet
            elif i == numbJets - 4 and numbJets - 4 >= 0:
                ParticleDict = funcs.AddParticle('FourthJet', None, Jet.P4(), ParticleDict)
                # FourthJet and AllJet hists                                
                HistDict['FourthJet']['Particles'].append(ParticleDict['FourthJet'])
                HistDict['AllJets']['Particles'].append(ParticleDict['FourthJet'])

            else:
                ParticleDict = funcs.AddParticle(str(i+1)+'Jet', None, Jet.P4(), ParticleDict)
                # AllJet hists                 
                HistDict['AllJets']['Particles'].append(ParticleDict[str(i+1)+'Jet'])

    # MissingET
    ParticleDict = funcs.AddParticle('MissingET', None, EventDict['MissingET_P'], ParticleDict)
    # MissingET hists
    HistDict['MissingET']['Particles'].append(ParticleDict['MissingET'])

    # q hists
    if FinalElectronCheck:
        HistDict['q_Lepton']['Particles'].append(ParticleDict['FinalElectron'])
        HistDict['q_Lepton']['Particles'].append(ParticleDict['BeamElectron'])

        HistDict['q_eMethod']['Particles'].append(ParticleDict['FinalElectron'])
        HistDict['q_eMethod']['Particles'].append(ParticleDict['BeamElectron'])

    if LeadingJetCheck:
        HistDict['q_Quark']['Particles'].append(ParticleDict['LeadingJet'])
        HistDict['q_Quark']['Particles'].append(ParticleDict['BeamQuark'])

    # Count hists
    HistDict['Electrons']['Count'] = numbElectrons
    HistDict['Muons']['Count'] = numbMuons
    HistDict['Jets']['Count'] = numbJets

    # LeadingMuon comparison hists
    if LeadingMuonCheck and SubLeadingMuonCheck:
        HistDict['MuonMuon']['Particles'].append(ParticleDict['LeadingMuon'])
        HistDict['MuonMuon']['Particles'].append(ParticleDict['SubLeadingMuon'])


    # FinalElectron-LeadingMuon comparison hists
    if FinalElectronCheck and LeadingMuonCheck:
        HistDict['FinalElectronLeadingMuon']['Particles'].append(ParticleDict['FinalElectron'])
        HistDict['FinalElectronLeadingMuon']['Particles'].append(ParticleDict['LeadingMuon'])

    # FinalElectron-SubLeadingMuon comparison hists
    if FinalElectronCheck and SubLeadingMuonCheck:
        HistDict['FinalElectronSubLeadingMuon']['Particles'].append(ParticleDict['FinalElectron'])
        HistDict['FinalElectronSubLeadingMuon']['Particles'].append(ParticleDict['SubLeadingMuon'])


    if FinalElectronCheck and LeadingJetCheck:
        # FinalElectron-LeadingJet comparison hists
        HistDict['FinalElectronLeadingJet']['Particles'].append(ParticleDict['FinalElectron'])
        HistDict['FinalElectronLeadingJet']['Particles'].append(ParticleDict['LeadingJet'])

    if LeadingMuonCheck and LeadingJetCheck:
        # LeadingJet-LeadingJet comparison hists
        HistDict['LeadingMuonLeadingJet']['Particles'].append(ParticleDict['LeadingMuon'])
        HistDict['LeadingMuonLeadingJet']['Particles'].append(ParticleDict['LeadingJet'])

    if SubLeadingMuonCheck and LeadingJetCheck:
        # SubLeadingJet-LeadingJet comparison hists
        HistDict['SubLeadingMuonLeadingJet']['Particles'].append(ParticleDict['SubLeadingMuon'])
        HistDict['SubLeadingMuonLeadingJet']['Particles'].append(ParticleDict['LeadingJet'])

    if FinalElectronCheck:
        # MissingET-FinalElectron comparison hists
        HistDict['MissingETFinalElectron']['Particles'].append(ParticleDict['MissingET'])
        HistDict['MissingETFinalElectron']['Particles'].append(ParticleDict['FinalElectron'])

    if LeadingJetCheck:
        # MissingET-LeadingJet comparison hists
        HistDict['MissingETLeadingJet']['Particles'].append(ParticleDict['MissingET'])
        HistDict['MissingETLeadingJet']['Particles'].append(ParticleDict['LeadingJet'])

    if LeadingMuonCheck:
        # MissingET-LeadingMuon comparison hists
        HistDict['MissingETLeadingMuon']['Particles'].append(ParticleDict['MissingET'])
        HistDict['MissingETLeadingMuon']['Particles'].append(ParticleDict['LeadingMuon'])
    
    if SubLeadingMuonCheck:
        # MissingET-SubLeadingMuon comparison hists
        HistDict['MissingETSubLeadingMuon']['Particles'].append(ParticleDict['MissingET'])
        HistDict['MissingETSubLeadingMuon']['Particles'].append(ParticleDict['SubLeadingMuon'])        

    
    if LeadingMuonCheck and SubLeadingMuonCheck:
        ParticleDict = funcs.AddParticle('MuonSum', ParticleDict['LeadingMuon']['PID'], ParticleDict['LeadingMuon']['P4']+ParticleDict['SubLeadingMuon']['P4'], ParticleDict)
        # MissingET-MuonSum comparison hists        
        HistDict['MissingETMuonSum']['Particles'].append(ParticleDict['MissingET'])
        HistDict['MissingETMuonSum']['Particles'].append(ParticleDict['MuonSum'])        

    funcs.FillHists(HistDict)

# Writing and closing file
outfile.Write()
outfile.Close()