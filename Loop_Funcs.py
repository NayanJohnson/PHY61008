from ROOT import gSystem, gInterpreter, TChain, TH1F, TH2F, TMath, TLorentzVector, TCanvas, TLegend, SetOwnership, TColor

import config, itertools
import Loop_Funcs as Loop
import Hist_Funcs as Hist

def ParticleLoop(TreeDict, EventNum, Run):
    '''
    Main particle loop.
    Given a dictionary:

    TreeDict =  {
        'Tree'      :   myTree,
        'NEvents'   :   NEvents,
        'Branches'  :   {
            'Particle'          :   branchParticle,
            'GenJets'           :   branchGenJets,
        }
    } 

    and the event being inspected, will return a dictionary:

    EventDict   =   {
        'Count'     :   {
            'Electrons'  :   e_count,
            'Muons'      :   mu_count,
            'Jets'       :   jet_count
        },
        'BeamElectron'  :   BeamElectron,
        'BeamQuark'     :   BeamQuark,
        'MissingET_P'   :   MissingET_P,
        'PTSorted'  :   {
            'Electron'  :   ElectronPT_sorted,
            'Muon'      :   MuonPT_sorted,
            'Jet'       :   JetPT_sorted
        }
    }
    '''
    Cuts = config.EventLoopParams['Level']['Loop'][Run]

    # Reading a specific event 
    TreeDict['Tree'].ReadEntry(EventNum)

    # Number ot particular particles in eventNbins
    e_count = 0
    mu_count = 0
    jet_count = 0
    
    # List of all final state leptons
    FinalLeptons = []
    
    # Neutrino 4momentum list
    MissingParticle = []

    # Lists for sorting by PT in this event
    ElectronPT = []
    MuonPT = []
    JetPT = []
    
    
    # Loop through generated particles
    for i in range(TreeDict['Branches']['Particle'].GetEntries()) :
        particle = TreeDict['Branches']['Particle'].At(i)        
                    
        # i == 0 corresponds to beam quark
        if i == 0:
            BeamQuark = particle
        # i == 1 corresponds to beam electron
        elif i == 1:         
            BeamElectron = particle
          
        # Final state particles                
        if particle.Status == 1:
            
            # Electrons and positrons
            if abs(particle.PID) == 11:
                # Electron cuts
                if Cuts['e_Eta'][0] <= particle.P4().Eta() <= Cuts['e_Eta'][1]:
                    if particle.P4().Pt() >= Cuts['e_Pt']:
                        # Adding the particle to the final state list
                        FinalLeptons.append(particle)                
                        e_count += 1
                        # Adding the electron to the sorting list 
                        ElectronPT.append( (particle.P4().Pt(), particle) )


                # Adding the electron to the sorting list 
                ElectronPT.append( (particle.PT, particle) )
                
            # Selecting mu
            elif abs(particle.PID) ==  13:     
                # Muon cuts
                if Cuts['mu_Eta'][0] <= particle.P4().Eta() <= Cuts['mu_Eta'][1]:
                    if particle.P4().Pt() >= Cuts['mu_Pt']:
                        # Adding the particle to the final state list
                        FinalLeptons.append(particle)              
                        mu_count += 1                
                        # Adding the muon to the sorting list                 
                        MuonPT.append( (particle.P4().Pt(), particle) )   

                   
                
            # Selecting neutrinos
            elif abs(particle.PID) == 12 or abs(particle.PID) == 14:
                MissingParticle.append(particle)
                
            FinalLeptons = FinalLeptons + MissingParticle
                
            
        # Loop through generated Jets
    for i in range(TreeDict['Branches']['GenJets'].GetEntries()):
        jet = TreeDict['Branches']['GenJets'].At(i)
        
        # Keeps track of how many particles the jet overlaps with
        Overlap = 0
        
        # Compare to final state leptons to look for overlap
        for particle in FinalLeptons:
            
            # Only need dR_Eta
            JetLepton_dR_Eta = jet.P4().DrEtaPhi(particle.P4())
       
            # Small dR corresponds to overlap between the jet and the particle  
            # If the jet overlaps with this particle:
            if JetLepton_dR_Eta < 0.4:
                Overlap += 1
                
        # Jet discared if it overlaps with any particles
        if Overlap == 0:
            # Jet cuts
            if Cuts['jet_Eta'][0] <= jet.P4().Eta() <= Cuts['e_Eta'][1]:
                if jet.P4().Pt() >= Cuts['jet_Pt']:
                    jet_count += 1
                    JetPT.append( (jet.P4().Eta(), jet) )
    
    # Sorts ElectronPT based on the 1st element in each tuple in ascending order
    ElectronPT_sorted = sorted(ElectronPT, key=lambda x: x[0])
    MuonPT_sorted = sorted(MuonPT, key=lambda x: x[0])
    JetPT_sorted = sorted(JetPT, key=lambda x: x[0])

    # MissingE is the sum of all neutrino momenta in the event
    MissingET_P = TLorentzVector()
    for particle in MissingParticle:
        particle.P4().SetPz(0)
        particle.P4().SetE(particle.P4().Et())
        MissingET_P = MissingET_P + particle.P4()

    EventDict   =   {
        'Count'     :   {
            'Electrons'  :   e_count,
            'Muons'      :   mu_count,
            'Jets'       :   jet_count
        },
        'BeamElectron'  :   BeamElectron,
        'BeamQuark'     :   BeamQuark,
        'MissingET_P'   :   MissingET_P,
        'PTSorted'  :   {
            'Electron'  :   ElectronPT_sorted,
            'Muon'      :   MuonPT_sorted,
            'Jet'       :   JetPT_sorted
        }
    }

    return EventDict

def GetParticles(myTree, Run, HistDict, EventNum):
    '''
    '''

    ParticleKeywords = config.ParticleKeywords
    # Reset particle list for the new event
    for _, dictionary in HistDict.items():
        dictionary['Particles'] = []
        
    # Reset ParticeDict for this event
    ParticleDict = {}
    for keyword in ParticleKeywords:
        ParticleDict = AddParticle(keyword, ParticleDict)

    # Particle loop with cuts
    EventDict = ParticleLoop(myTree, EventNum, Run)

    # Adding BeamElectron and BeamQuark
    ParticleDict = AddParticle('BeamElectron', ParticleDict, EventDict['BeamElectron'].P4())
    ParticleDict = AddParticle('BeamQuark', ParticleDict, EventDict['BeamQuark'].P4())

    # FinalElectron
    numbElectrons = EventDict['Count']['Electrons']
    for i in range(0, numbElectrons):
        # Checking that there is at least one electron present
        if numbElectrons != 0:
            LeadingElectron = EventDict['PTSorted']['Electron'][-1][1]
            ParticleDict = AddParticle('LeadingElectron', ParticleDict, LeadingElectron.P4())

    # Leading and SubLeading muons
    numbMuons = EventDict['Count']['Muons']
    for i in range(0, numbMuons):

        # Checking that there is at least one muon present
        if numbMuons != 0:
            Muon = EventDict['PTSorted']['Muon'][i][1]
            # Leading Muon
            if i == numbMuons - 1:
                ParticleDict = AddParticle('LeadingMuon', ParticleDict, Muon.P4(), Muon.PID)

            # SubLeading Muon
            elif i == numbMuons - 2 and numbMuons - 2 >= 0:
                ParticleDict = AddParticle('SubLeadingMuon', ParticleDict, Muon.P4(), Muon.PID)

            elif i == numbMuons - 3 and numbMuons - 3 >= 0:
                ParticleDict = AddParticle('ThirdMuon', ParticleDict, Muon.P4(), Muon.PID)

    # Jets
    numbJets = EventDict['Count']['Jets']
    for i in range(0, numbJets):
        
        # Checking that there is at least one jet present
        if numbJets != 0:
            Jet = EventDict['PTSorted']['Jet'][i][1]

            # Selecting the leading jet
            if i == numbJets - 1:
                ParticleDict = AddParticle('LeadingJet', ParticleDict, Jet.P4())
            # Selecting and checking for the subleading jet
            elif i == numbJets - 2 and numbJets - 2 >= 0:
                ParticleDict = AddParticle('SubLeadingJet', ParticleDict, Jet.P4())
            # Selecting and checking for the third jet 
            elif i == numbJets - 3 and numbJets - 3 >= 0:
                ParticleDict = AddParticle('ThirdJet', ParticleDict, Jet.P4())
            # Selecting and checking for the fourth jet
            elif i == numbJets - 4 and numbJets - 4 >= 0:
                ParticleDict = AddParticle('FourthJet', ParticleDict, Jet.P4())
            # Any extra jets
            else:
                ParticleDict = AddParticle(str(i+1)+'Jet', ParticleDict, Jet.P4())

    # MissingET
    ParticleDict = AddParticle('MissingET', ParticleDict, EventDict['MissingET_P'])

    # MuonSum
    MuonSum = None 
    if ParticleDict['LeadingMuon']['Check'] and ParticleDict['SubLeadingMuon']['Check'] and ParticleDict['ThirdMuon']['Check']:
        MuonSum = ParticleDict['LeadingMuon']['P4'] + ParticleDict['SubLeadingMuon']['P4'] +ParticleDict['ThirdMuon']['P4']
        ParticleDict = AddParticle('MuonSum', ParticleDict, MuonSum)

    # Count hists
    HistDict['Electrons']['Count'] = numbElectrons
    HistDict['Muons']['Count'] = numbMuons
    HistDict['Jets']['Count'] = numbJets

    return HistDict, ParticleDict, EventDict

