import Analysis_Funcs as funcs

myTree = funcs.LoadROOT("tag_1_delphes_events.root")

from ROOT import TFile, TH1F

outfile=TFile("GenParticles.root","RECREATE")

Nbins = 200


CountMin = 0
CountMax = 5

# Name = TH1F(Name, Title, NBins, xmin, xmax)

# Number of outgoing electrons (not including beam electrons)
ElectronCountHist = funcs.Histograms('Electron', HistVariables=['Count'], HistLimits=[(0, 10)])

# Number of outgoing muons (not including boson decay muons)
MuonCountHist = funcs.Histograms('Muon', HistVariables=['Count'], HistLimits=[(0, 10)])

# Number of outgoing jets
JetCountHist = funcs.Histograms('Jet', HistVariables=['Count'], HistLimits=[(0, 10)])

FinalElectronHist = funcs.Histograms('FinalElectron')
QSquaredHist = funcs.Histograms('QSquared', HistVariables=['Q2'], HistLimits=[(0, 200000)])

LeadingMuonHist = funcs.Histograms('LeadingMuon')
SubLeadingMuonHist = funcs.Histograms('SubLeadingMuon')

WPlusMuonHist = funcs.Histograms('WPlusMuon')
WMinusMuonHist = funcs.Histograms('WMinusMuon')

AllJetsHist = funcs.Histograms('AllJets', HistVariables=['Eta', 'Phi', 'PT'], HistLimits=[(-10, 10), (-3.5, 3.5), (-200, 300)])
LeadingJetHist = funcs.Histograms('LeadingJet', HistVariables=['Eta', 'Phi', 'PT'], HistLimits=[(-10, 10), (-3.5, 3.5), (-200, 300)])
SubLeadingJetHist = funcs.Histograms('SubLeadingJet', HistVariables=['Eta', 'Phi', 'PT'], HistLimits=[(-10, 10), (-3.5, 3.5), (-200, 300)])

ComparisonVars = ['dEta', 'dPhi', 'dRapidity', 'dR_Eta', 'dR_Rap', 'InvMass']
ComparisonLims = [(-20, 20), (-3.5, 3.5), (-20, 20), (0, 10), (0, 10), (0, 200)]
MuonMuonHist = funcs.Histograms('MuonMuon', HistVariables=ComparisonVars, HistLimits=ComparisonLims)
ElectronLeadingMuonHist = funcs.Histograms('ElectronLeadingMuon', HistVariables=ComparisonVars[0:5], HistLimits=ComparisonLims[0:5])
ElectronSubLeadingMuonHist = funcs.Histograms('ElectronSubLeadingMuon', HistVariables=ComparisonVars[0:5], HistLimits=ComparisonLims[0:5])

ElectronJetHist = funcs.Histograms('ElectronJet', HistVariables=['InvMass'], HistLimits=[(0, 200)])

MissingETHist = funcs.Histograms('MissingET', HistVariables=['Eta', 'Phi', 'MET'], HistLimits=[(-10, 10), (-3.5, 3.5), (0, 500)])
MissingETElectronHist = funcs.Histograms('MissingETElectron', HistVariables=['dPhi'], HistLimits=[(-3.5, 3.5)])
MissingETJetHist = funcs.Histograms('MissingETJet', HistVariables=['dPhi'], HistLimits=[(-3.5, 3.5)])
MissingETMuonHist = funcs.Histograms('MissingETMuon', HistVariables=['dPhi'], HistLimits=[(-3.5, 3.5)])

# Looping through events
for n in range(myTree['Events']):

    EventDict = funcs.ParticleLoop(myTree, n)

    ElectronCountHist[0].Fill(EventDict['Count']['Electron'])
    MuonCountHist[0].Fill(EventDict['Count']['Muon'])
    JetCountHist[0].Fill(EventDict['Count']['Jet'])

    BeamElectron = EventDict['BeamElectron']
    FinalElectron = EventDict['PTSorted']['Electron'][-1][1]

    FinalElectronHist[0].Fill(FinalElectron.Eta)
    FinalElectronHist[1].Fill(FinalElectron.Phi)
    FinalElectronHist[2].Fill(FinalElectron.Rapidity)
    FinalElectronHist[3].Fill(FinalElectron.PT)

    FinalElectron_P = (FinalElectron.E,  FinalElectron.Px, FinalElectron.Py, FinalElectron.Pz)
    BeamElectron_P = (BeamElectron.E,  BeamElectron.Px, BeamElectron.Py, BeamElectron.Pz)  
    q = tuple(x-y for x,y in zip(FinalElectron_P, BeamElectron_P))
    Q2 = abs( q[0]**2 - (q[1]**2 + q[2]**2 + q[3]**2) )
    QSquaredHist[0].Fill(Q2)

    LeadingMuon = EventDict['PTSorted']['Muon'][-1][1]
    SubLeadingMuon = EventDict['PTSorted']['Muon'][-2][1]

    LeadingMuonHist[0].Fill(LeadingMuon.Eta)
    LeadingMuonHist[1].Fill(LeadingMuon.Phi)
    LeadingMuonHist[2].Fill(LeadingMuon.Rapidity)
    LeadingMuonHist[3].Fill(LeadingMuon.PT)

    SubLeadingMuonHist[0].Fill(SubLeadingMuon.Eta)
    SubLeadingMuonHist[1].Fill(SubLeadingMuon.Phi)
    SubLeadingMuonHist[2].Fill(SubLeadingMuon.Rapidity)
    SubLeadingMuonHist[3].Fill(SubLeadingMuon.PT)

    # Same as before but for the leading and subleading muons
    for mu in [LeadingMuon, SubLeadingMuon]:
        
        if mu.PID == 13:
            WMinusMuonHist[0].Fill(mu.Eta)
            WMinusMuonHist[1].Fill(mu.Phi)
            WMinusMuonHist[2].Fill(mu.Rapidity)
            WMinusMuonHist[3].Fill(mu.PT)
        
        if mu.PID == -13:
            WPlusMuonHist[0].Fill(mu.Eta)
            WPlusMuonHist[1].Fill(mu.Phi)
            WPlusMuonHist[2].Fill(mu.Rapidity)
            WPlusMuonHist[3].Fill(mu.PT)   
    

    for i in range(0, len(EventDict['PTSorted']['Jet'])):
        
        AllJetsHist[0].Fill(EventDict['PTSorted']['Jet'][i][1].Eta)
        AllJetsHist[1].Fill(EventDict['PTSorted']['Jet'][i][1].Phi)
        AllJetsHist[2].Fill(EventDict['PTSorted']['Jet'][i][1].PT)

        # Selecting leading jet
        if i == len(EventDict['PTSorted']['Jet']) - 1:
            LeadingJetHist[0].Fill(EventDict['PTSorted']['Jet'][i][1].Eta)
            LeadingJetHist[1].Fill(EventDict['PTSorted']['Jet'][i][1].Phi)
            LeadingJetHist[2].Fill(EventDict['PTSorted']['Jet'][i][1].PT)
        # Selecting subleading jet
        elif i == len(EventDict['PTSorted']['Jet']) - 2:
            SubLeadingJetHist[0].Fill(EventDict['PTSorted']['Jet'][i][1].Eta)
            SubLeadingJetHist[1].Fill(EventDict['PTSorted']['Jet'][i][1].Phi)
            SubLeadingJetHist[2].Fill(EventDict['PTSorted']['Jet'][i][1].PT)

   
    # Comparing the leading muons
    MuonMuon = funcs.Comparison(LeadingMuon, SubLeadingMuon)
    MuonMuonInvMass = funcs.InvMass([LeadingMuon, SubLeadingMuon])

    MuonMuonHist[0].Fill(MuonMuon[0])
    MuonMuonHist[1].Fill(MuonMuon[1])
    MuonMuonHist[2].Fill(MuonMuon[2])
    MuonMuonHist[3].Fill(MuonMuon[3])
    MuonMuonHist[4].Fill(MuonMuon[4])
    MuonMuonHist[5].Fill(MuonMuonInvMass)

    # Comparing the electron and leading muon
    ElectronLeadingMuon = funcs.Comparison(FinalElectron, LeadingMuon)

    ElectronLeadingMuonHist[0].Fill(ElectronLeadingMuon[0])
    ElectronLeadingMuonHist[1].Fill(ElectronLeadingMuon[1])
    ElectronLeadingMuonHist[2].Fill(ElectronLeadingMuon[2])
    ElectronLeadingMuonHist[3].Fill(ElectronLeadingMuon[3])
    ElectronLeadingMuonHist[4].Fill(ElectronLeadingMuon[4])
    
    # Comparing the electron and subleading muon
    ElectronSubLeadingMuon = funcs.Comparison(FinalElectron, SubLeadingMuon)

    ElectronSubLeadingMuonHist[0].Fill(ElectronSubLeadingMuon[0])
    ElectronSubLeadingMuonHist[1].Fill(ElectronSubLeadingMuon[1])
    ElectronSubLeadingMuonHist[2].Fill(ElectronSubLeadingMuon[2])
    ElectronSubLeadingMuonHist[3].Fill(ElectronSubLeadingMuon[3])
    ElectronSubLeadingMuonHist[4].Fill(ElectronSubLeadingMuon[4])

    # Leading jet and electron invariant mass:
    # Commented out, since the GenJet branch doesnt seem to have energy or 
    # momenta leafs. Sub branches like GenJet Pruned do though.
    # ElectronJetInvMass = funcs.InvMass([FinalElectron, EventDict['PTSorted']['Jet'][-1][1]])
    # ElectronJetHist[0].Fill(ElectronJetInvMass)

    # There is only one MissingET entry per event
    MissingET = myTree['Branches']['MissingET'].At(0)       
    
    MissingETHist[0].Fill(MissingET.Eta)
    MissingETHist[1].Fill(MissingET.Phi)
    MissingETHist[2].Fill(MissingET.MET)

    # Comparing phi of MET with other particles:
    MissingETElectron = funcs.Comparison(MissingET, FinalElectron, Eta=False, Rapidity=False, R_Eta=False, R_Rap=False)
    MissingETElectronHist[0].Fill(MissingETElectron[1])
    
    # Commented out, since the GenJet branch doesnt seem to have energy or 
    # momenta leafs. Sub branches like GenJet Pruned do though.
    # MissingETJet = funcs.Comparison(MissingET, LeadingJet, Eta=False, Rapidity=False, R_Eta=False, R_Rap=False)
    # MissingETJetHist[0].Fill(MissingETJet[1])
    MissingETMuon = funcs.Comparison(MissingET, LeadingMuon, Eta=False, Rapidity=False, R_Eta=False, R_Rap=False)
    MissingETMuonHist[0].Fill(MissingETMuon[1])

outfile.Write()
outfile.Close()