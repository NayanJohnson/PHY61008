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

for _, dictionary in HistDict.items():
    dictionary['Particles'] = []
    dictionary['Hists'] = {}


import Analysis_Funcs as funcs

myTree = funcs.LoadROOT("tag_1_delphes_events.root")

from ROOT import TFile, TH1F, TMath

outfile = TFile("GenParticles.root","RECREATE")

Xsec = funcs.GetXSec('tag_1_pythia.log')

# L_int (Data) = 1 [ab-1] = 1000000 [pb-1]
# L_int (MC) = N/Xsec [pb-1]
Scale = 1000000 / (myTree['NEvents']/Xsec)
print('L_int (MC)', myTree['NEvents']/Xsec)
HistDict = funcs.MakeHists(HistDict, Scale)
# Looping through events
for n in range(myTree['NEvents']):

    for _, dictionary in HistDict.items():
        dictionary['Particles'] = []

    # Variables telling the loop what histograms to fill
    FinalElectronCheck = False
    LeadingMuonCheck = False
    SubLeadingMuonCheck = False
    LeadingJetCheck = False
    SubLeadingJetCheck = False

    EventDict = funcs.ParticleLoop(myTree, n)
    ParticleDict = {}

    ParticleDict = funcs.AddParticle('BeamElectron', EventDict['BeamElectron'].PID, EventDict['BeamElectron'].P4(), ParticleDict)
    ParticleDict = funcs.AddParticle('BeamQuark', EventDict['BeamQuark'].PID, EventDict['BeamQuark'].P4(), ParticleDict)

    # Final electron found from sorted list
    numbElectrons = EventDict['Count']['Electrons']
    for i in range(0, numbElectrons):
        Electron = EventDict['PTSorted']['Electron'][-1][1]
        # Checking that there is at least one electron present
        if numbElectrons != 0:
            FinalElectronCheck = True
            ParticleDict = funcs.AddParticle('FinalElectron', Electron.PID, Electron.P4(), ParticleDict)
            HistDict['FinalElectron']['Particles'].append(ParticleDict['FinalElectron'])

    # Leading and SubLeading muon found from sorted list
    numbMuons = EventDict['Count']['Muons']
    for i in range(0, numbMuons):

        # Checking that there is at least one muon present
        if numbMuons != 0:
            Muon = EventDict['PTSorted']['Muon'][i][1]
            # Checking if there is a leading muon
            if i == numbMuons - 1 and 0 <= numbMuons - 1:
                LeadingMuonCheck = True

                ParticleDict = funcs.AddParticle('LeadingMuon', Muon.PID, Muon.P4(), ParticleDict)
                HistDict['LeadingMuon']['Particles'].append(ParticleDict['LeadingMuon'])

            # CHecking if there is a subleading muon
            elif i == numbMuons - 2 and 0 <= numbMuons - 2:
                SubLeadingMuonCheck = True

                ParticleDict = funcs.AddParticle('SubLeadingMuon', Muon.PID, Muon.P4(), ParticleDict)
                HistDict['SubLeadingMuon']['Particles'].append(ParticleDict['SubLeadingMuon'])


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
  
  
    numbJets = EventDict['Count']['Jets']
    for i in range(0, numbJets):
        
        # Checking that there is at least one jet present
        if numbJets != 0:
            Jet = EventDict['PTSorted']['Jet'][i][1]
            # Selecting and checking for the leading jet
            if i == numbJets - 1 and numbJets - 1 >= 0:
                LeadingJetCheck = True
                ParticleDict = funcs.AddParticle('LeadingJet', None, Jet.P4(), ParticleDict)
                HistDict['LeadingJet']['Particles'].append(ParticleDict['LeadingJet'])
                HistDict['AllJets']['Particles'].append(ParticleDict['LeadingJet'])


            # Selecting and checking for the subleading jet
            elif i == numbJets - 2 and numbJets - 2 >= 0:
                SubLeadingJetCheck = True
                ParticleDict = funcs.AddParticle('SubLeadingJet', None, Jet.P4(), ParticleDict)
                HistDict['SubLeadingJet']['Particles'].append(ParticleDict['SubLeadingJet'])
                HistDict['AllJets']['Particles'].append(ParticleDict['SubLeadingJet'])
                            # Selecting and checking for the third jet 
            elif i == numbJets - 3 and numbJets - 3 >= 0:
                ParticleDict = funcs.AddParticle('ThirdJet', None, Jet.P4(), ParticleDict)
                HistDict['ThirdJet']['Particles'].append(ParticleDict['ThirdJet'])
                HistDict['AllJets']['Particles'].append(ParticleDict['ThirdJet'])

            # Selecting and checking for the fourth jet
            elif i == numbJets - 4 and numbJets - 4 >= 0:
                ParticleDict = funcs.AddParticle('FourthJet', None, Jet.P4(), ParticleDict)
                HistDict['FourthJet']['Particles'].append(ParticleDict['FourthJet'])
                HistDict['AllJets']['Particles'].append(ParticleDict['FourthJet'])

            else:
                ParticleDict = funcs.AddParticle(str(i+1)+'Jet', None, Jet.P4(), ParticleDict)
                HistDict['AllJets']['Particles'].append(ParticleDict[str(i+1)+'Jet'])

    # MissingET
    ParticleDict = funcs.AddParticle('MissingET', None, EventDict['MissingET_P'], ParticleDict)
    HistDict['MissingET']['Particles'].append(ParticleDict['MissingET'])

    # Two different Q2 calcs
    if FinalElectronCheck:
        
        HistDict['q_Lepton']['Particles'].append(ParticleDict['FinalElectron'])
        HistDict['q_Lepton']['Particles'].append(ParticleDict['BeamElectron'])

        HistDict['q_eMethod']['Particles'].append(ParticleDict['FinalElectron'])
        HistDict['q_eMethod']['Particles'].append(ParticleDict['BeamElectron'])

    if LeadingJetCheck:

        HistDict['q_Quark']['Particles'].append(ParticleDict['LeadingJet'])
        HistDict['q_Quark']['Particles'].append(ParticleDict['BeamQuark'])


    HistDict['Electrons']['Count'] = numbElectrons
    HistDict['Muons']['Count'] = numbMuons
    HistDict['Jets']['Count'] = numbJets


    if LeadingMuonCheck and SubLeadingMuonCheck:
        # Comparing the leading muons
        HistDict['MuonMuon']['Particles'].append(ParticleDict['LeadingMuon'])
        HistDict['MuonMuon']['Particles'].append(ParticleDict['SubLeadingMuon'])



    if FinalElectronCheck and LeadingMuonCheck:
        # Comparing the electron and leading muon
        HistDict['FinalElectronLeadingMuon']['Particles'].append(ParticleDict['FinalElectron'])
        HistDict['FinalElectronLeadingMuon']['Particles'].append(ParticleDict['LeadingMuon'])

    
    if FinalElectronCheck and SubLeadingMuonCheck:
        # Comparing the electron and subleading muon
        HistDict['FinalElectronSubLeadingMuon']['Particles'].append(ParticleDict['FinalElectron'])
        HistDict['FinalElectronSubLeadingMuon']['Particles'].append(ParticleDict['SubLeadingMuon'])


    if FinalElectronCheck and LeadingJetCheck:
        # Leading jet and electron dPhi and invariant mass:
        HistDict['FinalElectronLeadingJet']['Particles'].append(ParticleDict['FinalElectron'])
        HistDict['FinalElectronLeadingJet']['Particles'].append(ParticleDict['LeadingJet'])

    if LeadingMuonCheck and LeadingJetCheck:
        HistDict['LeadingMuonLeadingJet']['Particles'].append(ParticleDict['LeadingMuon'])
        HistDict['LeadingMuonLeadingJet']['Particles'].append(ParticleDict['LeadingJet'])

    if SubLeadingMuonCheck and LeadingJetCheck:
        HistDict['SubLeadingMuonLeadingJet']['Particles'].append(ParticleDict['SubLeadingMuon'])
        HistDict['SubLeadingMuonLeadingJet']['Particles'].append(ParticleDict['LeadingJet'])



    # Comparing phi of MET with other particles:

    if FinalElectronCheck:
        HistDict['MissingETFinalElectron']['Particles'].append(ParticleDict['MissingET'])
        HistDict['MissingETFinalElectron']['Particles'].append(ParticleDict['FinalElectron'])

    if LeadingJetCheck:
        HistDict['MissingETLeadingJet']['Particles'].append(ParticleDict['MissingET'])
        HistDict['MissingETLeadingJet']['Particles'].append(ParticleDict['LeadingJet'])

    if LeadingMuonCheck:
        HistDict['MissingETLeadingMuon']['Particles'].append(ParticleDict['MissingET'])
        HistDict['MissingETLeadingMuon']['Particles'].append(ParticleDict['LeadingMuon'])
    
    if SubLeadingMuonCheck:

        HistDict['MissingETSubLeadingMuon']['Particles'].append(ParticleDict['MissingET'])
        HistDict['MissingETSubLeadingMuon']['Particles'].append(ParticleDict['SubLeadingMuon'])        

    
    if LeadingMuonCheck and SubLeadingMuonCheck:
        ParticleDict = funcs.AddParticle('MuonSum', ParticleDict['LeadingMuon']['PID'], ParticleDict['LeadingMuon']['P4']+ParticleDict['SubLeadingMuon']['P4'], ParticleDict)
        HistDict['MissingETMuonSum']['Particles'].append(ParticleDict['MissingET'])
        HistDict['MissingETMuonSum']['Particles'].append(ParticleDict['MuonSum'])        

    funcs.FillHists(HistDict)

# Writing and closing file
outfile.Write()
outfile.Close()