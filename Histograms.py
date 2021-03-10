import Classes
import Analysis_Funcs as funcs

myTree = funcs.LoadROOT("tag_1_delphes_events.root")

from ROOT import TFile, TH1F, TMath

outfile = TFile("GenParticles.root","RECREATE")

HistDict = {
    'Electrons'     :   {
        'vars'      :   ['Count']
    }

    'Muons'         :   {
        'vars'      :   ['Count']
    }

    'Jet'           :   {
        'vars'      :   ['Count']
    }

    'FinalElectron' :   {
        'vars'      :   ['Eta', 'Phi', 'Rapidity', 'PT']
    }

    'LeadingMuon'   :   {
        'vars'      :   ['Eta', 'Phi', 'Rapidity', 'PT']
    }

    'SubLeadingMuon':   {
        'vars'      :   ['Eta', 'Phi', 'Rapidity', 'PT']
    }

    'WPlusMuon'     :   {
        'vars'      :   ['Eta', 'Phi', 'Rapidity', 'PT']
    }

    'WMinusMuon'    :   {
        'vars'      :   ['Eta', 'Phi', 'Rapidity', 'PT']
    }

    'AllJets'       :   {
        'vars'      :   ['Eta', 'Phi', 'Rapidity', 'PT']
    }

    'LeadingJet'    :   {
        'vars'      :   ['Eta', 'Phi', 'Rapidity', 'PT']
    }

    'SubLeadingJet' :   {
        'vars'      :   ['Eta', 'Phi', 'Rapidity', 'PT']
    }

    'ThirdJet'      :   {
        'vars'      :   ['Eta', 'Phi', 'Rapidity', 'PT']
    }

    'MissingET'     :   {
        'vars'      :   ['Eta', 'Phi', 'Rapidity', 'PT']
    }

    'QSquared_Lepton'      
                    :   {
        'vars'      :   ['Q2']
    }

    'QSquared_Quark'      
                    :   {
        'vars'      :   ['Q2']
    }

    'QSquared_eMethod'      
                    :   {
        'vars'      :   ['Q2']
    }

    'MuonMuon'      :   {
        'vars'      :   ['dEta', 'dPhi', 'dRapidity', 'dR_Eta', 'dR_Rap', 'InvMass']
    }

    'FinalElectronLeadingMuon'  
                    :   {
        'vars'      :   ['dEta', 'dPhi', 'dRapidity', 'dR_Eta', 'dR_Rap', 'InvMass']
    }
    
    'FinalElectronSubLeadingMuon'
                    :   {
        'vars'      :   ['dEta', 'dPhi', 'dRapidity', 'dR_Eta', 'dR_Rap', 'InvMass']
    }

    'ElectronJet'   :   {
        'vars'      :   ['dEta', 'dPhi', 'dRapidity', 'dR_Eta', 'dR_Rap', 'InvMass']
    }

    'MissingETFinalElectron'
                    :   {
        'vars'      :   ['dPhi', 'InvMass']
    }

    'MissingETJet'  :   {
        'vars'      :   ['dPhi', 'InvMass']
    }

    'MissingETLeadingMuon'
                    :   {
        'vars'      :   ['dPhi', 'InvMass']
    }

    'MissingETSubLeadingMuon'
                    :   {
        'vars'      :   ['dPhi', 'InvMass']
    }

    'MissingETMuonSum'
                    :   {
        'vars'      :   ['dPhi', 'InvMass']
    }
}




Histograms = Classes.Historgram.MakeHists(HistDict)

# Looping through events
for n in range(myTree['Events']):

    for _, dictionary in HistDict:
        dictionary['particles'] = []

    # Variables telling the loop what histograms to fill
    FinalElectronCheck = False
    LeadingMuonCheck = False
    SubLeadingMuonCheck = False
    LeadingJetCheck = False
    SubLeadingJetCheck = False

    EventDict = funcs.ParticleLoop(myTree, n)
    ParticleDict = {}

    ParticleDict = funcs.AddParticle('BeamElectron', EventDict['BeamElectron'], ParticleDict)
    ParticleDict = funcs.AddParticle('BeamQuark', EventDict['BeamQuark'], ParticleDict)

    # Final electron found from sorted list
    numbElectrons = EventDict['Count']['Electrons']
    for i in range(0, numbElectrons):

        # Checking that there is at least one electron present
        if numbElectrons != 0:
            FinalElectronCheck = True
            FinalElectron = EventDict['PTSorted']['Electron'][-1][1]
            ParticleDict = funcs.AddParticle('FinalElectron', EventDict['PTSorted']['Electron'][-1][1], ParticleDict)
            HistDict['FinalElectron']['Particles'].append(ParticleDict['FinalElectron'])

    # Leading and SubLeading muon found from sorted list
    numbMuons = EventDict['Count']['Muons']
    for i in range(0, numbMuons):

        # Checking that there is at least one muon present
        if numbMuons != 0:

            # Checking if there is a leading muon
            if i == numbMuons - 1 and 0 <= numbMuons - 1:
                LeadingMuonCheck = True

                ParticleDict = funcs.AddParticle('LeadingMuon', EventDict['PTSorted']['Muon'][i][1], ParticleDict)
                HistDict['LeadingMuon']['Particles'].append(ParticleDict['LeadingMuon'])

            # CHecking if there is a subleading muon
            elif i == numbMuons - 2 and 0 <= numbMuons - 2:
                SubLeadingMuonCheck = True

                ParticleDict = funcs.AddParticle('SubLeadingMuon', EventDict['PTSorted']['Muon'][i][1], ParticleDict)
                HistDict['SubLeadingMuon']['Particles'].append(ParticleDict['SubLeadingMuon'])


    # Leading and SubLeading muons will always be from the W bosons 
    # (in this process) so I seperate them by charge to determine which
    # boson they came from

    # Will only run if that muon is present
    if LeadingMuonCheck:    
        if ParticleDict['LeadingMuon']['PID'] == 13:
            HistDict['WMinusMuon']['Particles'].append(ParticleDict['LeadingMuon'])

        elif ParticleDict['LeadingMuon']['PID'] == -13:
            HistDict['WPlusMuonHist']['Particles'].append(ParticleDict['LeadingMuon'])

    if SubLeadingMuonCheck:  
        if ParticleDict['SubLeadingMuon']['PID'] == 13:
            HistDict['WMinusMuon']['Particles'].append(ParticleDict['SubLeadingMuon'])
        
        elif ParticleDict['SubLeadingMuon']['PID'] == -13:
            HistDict['WPlusMuonHist']['Particles'].append(ParticleDict['SubLeadingMuon'])
  
  
    numbJets = EventDict['Count']['Jets']
    for i in range(0, numbJets):
        
        # Checking that there is at least one jet present
        if numbJets != 0:

            # Selecting and checking for the leading jet
            if i == numbJets - 1 and numbJets - 1 >= 0:
                LeadingJetCheck = True
                ParticleDict = funcs.AddParticle('LeadingJet', EventDict['PTSorted']['Jet'][i][1], ParticleDict)
                HistDict['LeadingJet']['Particles'].append(ParticleDict['LeadingJet'])
                HistDict['AllJets']['Particles'].append(ParticleDict['LeadingJet'])


            # Selecting and checking for the subleading jet
            elif i == numbJets - 2 and numbJets - 2 >= 0:
                SubLeadingJetCheck = True
                ParticleDict = funcs.AddParticle('SubLeadingJet', EventDict['PTSorted']['Jet'][i][1], ParticleDict)
                HistDict['SubLeadingJet']['Particles'].append(ParticleDict['SubLeadingJet'])
                HistDict['AllJets']['Particles'].append(ParticleDict['SubLeadingJet'])
                            # Selecting and checking for the third jet 
            elif i == numbJets - 3 and numbJets - 3 >= 0:
                ParticleDict = funcs.AddParticle('ThirdJet', EventDict['PTSorted']['Jet'][i][1], ParticleDict)
                HistDict['ThirdJet']['Particles'].append(ParticleDict['ThirdJet'])
                HistDict['AllJets']['Particles'].append(ParticleDict['ThirdJet'])

            # Selecting and checking for the fourth jet
            elif i == numbJets - 4 and numbJets - 4 >= 0:
                ParticleDict = funcs.AddParticle('FourthJet', EventDict['PTSorted']['Jet'][i][1], ParticleDict)
                HistDict['FourthJet']['Particles'].append(ParticleDict['FourthJet'])
                HistDict['AllJets']['Particles'].append(ParticleDict['FourthJet'])

            else:
                ParticleDict = funcs.AddParticle(str(i+1)+'Jet', EventDict['PTSorted']['Jet'][i][1], ParticleDict)
                HistDict['AllJets']['Particles'].append(ParticleDict[str(i+1)+'Jet'])


    # Two different Q2 calcs
    if FinalElectronCheck:
        
        HistDict['QSquared_Electron']['Particles'].append(ParticleDict['FinalElectron'])
        HistDict['QSquared_Electron']['Particles'].append(ParticleDict['BeamElectron'])


        q_electron = FinalElectron_P - BeamElectron_P
        # For some reason Q2 is always negative?
        Q2_electron = abs(q_electron.Mag2())
        QSquaredHist[0].Fill(Q2_electron)

        HistDict['QSquared_eMethod']['Particles'].append(ParticleDict['FinalElectron'])
        HistDict['QSquared_eMethod']['Particles'].append(ParticleDict['BeamElectron'])

        # Implimenting the e method
        Q2_eMethod = abs(2*BeamElectron_P.E()*FinalElectron_P.E()*(1 - TMath.Cos(FinalElectron_P.Theta())))
        QSquaredHist[2].Fill(Q2_eMethod)

    if LeadingJetCheck:

        HistDict['QSquared_Electron']['Particles'].append(ParticleDict['FinalElectron'])
        HistDict['QSquared_Electron']['Particles'].append(ParticleDict['BeamElectron'])

        q_quark = LeadingJet_P - BeamQuark_P
        # For some reason Q2 is always negative?
        Q2_quark = abs(q_quark.Mag2())
        QSquaredHist[1].Fill(Q2_quark)


    ElectronCountHist[0].Fill(numbElectrons)
    MuonCountHist[0].Fill(numbMuons)
    JetCountHist[0].Fill(numbJets)

    if LeadingMuonCheck and SubLeadingMuonCheck:
   
        # Comparing the leading muons
        MuonMuon = funcs.Comparison(LeadingMuon_P, SubLeadingMuon_P)
        MuonSum = LeadingMuon_P + SubLeadingMuon_P
        MuonMuonInvMass = MuonSum.M()

        MuonMuonHist[0].Fill(MuonMuon[0])
        MuonMuonHist[1].Fill(MuonMuon[1])
        MuonMuonHist[2].Fill(MuonMuon[2])
        MuonMuonHist[3].Fill(MuonMuon[3])
        MuonMuonHist[4].Fill(MuonMuon[4])
        MuonMuonHist[5].Fill(MuonMuonInvMass)

    if FinalElectronCheck and LeadingMuonCheck:
        # Comparing the electron and leading muon
        ElectronLeadingMuon = funcs.Comparison(FinalElectron_P, LeadingMuon_P)

        ElectronLeadingMuonHist[0].Fill(ElectronLeadingMuon[0])
        ElectronLeadingMuonHist[1].Fill(ElectronLeadingMuon[1])
        ElectronLeadingMuonHist[2].Fill(ElectronLeadingMuon[2])
        ElectronLeadingMuonHist[3].Fill(ElectronLeadingMuon[3])
        ElectronLeadingMuonHist[4].Fill(ElectronLeadingMuon[4])
    
    if FinalElectronCheck and SubLeadingMuonCheck:
        # Comparing the electron and subleading muon
        ElectronSubLeadingMuon = funcs.Comparison(FinalElectron_P, SubLeadingMuon_P)

        ElectronSubLeadingMuonHist[0].Fill(ElectronSubLeadingMuon[0])
        ElectronSubLeadingMuonHist[1].Fill(ElectronSubLeadingMuon[1])
        ElectronSubLeadingMuonHist[2].Fill(ElectronSubLeadingMuon[2])
        ElectronSubLeadingMuonHist[3].Fill(ElectronSubLeadingMuon[3])
        ElectronSubLeadingMuonHist[4].Fill(ElectronSubLeadingMuon[4])

    if FinalElectronCheck and LeadingJetCheck:
        # Leading jet and electron dPhi and invariant mass:
        ElectronJet = funcs.Comparison(FinalElectron_P, LeadingJet_P)
        ElectronJetInvMass = (FinalElectron_P + LeadingJet_P).M()
        ElectronJetHist[0].Fill(ElectronJet[1])
        ElectronJetHist[1].Fill(ElectronJetInvMass)

    # MissingET
    MissingET_P = EventDict['MissingET_P']    
    
    # In the detector, only the transverse components can be resolved
    MissingETHist[0].Fill(MissingET_P.Eta())
    MissingETHist[1].Fill(MissingET_P.Phi())
    MissingETHist[2].Fill(MissingET_P.Rapidity())
    MissingETHist[3].Fill(MissingET_P.Pt())
    MissingETHist[4].Fill(MissingET_P.Et())

    # Comparing phi of MET with other particles:

    if FinalElectronCheck:
        MissingETElectron = funcs.Comparison(MissingET_P, FinalElectron_P, Eta=False, Rapidity=False, R_Eta=False, R_Rap=False)
        MissingETElectronHist[0].Fill(MissingETElectron[1])

    if LeadingJetCheck:
        MissingETJet = funcs.Comparison(MissingET_P, LeadingJet_P, Eta=False, Rapidity=False, R_Eta=False, R_Rap=False)
        MissingETJetHist[0].Fill(MissingETJet[1])

    if LeadingMuonCheck:
        MissingETLeadingMuon = funcs.Comparison(MissingET_P, LeadingMuon_P, Eta=False, Rapidity=False, R_Eta=False, R_Rap=False)
        MissingETLeadingMuonHist[0].Fill(MissingETLeadingMuon[1])
    
    if SubLeadingMuonCheck:
        MissingETSubLeadingMuon = funcs.Comparison(MissingET_P, SubLeadingMuon_P, Eta=False, Rapidity=False, R_Eta=False, R_Rap=False)
        MissingETSubLeadingMuonHist[0].Fill(MissingETSubLeadingMuon[1])
    
    if LeadingMuonCheck and SubLeadingMuonCheck:
        MissingETMuonSum = funcs.Comparison(MissingET_P, MuonSum, Eta=False, Rapidity=False, R_Eta=False, R_Rap=False)
        MissingETMuonSumHist[0].Fill(MissingETMuonSum[1])

# Writing and closing file
outfile.Write()
outfile.Close()