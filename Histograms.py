from ROOT import gSystem, gInterpreter

# Path of Delphes directory 
# Personal laptop path
gSystem.AddDynamicPath("/home/nayan/MG5_aMC_v2_8_2/Delphes/")
# Cluster path
# ROOT.gSystem.AddDynamicPath("/home/johnson/MG5_aMC_v2_4_3/Delphes/")
gSystem.Load("libDelphes")

gInterpreter.Declare('#include "classes/DelphesClasses.h"')
gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')

filename = "tag_1_delphes_events.root"
# filename = "Electron/tag_1_pythia_events.root"
# filename = "Neutrino/tag_1_pythia_events..root"

from ROOT import TChain, ExRootTreeReader 

# Create chain of root trees 
chain = TChain("Delphes")
chain.Add(filename)

# Create object of class ExRootTreeReader
myTree = ExRootTreeReader(chain)
Events = myTree.GetEntries()

# Get pointers to branches used in this analysis
branchParticle = myTree.UseBranch("Particle")
branchGenJets = myTree.UseBranch("GenJet")
branchMissingET = myTree.UseBranch("MissingET")

from ROOT import TMath

def comparison(A, B, Eta=True, Phi=True, Rapidity=True, R_Eta=True, R_Rap=True ):
    '''
    Given two particles will compute dEta, dPhi, dRapidty and two different versions of dR (one using dEta and one using dRapidity)
    A, B = Particle branch
    Eta, Phi, Rapidity, R = what comparisons to compute
    '''
    
    # Default values
    dEta, dPhi, dRapidity, dR_Eta, dR_Rap = 'NA', 'NA', 'NA', 'NA', 'NA'
    Pi = TMath.Pi()
    
    
    if Eta:
        dEta = A.Eta - B.Eta
        
    if Phi:
        dPhi = A.Phi - B.Phi
    
        # Constraining dPhi between -2Pi and 2Pi
        if dPhi < -Pi:
            dPhi = dPhi + 2*Pi
        elif dPhi > Pi:
            dPhi = dPhi - 2*Pi
    
    if Rapidity:
        dRapidity = A.Rapidity - B.Rapidity
    
    if R_Eta and Phi and Eta:
        dR_Eta = (dPhi**2 + dEta**2)**0.5
        
    if R_Rap and Phi and Rapidity:
        dR_Rap = (dPhi**2 + dRapidity**2)**0.5
    
    return (dEta, dPhi, dRapidity, dR_Eta, dR_Rap)


from ROOT import TFile, TH1F, TBranch

outfile=TFile("GenParticles.root","RECREATE")

Nbins = 200

CountMin = 0
CountMax = 5

# Name = TH1F(Name, Title, NBins, xmin, xmax)

# Number of outgoing electrons (not including beam electrons)
ElectronCount = TH1F("ElectronCount", "ElectronCount;Number per Event;Frequency", Nbins, CountMin, CountMax)

# Number of outgoing muons (not including boson decay muons)
MuonCount = TH1F("MuonCount", "MuonCount;Number per Event;Frequency", Nbins, CountMin, CountMax)

# Number of outgoing jets
JetCount = TH1F("JetCount", "JetCount;Number per Event;Frequency", Nbins, CountMin, 10)

EtaMin = -10
EtaMax = 10
PhiMin = -3.5
PhiMax = 3.5
RapidityMin = -20
RapidityMax = 20
PTMin = -200
PTMax = 300

# Outgoing beam electrons
FinalElectron_Eta = TH1F("FinalElectron_Eta", "FinalElectron_Eta;Eta;Frequency", Nbins, EtaMin, EtaMax)
FinalElectron_Phi = TH1F("FinalElectron_Phi", "FinalElectron_Phi;Phi;Frequency", Nbins, PhiMin, PhiMax)
FinalElectron_Rapidity = TH1F("FinalElectron_Rapidity", "FinalElectron_Rapidity;Rapidity;Frequency", Nbins, RapidityMin, RapidityMax)
FinalElectron_PT = TH1F("FinalElectron_PT", "FinalElectron_PT;PT;Frequency", Nbins, PTMin, PTMax)

# Outgoing leading boson muons
Muon_Leading_Eta = TH1F("Muon_Leading_Eta", "Muon_Leading_Eta;Eta;Frequency", Nbins, EtaMin, EtaMax)
Muon_Leading_Phi = TH1F("Muon_Leading_Phi", "Muon_Leading_Phi;Phi;Frequency", Nbins, PhiMin, PhiMax)
Muon_Leading_Rapidity = TH1F("Muon_Leading_Rapidity", "Muon_Leading_Rapidity;Rapidity;Frequency", Nbins, RapidityMin, RapidityMax)
Muon_Leading_PT = TH1F("Muon_Leading_PT", "Muon_Leading_PT;PT;Frequency", Nbins, PTMin, PTMax)

# Outgoing subleading boson muons
Muon_SubLeading_Eta = TH1F("Muon_SubLeading_Eta", "Muon_SubLeading_Eta;Eta;Frequency", Nbins, EtaMin, EtaMax)
Muon_SubLeading_Phi = TH1F("Muon_SubLeading_Phi", "Muon_SubLeading_Phi;Phi;Frequency", Nbins, PhiMin, PhiMax)
Muon_SubLeading_Rapidity = TH1F("Muon_SubLeading_Rapidity", "Muon_SubLeading_Rapidity;Rapidity;Frequency", Nbins, RapidityMin, RapidityMax)
Muon_SubLeading_PT = TH1F("Muon_SubLeading_PT", "Muon_SubLeading_PT;PT;Frequency", Nbins, PTMin, PTMax)

# Outgoing mu- from bosons
BosonMuon_Minus_Eta = TH1F("BosonMuon_Minus_Eta", "BosonMuon_Minus_Eta;Eta;Frequency", Nbins, EtaMin, EtaMax)
BosonMuon_Minus_Phi = TH1F("BosonMuon_Minus_Phi", "BosonMuon_Minus_Phi;Eta;Frequency", Nbins, PhiMin, PhiMax)
BosonMuon_Minus_Rapidity= TH1F("BosonMuon_Minus_Rapidity", "BosonMuon_Minus_Rapidity;Eta;Frequency", Nbins, RapidityMin, RapidityMax)
BosonMuon_Minus_PT = TH1F("BosonMuon_Minus_PT", "BosonMuon_Minus_PT;Eta;Frequency", Nbins, PTMin, PTMax)

# Outgoing mu+ from bosons
BosonMuon_Plus_Eta = TH1F("BosonMuon_Plus_Eta", "BosonMuon_Plus_Eta;Eta;Frequency", Nbins, EtaMin, EtaMax)
BosonMuon_Plus_Phi = TH1F("BosonMuon_Plus_Phi", "BosonMuon_Plus_Phi;Eta;Frequency", Nbins, PhiMin, PhiMax)
BosonMuon_Plus_Rapidity = TH1F("BosonMuon_Plus_Rapidity", "BosonMuon_Plus_Rapidity;Eta;Frequency", Nbins, RapidityMin, RapidityMax)
BosonMuon_Plus_PT = TH1F("BosonMuon_Plus_PT", "BosonMuon_Plus_PT;Eta;Frequency", Nbins, PTMin, PTMax) 

# Outgoing mu- with boson mu excluded
NonBosonMuon_Minus_Eta = TH1F("NonBosonMuon_Minus_Eta", "NonBosonMuon_Minus_Eta;Eta;Frequency", Nbins, EtaMin, EtaMax)
NonBosonMuon_Minus_Phi = TH1F("NonBosonMuon_Minus_Phi", "NonBosonMuon_Minus_Phi;Eta;Frequency", Nbins, PhiMin, PhiMax)
NonBosonMuon_Minus_Rapidity= TH1F("NonBosonMuon_Minus_Rapidity", "NonBosonMuon_Minus_Rapidity;Eta;Frequency", Nbins, RapidityMin, RapidityMax)
NonBosonMuon_Minus_PT = TH1F("NonBosonMuon_Minus_PT", "NonBosonMuon_Minus_PT;Eta;Frequency", Nbins, PTMin, PTMax)

# Outgoing mu+ with boson mu excluded
NonBosonMuon_Plus_Eta = TH1F("NonBosonMuon_Plus_Eta", "NonBosonMuon_Plus_Eta;Eta;Frequency", Nbins, EtaMin, EtaMax)
NonBosonMuon_Plus_Phi = TH1F("NonBosonMuon_Plus_Phi", "NonBosonMuon_Plus_Phi;Eta;Frequency", Nbins, PhiMin, PhiMax)
NonBosonMuon_Plus_Rapidity = TH1F("NonBosonMuon_Plus_Rapidity", "NonBosonMuon_Plus_Rapidity;Eta;Frequency", Nbins, RapidityMin, RapidityMax)
NonBosonMuon_Plus_PT = TH1F("NonBosonMuon_Plus_PT", "NonBosonMuon_Plus_PT;Eta;Frequency", Nbins, PTMin, PTMax) 

# Outgoing leading jets
Jet_Leading_Eta = TH1F("Jet_Leading_Eta", "Jet_Leading_EtaEta;Frequency", Nbins, EtaMin, EtaMax)
Jet_Leading_Phi = TH1F("Jet_Leading_Phi", "Jet_Leading_Phi;Phi;Frequency", Nbins, PhiMin, PhiMax)
Jet_Leading_Rapidity = TH1F("Jet_Leading_Rapidity", "Jet_Leading_Rapidity;Rapidity;Frequency", Nbins, RapidityMin, RapidityMax)
Jet_Leading_PT = TH1F("Jet_Leading_PT", "Jet_Leading_PT;PT;Frequency", Nbins, PTMin, PTMax)

# Outgoing subleading jets
Jet_SubLeading_Eta = TH1F("Jet_SubLeading_Eta", "Jet_SubLeading_Eta;Eta;Frequency", Nbins, EtaMin, EtaMax)
Jet_SubLeading_Phi = TH1F("Jet_SubLeading_Phi", "Jet_SubLeading_Phi;Phi;Frequency", Nbins, PhiMin, PhiMax)
Jet_SubLeading_Rapidity = TH1F("Jet_SubLeading_Rapidity", "Jet_SubLeading_Rapidity;Rapidity;Frequency", Nbins, RapidityMin, RapidityMax)
Jet_SubLeading_PT = TH1F("Jet_SubLeading_PT", "Jet_SubLeading_PT;PT;Frequency", Nbins, PTMin, PTMax)

Q2Min = 0
Q2Max = 200000

QSquared = TH1F("QSquared", "QSquared;Q2;Frequency", Nbins, Q2Min, Q2Max)

dEtaMin = -10
dEtaMax = 10
dPhiMin = PhiMin
dPhiMax = PhiMax
dRapidityMin = -20
dRapidityMax = 20
dRMin = 0
dRMax = 10

MuonMuon_dEta = TH1F("MuonMuon_dEta", "MuonMuon_dEta;dEta;Frequency", Nbins, EtaMin, EtaMax)
MuonMuon_dPhi = TH1F("MuonMuon_dPhi", "MuonMuon_dPhi;dPhi;Frequency", Nbins, PhiMin, PhiMax)
MuonMuon_dRapidity = TH1F("MuonMuon_dRapidity", "MuonMuon_dRapidity;dRapidity;Frequency", Nbins, RapidityMin, RapidityMax)
MuonMuon_dR_Eta = TH1F("MuonMuon_dR_Eta", "MuonMuon_dR_Eta;dR_Eta;Frequency", Nbins, dRMin, dRMax)
MuonMuon_dR_Rap = TH1F("MuonMuon_dR_Rap", "MuonMuon_dR_Rap;dR_Rap;Frequency", Nbins, dRMin, dRMax)


ElectronLeadingMuon_dEta = TH1F("ElectronLeadingMuon_dEta", "ElectronLeadingMuon_dEta;dEta;Frequency", Nbins, EtaMin, EtaMax)
ElectronLeadingMuon_dPhi = TH1F("ElectronLeadingMuon_dPhi", "ElectronLeadingMuon_dPhi;dPhi;Frequency", Nbins, PhiMin, PhiMax)
ElectronLeadingMuon_dRapidity = TH1F("ElectronLeadingMuon_dRapidity", "ElectronLeadingMuon_dRapidity;dRapidity;Frequency", Nbins, RapidityMin, RapidityMax)
ElectronLeadingMuon_dR_Eta = TH1F("ElectronLeadingMuon_dR_Eta", "ElectronLeadingMuon_dR_Eta;dR_Eta;Frequency", Nbins, dRMin, dRMax)
ElectronLeadingMuon_dR_Rap = TH1F("ElectronLeadingMuon_dR_Rap", "ElectronLeadingMuon_dR_Rap;dR_Rap;Frequency", Nbins, dRMin, dRMax)

ElectronSubLeadingMuon_dEta = TH1F("ElectronSubLeadingMuon_dEta", "ElectronSubLeadingMuon_dEta;dEta;Frequency", Nbins, EtaMin, EtaMax)
ElectronSubLeadingMuon_dPhi = TH1F("ElectronSubLeadingMuon_dPhi", "ElectronSubLeadingMuon_dPhi;dPhi;Frequency", Nbins, PhiMin, PhiMax)
ElectronSubLeadingMuon_dRapidity = TH1F("ElectronSubLeadingMuon_dRapidity", "ElectronSubLeadingMuon_dRapidity;dRapidity;Frequency", Nbins, RapidityMin, RapidityMax)
ElectronSubLeadingMuon_dR_Eta = TH1F("ElectronSubLeadingMuon_dR_Eta", "ElectronSubLeadingMuon_dR_Eta;dR_Eta;Frequency", Nbins, dRMin, dRMax)
ElectronSubLeadingMuon_dR_Rap = TH1F("ElectronSubLeadingMuon_dR_Rap", "ElectronSubLeadingMuon_dR_Rap;dR_Rap;Frequency", Nbins, dRMin, dRMax)

METMin = 0
METMax = 500

# Missing ET
MissingET_Eta = TH1F("MissingET_Eta", "MissingET_Eta;Eta;Frequency", Nbins, EtaMin, EtaMax)
MissingET_Phi = TH1F("MissingET_Phi", "MissingET_Phi;Phi;Frequency", Nbins, PhiMin, PhiMax)
MissingET_MET = TH1F("MissingET_MET", "MissingET_MET;MET;Frequency", Nbins, METMin, METMax)

# Looping through events
for n in range(Events):

    myTree.ReadEntry(n)
    
    # Number ot particular particles in eventNbins
    e_count = 0
    mu_count = 0
    jet_count = 0
    
    # List of all final state leptons
    FinalLeptons = []
    
    # Lists for sorting by PT in this event
    ElectronPT = []
    MuonPT = []
    JetPT = []
    
    # Tuples for the components of the electron beam incoming and outgoing 4vectors
    BeamElectron_P = (0 , 0, 0, 0)
    FinalElectron_P = (0 , 0, 0, 0)
    
    # Loop through generated particles
    for i in range(branchParticle.GetEntries()) :
        particle = branchParticle.At(i)        
                    
        # i == 0 corresponds to beam quark
        # i == 1 corresponds to beam electron
        if i == 1:         
            BeamElectron = particle
                    
        # Final state particles                
        if particle.Status == 1:
            
            # Electrons
            if particle.PID == 11:
                # Adding the particle to the final state list
                FinalLeptons.append(particle)                
                e_count += 1

                # Adding the electron to the sorting list 
                ElectronPT.append( (particle.PT, particle) )
                
            # Selecting positrons
            elif particle.PID == -11:
                # Adding the particle to the final state list
                FinalLeptons.append(particle)       
                e_count += 1
                
            # Selecting mu-
            elif particle.PID ==  13 or particle.PID == -13:                
                # Adding the particle to the final state list
                FinalLeptons.append(particle)              
                mu_count += 1                
                
                # Adding the muon to the sorting list                 
                MuonPT.append( (particle.PT, particle) )      
                
            # Selecting neutrinos
            elif abs(particle.PID) == 12 or abs(particle.PID) == 14:
                 FinalLeptons.append(particle)
                
            
        # Loop through generated Jets
    for i in range(branchGenJets.GetEntries()):
        jet = branchGenJets.At(i)
        
        # Keeps track of how many particles the jet overlaps with
        Overlap = 0
        
        # Compare to final state leptons to look for overlap
        for particle in FinalLeptons:
            
            # Only need dEta and dPhi
            # JetLepton = comparison(A=jet, B=particle, dEta=True, dPhi=True, dRapidity=False, dR=False)
            JetLepton = comparison(jet, particle, True, True, False, True, False)
            
            # Small dR corresponds to overlap between the jet and the particle           
            # If the jet overlaps with this particle:
            if JetLepton[3] < 0.4:
                Overlap += 1
                
        # Jet discared if it overlaps with any particles
        if Overlap == 0:
            jet_count += 1
            JetPT.append( ( jet.PT, jet) )
    
    # Sorts ElectronPT based on the 1st element in each tuple in ascending order
    ElectronPT_sorted = sorted(ElectronPT, key=lambda x: x[0])
    FinalElectron = ElectronPT_sorted[-1][1]

    FinalElectron_Eta.Fill(FinalElectron.Eta)
    FinalElectron_Phi.Fill(FinalElectron.Phi)
    FinalElectron_Rapidity.Fill(FinalElectron.Rapidity)
    FinalElectron_PT.Fill(FinalElectron.PT)

    # Sorts MuonPT based on the 1st element in each tuple in ascending order
    MuonPT_sorted = sorted(MuonPT, key=lambda x: x[0])
    
    # Leading and subleading muons have the highest and second highest PT
    LeadingMuon = MuonPT_sorted[-1][1]
    SubLeadingMuon = MuonPT_sorted[-2][1]

    Muon_Leading_Eta.Fill(LeadingMuon.Eta)
    Muon_Leading_Phi.Fill(LeadingMuon.Phi)
    Muon_Leading_Rapidity.Fill(LeadingMuon.Rapidity)
    Muon_Leading_PT.Fill(LeadingMuon.PT)

    Muon_SubLeading_Eta.Fill(SubLeadingMuon.Eta)
    Muon_SubLeading_Phi.Fill(SubLeadingMuon.Phi)
    Muon_SubLeading_Rapidity.Fill(SubLeadingMuon.Rapidity)
    Muon_SubLeading_PT.Fill(SubLeadingMuon.PT)
    
    NonBosonMuon = []
    # i should run from 0 to n-3 (range(a, b) runs from a to b-1)
    for i in range(0, len(MuonPT) - 2):
        
        # mu should include all muons except the leading  and subleading
        mu = MuonPT_sorted[i][1]
        
        if mu.PID == 13:
            NonBosonMuon_Minus_Eta.Fill(mu.Eta)
            NonBosonMuon_Minus_Phi.Fill(mu.Phi)
            NonBosonMuon_Minus_Rapidity.Fill(mu.Rapidity)
            NonBosonMuon_Minus_PT.Fill(mu.PT)
        
        if mu.PID == -13:
            NonBosonMuon_Plus_Eta.Fill(mu.Eta)
            NonBosonMuon_Plus_Phi.Fill(mu.Phi)
            NonBosonMuon_Plus_Rapidity.Fill(mu.Rapidity)
            NonBosonMuon_Plus_PT.Fill(mu.PT)
    
    # Same as before but for the leading and subleading muons
    for i in [1, 2]:
        
        mu = MuonPT_sorted[-i][1]
        
        if mu.PID == 13:
            BosonMuon_Minus_Eta.Fill(mu.Eta)
            BosonMuon_Minus_Phi.Fill(mu.Phi)
            BosonMuon_Minus_Rapidity.Fill(mu.Rapidity)
            BosonMuon_Minus_PT.Fill(mu.PT)
        
        if mu.PID == -13:
            BosonMuon_Plus_Eta.Fill(mu.Eta)
            BosonMuon_Plus_Phi.Fill(mu.Phi)
            BosonMuon_Plus_Rapidity.Fill(mu.Rapidity)
            BosonMuon_Plus_PT.Fill(mu.PT)        

    
    # Sorts JetPT based on the 1st element in each tuple in ascending order 
    JetPT_sorted = sorted(JetPT, key=lambda x: x[0])
    
    if len(JetPT) >= 1:
        
        # The leading jet has the highest PT    
        LeadingJet = JetPT_sorted[-1][1]

        Jet_Leading_Eta.Fill(LeadingJet.Eta)
        Jet_Leading_Phi.Fill(LeadingJet.Phi)
        # Jet doesnt have a Rapidality
#         Jet_Leading_Rapidity.Fill(LeadingJet.Rapidity)
        Jet_Leading_PT.Fill(LeadingJet.PT) 
        
        if len(JetPT) >=2:
            
                # The subleading jet has the second highest PT    
                SubLeadingJet = JetPT_sorted[-2][1]    
                
                Jet_SubLeading_Eta.Fill(SubLeadingJet.Eta)
                Jet_SubLeading_Phi.Fill(SubLeadingJet.Phi)
                # Jet doesnt have a Rapidality
#                 Jet_SubLeading_Rapidity.Fill(SubLeadingJet.Rapidity)
                Jet_SubLeading_PT.Fill(SubLeadingJet.PT)     

    
    # Accounting for beam final state electron, boson muons and beam final state jet
    ElectronCount.Fill(e_count)
    MuonCount.Fill(mu_count)
    JetCount.Fill(jet_count)
    
    # QSquared of the event
    
    FinalElectron_P = (FinalElectron.E,  FinalElectron.Px, FinalElectron.Py, FinalElectron.Pz)
    BeamElectron_P = (BeamElectron.E,  BeamElectron.Px, BeamElectron.Py, BeamElectron.Pz)  
    
    # q = FinalElectron_P - BeamElectron_P (for each element)
    q = tuple(x-y for x,y in zip(FinalElectron_P, BeamElectron_P))
    # Q2 = - q.q = E^2 - p^2
    Q2 = abs( q[0]**2 - (q[1]**2 + q[2]**2 + q[3]**2) )
    
#     FinalElectron_Theta = TMath.ATan(FinalElectron.CtgTheta)
#     Q2 = abs( 2*FinalElectron.E*BeamElectron.E*( 1 + TMath.Cos(FinalElectron_Theta)) )  
    
#     print('Event', n, ' Final Electron:', FinalElectron_P, ' Beam Electron:', BeamElectron_P, ' Q2', Q2)
    QSquared.Fill(Q2)
    
    
    
    # Comparing the leading muons
    MuonMuon = comparison(LeadingMuon, SubLeadingMuon)
    
    MuonMuon_dEta.Fill(MuonMuon[0])
    MuonMuon_dPhi.Fill(MuonMuon[1])
    MuonMuon_dRapidity.Fill(MuonMuon[2])
    MuonMuon_dR_Eta.Fill( MuonMuon[3] )
    MuonMuon_dR_Rap.Fill( MuonMuon[4] )
    
    # Comparing the electron and leading muon
    ElectronLeadingMuon = comparison(FinalElectron, LeadingMuon)

    ElectronLeadingMuon_dEta.Fill(ElectronLeadingMuon[0])
    ElectronLeadingMuon_dPhi.Fill(ElectronLeadingMuon[1])
    ElectronLeadingMuon_dRapidity.Fill(ElectronLeadingMuon[2])
    ElectronLeadingMuon_dR_Eta.Fill( ElectronLeadingMuon[3] )
    ElectronLeadingMuon_dR_Rap.Fill( ElectronLeadingMuon[4] )
    
    # Comparing the electron and subleading muon
    ElectronSubLeadingMuon = comparison(FinalElectron, SubLeadingMuon)

    ElectronSubLeadingMuon_dEta.Fill(ElectronSubLeadingMuon[0])
    ElectronSubLeadingMuon_dPhi.Fill(ElectronSubLeadingMuon[1])
    ElectronSubLeadingMuon_dRapidity.Fill(ElectronSubLeadingMuon[2])
    ElectronSubLeadingMuon_dR_Eta.Fill( ElectronSubLeadingMuon[3] )
    ElectronSubLeadingMuon_dR_Rap.Fill( ElectronSubLeadingMuon[4] )
    
    # Comparing the leading jets (Should first impliment jet cuts)
#     MuonMuon = [
#         LeadingMuon.Eta - SubLeadingMuon.Eta, #dEta
#         LeadingMuon.Phi - SubLeadingMuon.Phi, #dPhi
#         LeadingMuon.Rapidity - SubLeadingMuon.Rapidity #dRapidity
#     ]

#     MuonMuon_dEta.Fill(MuonMuon[0])
#     MuonMuon_dPhi.Fill(MuonMuon[1])
#     MuonMuon_dRapidity.Fill(MuonMuon[2])
#     MuonMuon_dR.Fill( (MuonMuon[1]**2 + MuonMuon[2]**2)**0.5 )        
 
    for i in range(branchMissingET.GetEntries()) :
        missingET = branchMissingET.At(i)       
        
        MissingET_Eta.Fill(missingET.Eta)
        MissingET_Phi.Fill(missingET.Phi)
        MissingET_MET.Fill(missingET.MET)
        
    
outfile.Write()
outfile.Close()
