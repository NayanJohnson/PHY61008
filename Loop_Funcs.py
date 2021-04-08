from ROOT import gSystem, gInterpreter, TChain, TLorentzVector

# Path of Delphes directory 
gSystem.AddDynamicPath("/home/nayan/MG5_aMC_v2_8_2/Delphes/")
gSystem.Load("libDelphes")

gInterpreter.Declare('#include "classes/DelphesClasses.h"')
gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')

import config, requests, itertools
import Particle_Funcs as ParticleFuncs
import Hist_Funcs as HistFuncs

"""
Definitions of used objects:

TreeDict =  {
    'Tree'      :   myTree,
    'NEvents'   :   NEvents,
    'Branches'  :   {
        'Particle'          :   branchParticle,
        'GenJets'           :   branchGenJets,
    }
} 

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

"""
def LoadROOT(filename):
    '''
    Loads .root file with tree labeled "Delphes" and outputs dictionary containing the number 
    of events and branches.
    '''

    # Create chain of root trees 
    chain = TChain("Delphes")
    chain.Add(filename)

    # Create object of class ExRootTreeReader
    myTree = ExRootTreeReader(chain)
    NEvents = myTree.GetEntries()

    # Get pointers to branches used in this analysis
    branchParticle = myTree.UseBranch("Particle")
    branchGenJets = myTree.UseBranch("GenJet")

    TreeDict =  {
                    'Tree'      :   myTree,
                    'NEvents'   :   NEvents,
                    'Branches'  :   {
                        'Particle'          :   branchParticle,
                        'GenJets'           :   branchGenJets,
                    }
                }

    return TreeDict

def ParticleLoop(TreeDict, EventNum, Run):
    '''
    Main particle loop.
    Given a TreeDict, the event number and type of run, will return an EventDict
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
        ParticleDict = ParticleFuncs.AddParticle(keyword, ParticleDict)

    # Particle loop with cuts
    EventDict = ParticleLoop(myTree, EventNum, Run)

    # Adding BeamElectron and BeamQuark
    ParticleDict = ParticleFuncs.AddParticle('BeamElectron', ParticleDict, EventDict['BeamElectron'].P4())
    ParticleDict = ParticleFuncs.AddParticle('BeamQuark', ParticleDict, EventDict['BeamQuark'].P4())

    # FinalElectron
    numbElectrons = EventDict['Count']['Electrons']
    for i in range(0, numbElectrons):
        # Checking that there is at least one electron present
        if numbElectrons != 0:
            LeadingElectron = EventDict['PTSorted']['Electron'][-1][1]
            ParticleDict = ParticleFuncs.AddParticle('LeadingElectron', ParticleDict, LeadingElectron.P4())

    # Leading and SubLeading muons
    numbMuons = EventDict['Count']['Muons']
    for i in range(0, numbMuons):

        # Checking that there is at least one muon present
        if numbMuons != 0:
            Muon = EventDict['PTSorted']['Muon'][i][1]
            # Leading Muon
            if i == numbMuons - 1:
                ParticleDict = ParticleFuncs.AddParticle('LeadingMuon', ParticleDict, Muon.P4(), Muon.PID)

            # SubLeading Muon
            elif i == numbMuons - 2 and numbMuons - 2 >= 0:
                ParticleDict = ParticleFuncs.AddParticle('SubLeadingMuon', ParticleDict, Muon.P4(), Muon.PID)

            elif i == numbMuons - 3 and numbMuons - 3 >= 0:
                ParticleDict = ParticleFuncs.AddParticle('ThirdMuon', ParticleDict, Muon.P4(), Muon.PID)

    # Jets
    numbJets = EventDict['Count']['Jets']
    for i in range(0, numbJets):
        
        # Checking that there is at least one jet present
        if numbJets != 0:
            Jet = EventDict['PTSorted']['Jet'][i][1]

            # Selecting the leading jet
            if i == numbJets - 1:
                ParticleDict = ParticleFuncs.AddParticle('LeadingJet', ParticleDict, Jet.P4())
            # Selecting and checking for the subleading jet
            elif i == numbJets - 2 and numbJets - 2 >= 0:
                ParticleDict = ParticleFuncs.AddParticle('SubLeadingJet', ParticleDict, Jet.P4())
            # Selecting and checking for the third jet 
            elif i == numbJets - 3 and numbJets - 3 >= 0:
                ParticleDict = ParticleFuncs.AddParticle('ThirdJet', ParticleDict, Jet.P4())
            # Selecting and checking for the fourth jet
            elif i == numbJets - 4 and numbJets - 4 >= 0:
                ParticleDict = ParticleFuncs.AddParticle('FourthJet', ParticleDict, Jet.P4())
            # Any extra jets
            else:
                ParticleDict = ParticleFuncs.AddParticle(str(i+1)+'Jet', ParticleDict, Jet.P4())

    # MissingET
    ParticleDict = ParticleFuncs.AddParticle('MissingET', ParticleDict, EventDict['MissingET_P'])

    # MuonSum
    MuonSum = None 
    if ParticleDict['LeadingMuon']['Check'] and ParticleDict['SubLeadingMuon']['Check'] and ParticleDict['ThirdMuon']['Check']:
        MuonSum = ParticleDict['LeadingMuon']['P4'] + ParticleDict['SubLeadingMuon']['P4'] +ParticleDict['ThirdMuon']['P4']
        ParticleDict = ParticleFuncs.AddParticle('MuonSum', ParticleDict, MuonSum)

    # Count hists
    HistDict['Electrons']['Count'] = numbElectrons
    HistDict['Muons']['Count'] = numbMuons
    HistDict['Jets']['Count'] = numbJets

    return HistDict, ParticleDict, EventDict

def EventLoop(myTree, outfileprefix, LoopRun, EventRun, BackgroundRun):
    '''
    '''

    outfilename = outfileprefix+'_Loop'+LoopRun+'Event'+EventRun+'Background'+BackgroundRun+'.root'

    # Open output
    outfile = TFile(outfilename,"RECREATE")

    HistDict = requests.HistDict

    # Initialise requested hists from HistDict
    HistDict = HistFuncs.MakeHists(HistDict)

    EventCuts = config.EventLoopParams['Level']['Event'][EventRun]
    BackgroundCuts = config.EventLoopParams['Level']['Background'][BackgroundRun] 
    
    Zdecays = config.EventLoopParams['Z']['Decays']
    WPlusdecays = config.EventLoopParams['WPlus']['Decays']
    WMinusdecays = config.EventLoopParams['WMinus']['Decays']
    
    EventCutNum = 0
    # Looping through events
    for EventNum in range(myTree['NEvents']):

        HistDict, ParticleDict, EventDict = ParticleFuncs.GetParticles(myTree, LoopRun, HistDict, EventNum)

        FinalBeamElectron_Sorted = list(EventDict['PTSorted']['Electron'])

        # print('before:', len(FinalBeamElectron_Sorted))
        # print([(x, x[1].P4().Eta()) for x in FinalBeamElectron_Sorted])
        # i = 0
        

        # Cuts out electrons in the PTSorted list and then takes the leading result as the beam electron
        for particle in EventDict['PTSorted']['Electron']:
            # print(particle)
            # i+=1
            # print(i)
            if BackgroundCuts['BeamElectron']['Eta'][0] <= particle[1].P4().Eta() <= BackgroundCuts['BeamElectron']['Eta'][1]:
                # print('Pass')
                continue
            else:
                FinalBeamElectron_Sorted.remove(particle)
                # print('Remove')

        # print('after:', len(FinalBeamElectron_Sorted))
        # print([(x, x[1].P4().Eta()) for x in FinalBeamElectron_Sorted])

        if len(FinalBeamElectron_Sorted) != 0:
            ParticleDict = ParticleFuncs..AddParticle('FinalBeamElectron', ParticleDict, FinalBeamElectron_Sorted[-1][1].P4())
        else:
            continue


        # Event level selection for WWEmJ_WW_Muons
        if EventDict['Count']['Electrons'] >= EventCuts['Electrons'] and EventDict['Count']['Muons'] >= EventCuts['Muons'] and EventDict['Count']['Jets'] >= EventCuts['Jets']:
            
            EventCutNum += 1
            for Zdecay in Zdecays:
                if Zdecay == None:
                    continue
                elif Zdecays[0] == Zdecays[1]:
                    continue
                else:
                    ParticleDict, EventDict = ParticleFuncs..InvMassCheck(Zdecay, 'Z', ParticleDict, EventDict)

            for WPlusdecay in WPlusdecays:
                if WPlusdecay == None:
                    continue
                elif WPlusdecays[0] == WPlusdecays[1]:
                    continue            
                elif WPlusdecay == 'Jets':
                    ParticleDict, EventDict = ParticleFuncs..InvMassCheck(WPlusdecay, 'WPlus', ParticleDict, EventDict)
                else:
                    particlesList = [ParticleDict['Leading'+WPlusdecay[0:-1]], ParticleDict['SubLeading'+WPlusdecay[0:-1]]]
                    for Lepton in particlesList:
                        if Lepton['Check']:
                            if Lepton['PID'] == -13:
                                ParticleDict = ParticleFuncs..AddParticle('WPlus'+WPlusdecay[0:-1], ParticleDict, Lepton['P4'])

            for WMinusdecay in WMinusdecays:
                if WMinusdecay == None:
                    continue
                elif WMinusdecays[0] == WMinusdecays[1]:
                    continue            
                elif WMinusdecay == 'Jets':
                    ParticleDict, EventDict = ParticleFuncs..InvMassCheck(WMinusdecay, 'WMinus', ParticleDict, EventDict)
                else:
                    particlesList = [ParticleDict['Leading'+WMinusdecay[0:-1]], ParticleDict['SubLeading'+WMinusdecay[0:-1]]]
                    for Lepton in particlesList:
                        if Lepton['Check']:
                            if Lepton['PID'] == 13:
                                ParticleDict = ParticleFuncs..AddParticle('WMinus'+WMinusdecay[0:-1], ParticleDict, Lepton['P4'])

            if len(EventDict['PTSorted']['Jet']) != 0:
                ParticleDict = ParticleFuncs..AddParticle('FinalBeamJet', ParticleDict, EventDict['PTSorted']['Jet'][-1][1].P4())

            # Filling HistDict with particles then filling the hists
            HistDict = ParticleFuncs..RequestParticles(HistDict, ParticleDict)
            HistFuncs.FillHists(HistDict)

    # Get scaling factor for histograms
    Scale = HistFuncs.GetScale('tag_1_pythia.log', myTree['NEvents'])

    # Scaling and altering hist lims
    for category, attributes in HistDict.items():
        for var, hist in attributes['Hists'].items():
            hist = HistFuncs.HistLims(hist, var, Scale=Scale)[0]
    # Writing and closing file
    outfile.Write()
    outfile.Close()
