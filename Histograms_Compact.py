import Analysis_Funcs as funcs

myTree = funcs.LoadROOT("tag_1_delphes_events.root")

from ROOT import TFile, TH1F

outfile=TFile("GenParticles.root","RECREATE")

Nbins = 200


CountMin = 0
CountMax = 5

# Name = funcs.Histogram(name, Nbins=200, HistVariables=['Eta', 'Phi', 'Rapidity', 'PT'], HistLimits=[(-10, 10), (-3.5, 3.5), (-10, 10), (-200, 300)])

# Number of outgoing electrons
ElectronCountHist = funcs.Histograms('Electron', HistVariables=['Count'], HistLimits=[(0, 10)])

# Number of outgoing muons
MuonCountHist = funcs.Histograms('Muon', HistVariables=['Count'], HistLimits=[(0, 10)])

# Number of outgoing jets
JetCountHist = funcs.Histograms('Jet', HistVariables=['Count'], HistLimits=[(0, 10)])

# Outgoing Beam electron and Q2
FinalElectronHist = funcs.Histograms('FinalElectron')
QSquaredHist = funcs.Histograms('QSquared', HistVariables=['Q2'], HistLimits=[(0, 200000)])

# Boson Muons by leading and subleading
LeadingMuonHist = funcs.Histograms('LeadingMuon')
SubLeadingMuonHist = funcs.Histograms('SubLeadingMuon')

# Boson Muons by charge
WPlusMuonHist = funcs.Histograms('WPlusMuon')
WMinusMuonHist = funcs.Histograms('WMinusMuon')

# Jets
AllJetsHist = funcs.Histograms('AllJets')
LeadingJetHist = funcs.Histograms('LeadingJet')
SubLeadingJetHist = funcs.Histograms('SubLeadingJet')
ThirdJetHist = funcs.Histograms('ThirdJet')
FourthJetHist  = funcs.Histograms('FourthJet')

# Various comparisons
ComparisonVars = ['dEta', 'dPhi', 'dRapidity', 'dR_Eta', 'dR_Rap', 'InvMass']
ComparisonLims = [(-20, 20), (-3.5, 3.5), (-20, 20), (0, 10), (0, 10), (0, 800)]
MuonMuonHist = funcs.Histograms('MuonMuon', HistVariables=ComparisonVars, HistLimits=ComparisonLims)
ElectronLeadingMuonHist = funcs.Histograms('ElectronLeadingMuon', HistVariables=ComparisonVars[0:5], HistLimits=ComparisonLims[0:5])
ElectronSubLeadingMuonHist = funcs.Histograms('ElectronSubLeadingMuon', HistVariables=ComparisonVars[0:5], HistLimits=ComparisonLims[0:5])

# Invariant mass of electron and beam jet
ElectronJetHist = funcs.Histograms('ElectronJet', HistVariables=['InvMass'], HistLimits=[(0, 800)])

# MissingET hists and dPhi comparisons
MissingETHist = funcs.Histograms('MissingET', HistVariables=['Eta', 'Phi', 'Rapidity', 'PT', 'MET'], HistLimits=[(-10, 10), (-3.5, 3.5), (-10, 10), (-200, 300), (0, 500)])
MissingETElectronHist = funcs.Histograms('MissingETElectron', HistVariables=['dPhi'], HistLimits=[(-3.5, 3.5)])
MissingETJetHist = funcs.Histograms('MissingETJet', HistVariables=['dPhi'], HistLimits=[(-3.5, 3.5)])
MissingETLeadingMuonHist = funcs.Histograms('MissingETLeadingMuon', HistVariables=['dPhi'], HistLimits=[(-3.5, 3.5)])
MissingETSubLeadingMuonHist = funcs.Histograms('MissingETSubLeadingMuon', HistVariables=['dPhi'], HistLimits=[(-3.5, 3.5)])
MissingETMuonSumHist = funcs.Histograms('MissingETMuonSum', HistVariables=['dPhi'], HistLimits=[(-3.5, 3.5)])

# Looping through events
for n in range(myTree['Events']):

    EventDict = funcs.ParticleLoop(myTree, n)

    ElectronCountHist[0].Fill(EventDict['Count']['Electron'])
    MuonCountHist[0].Fill(EventDict['Count']['Muon'])
    JetCountHist[0].Fill(EventDict['Count']['Jet'])

    BeamElectron = EventDict['BeamElectron']
    BeamElectron_P = BeamElectron.P4()
    FinalElectron = EventDict['PTSorted']['Electron'][-1][1]
    FinalElectron_P = FinalElectron.P4()

    FinalElectronHist[0].Fill(FinalElectron_P.Eta())
    FinalElectronHist[1].Fill(FinalElectron_P.Phi())
    FinalElectronHist[2].Fill(FinalElectron_P.Rapidity())
    FinalElectronHist[3].Fill(FinalElectron_P.Pt())


    q = FinalElectron_P - BeamElectron_P

    # For some reason Q2 is always negative?
    Q2 = abs(q.Mag2())
    QSquaredHist[0].Fill(Q2)

    # Leading and SubLeading muon found from sorted list
    LeadingMuon = EventDict['PTSorted']['Muon'][-1][1]
    LeadingMuon_P = LeadingMuon.P4()
    SubLeadingMuon = EventDict['PTSorted']['Muon'][-2][1]
    SubLeadingMuon_P = SubLeadingMuon.P4()

    LeadingMuonHist[0].Fill(LeadingMuon_P.Eta())
    LeadingMuonHist[1].Fill(LeadingMuon_P.Phi())
    LeadingMuonHist[2].Fill(LeadingMuon_P.Rapidity())
    LeadingMuonHist[3].Fill(LeadingMuon_P.Pt())

    SubLeadingMuonHist[0].Fill(SubLeadingMuon_P.Eta())
    SubLeadingMuonHist[1].Fill(SubLeadingMuon_P.Phi())
    SubLeadingMuonHist[2].Fill(SubLeadingMuon_P.Rapidity())
    SubLeadingMuonHist[3].Fill(SubLeadingMuon_P.Pt())

    # Leading and SubLeading muons will always be from the W bosons 
    # (in this process) so I seperate them by charge to determine which
    # boson they came from
    for mu in [LeadingMuon, SubLeadingMuon]:
        
        if mu.PID == 13:
            WMinusMuonHist[0].Fill(mu.P4().Eta())
            WMinusMuonHist[1].Fill(mu.P4().Phi())
            WMinusMuonHist[2].Fill(mu.P4().Rapidity())
            WMinusMuonHist[3].Fill(mu.P4().Pt())
        
        if mu.PID == -13:
            WPlusMuonHist[0].Fill(mu.P4().Eta())
            WPlusMuonHist[1].Fill(mu.P4().Phi())
            WPlusMuonHist[2].Fill(mu.P4().Rapidity())
            WPlusMuonHist[3].Fill(mu.P4().Pt())   
    

    numbJets = len(EventDict['PTSorted']['Jet'])
    for i in range(0, numbJets):
        
        AllJetsHist[0].Fill(EventDict['PTSorted']['Jet'][i][1].P4().Eta())
        AllJetsHist[1].Fill(EventDict['PTSorted']['Jet'][i][1].P4().Phi()) 
        AllJetsHist[2].Fill(EventDict['PTSorted']['Jet'][i][1].P4().Rapidity())    
        AllJetsHist[3].Fill(EventDict['PTSorted']['Jet'][i][1].P4().Pt())

        # Selecting leading jet
        if i == numbJets - 1 and numbJets - 1 >= 0:
            LeadingJet_P = EventDict['PTSorted']['Jet'][i][1].P4()
            LeadingJetHist[0].Fill(LeadingJet_P.Eta())
            LeadingJetHist[1].Fill(LeadingJet_P.Phi())
            LeadingJetHist[2].Fill(LeadingJet_P.Rapidity())
            LeadingJetHist[3].Fill(LeadingJet_P.Pt())

        # Selecting subleading jet
        elif i == numbJets - 2 and numbJets - 2 >= 0:
            SubLeadingJet_P = EventDict['PTSorted']['Jet'][i][1].P4()
            SubLeadingJetHist[0].Fill(SubLeadingJet_P.Eta())
            SubLeadingJetHist[1].Fill(SubLeadingJet_P.Phi())
            SubLeadingJetHist[2].Fill(SubLeadingJet_P.Rapidity())
            SubLeadingJetHist[3].Fill(SubLeadingJet_P.Pt())
        
        elif i == numbJets - 3 and numbJets - 3 >= 0:
            ThirdJet_P = EventDict['PTSorted']['Jet'][i][1].P4()
            ThirdJetHist[0].Fill(ThirdJet_P.Eta())
            ThirdJetHist[1].Fill(ThirdJet_P.Phi())
            ThirdJetHist[2].Fill(ThirdJet_P.Rapidity())
            ThirdJetHist[3].Fill(ThirdJet_P.Pt())
        
        elif i == numbJets - 4 and numbJets - 4 >= 0:
            FourthJet_P = EventDict['PTSorted']['Jet'][i][1].P4()
            FourthJetHist[0].Fill(FourthJet_P.Eta())
            FourthJetHist[1].Fill(FourthJet_P.Phi())
            FourthJetHist[2].Fill(FourthJet_P.Rapidity())
            FourthJetHist[3].Fill(FourthJet_P.Pt())
        

   
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

    # Comparing the electron and leading muon
    ElectronLeadingMuon = funcs.Comparison(FinalElectron_P, LeadingMuon_P)

    ElectronLeadingMuonHist[0].Fill(ElectronLeadingMuon[0])
    ElectronLeadingMuonHist[1].Fill(ElectronLeadingMuon[1])
    ElectronLeadingMuonHist[2].Fill(ElectronLeadingMuon[2])
    ElectronLeadingMuonHist[3].Fill(ElectronLeadingMuon[3])
    ElectronLeadingMuonHist[4].Fill(ElectronLeadingMuon[4])
    
    # Comparing the electron and subleading muon
    ElectronSubLeadingMuon = funcs.Comparison(FinalElectron_P, SubLeadingMuon_P)

    ElectronSubLeadingMuonHist[0].Fill(ElectronSubLeadingMuon[0])
    ElectronSubLeadingMuonHist[1].Fill(ElectronSubLeadingMuon[1])
    ElectronSubLeadingMuonHist[2].Fill(ElectronSubLeadingMuon[2])
    ElectronSubLeadingMuonHist[3].Fill(ElectronSubLeadingMuon[3])
    ElectronSubLeadingMuonHist[4].Fill(ElectronSubLeadingMuon[4])

    # Leading jet and electron invariant mass:
    ElectronJetInvMass = (FinalElectron_P + LeadingJet_P).M()
    ElectronJetHist[0].Fill(ElectronJetInvMass)

    # MissingE
    MissingET_P = EventDict['MissingET_P']    
    
    # In the detector, only the transverse components can be resolved
    MissingETHist[0].Fill(MissingET_P.Eta())
    MissingETHist[1].Fill(MissingET_P.Phi())
    MissingETHist[2].Fill(MissingET_P.Rapidity())
    MissingETHist[3].Fill(MissingET_P.Pt())
    MissingETHist[4].Fill(MissingET_P.Et())

    # Comparing phi of MET with other particles:
    MissingETElectron = funcs.Comparison(MissingET_P, FinalElectron_P, Eta=False, Rapidity=False, R_Eta=False, R_Rap=False)
    MissingETElectronHist[0].Fill(MissingETElectron[1])

    MissingETJet = funcs.Comparison(MissingET_P, LeadingJet_P, Eta=False, Rapidity=False, R_Eta=False, R_Rap=False)
    MissingETJetHist[0].Fill(MissingETJet[1])

    MissingETLeadingMuon = funcs.Comparison(MissingET_P, LeadingMuon_P, Eta=False, Rapidity=False, R_Eta=False, R_Rap=False)
    MissingETLeadingMuonHist[0].Fill(MissingETLeadingMuon[1])
    MissingETSubLeadingMuon = funcs.Comparison(MissingET_P, SubLeadingMuon_P, Eta=False, Rapidity=False, R_Eta=False, R_Rap=False)
    MissingETSubLeadingMuonHist[0].Fill(MissingETSubLeadingMuon[1])
    MissingETMuonSum = funcs.Comparison(MissingET_P, MuonSum, Eta=False, Rapidity=False, R_Eta=False, R_Rap=False)
    MissingETMuonSumHist[0].Fill(MissingETMuonSum[1])

# Writing and closing file
outfile.Write()
outfile.Close()