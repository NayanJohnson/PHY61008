"""
Data structures used:

Holds 
TreeDict =  {
    'Tree'          :       TChain of all trees being used,
    'TreeReader'    :       ExRootTreeReader(chain),
    'Branches'  :   {
        'Name'              :   TreeReader.UseBranch('Name'),
        ...
    }
} 

EventDict   =   {
    'Count'     :   {
        Particle Name  :   Count,
        ...
    },
    'BeamElectron'  :   BeamElectron,
    'BeamQuark'     :   BeamQuark,
    'MissingET'     :   MissingET,
    'PTSorted'  :   {
        'Electron'  :   ElectronPT_sorted,
        'Muon'      :   MuonPT_sorted,
        'Jet'       :   JetPT_sorted
    }
}
"""


# Needed to allow use of kInfo, gErrorIgnoreLevel
import ROOT

# Used to make some functions shut up :P
class Quiet:
    """
    Context manager for silencing certain ROOT operations.  Usage:
    with Quiet(level = ROOT.kInfo+1):
       foo_that_makes_output

    You can set a higher or lower warning level to ignore different
    kinds of messages.  After the end of indentation, the level is set
    back to what it was previously.

    gErrorIgnoreLevel = kPrint, kInfo, kWarning, kError, kBreak, kSysError, kFatal
    """
    def __init__(self, level=ROOT.kInfo + 1):
        self.level = level

    def __enter__(self):
        self.oldlevel = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = self.level

    def __exit__(self, type, value, traceback):
        ROOT.gErrorIgnoreLevel = self.oldlevel


from ROOT import gSystem, gInterpreter, TChain, TFile, TLorentzVector

# Path of Delphes directory in your system
gSystem.AddDynamicPath('/home/nayan/MG5_aMC_v2_8_2/Delphes/')
gSystem.Load('libDelphes')

gInterpreter.Declare('#include "classes/DelphesClasses.h"')
gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')

from ROOT import ExRootTreeReader

# Import other .py files to use
import config, requests
import Particle_Funcs as ParticleFuncs
import Hist_Funcs as HistFuncs

def LoadTrees(TreeList, prefix):
    '''
    Loads all 'Delphes' trees in the TreeList outputs a dictionary containing information and branch pointers
    '''

    # Create chain of root trees 
    chain = TChain('Delphes')
    for tree in TreeList:
        chain.Add(tree)

    # Create object of class ExRootTreeReader
    TreeReader = ExRootTreeReader(chain)

    # The data set may use a different NEvents than is stored in the data set 
    # eg. if the data set has been pruned it will have a lower NEvents than output from MG5
    if prefix=='Signal' or prefix=='Background':
        NEvents = config.EventLoopParams[prefix]['NEvents']
    else:
        NEvents = TreeReader.GetEntries()

    # Get pointers to branches used in this analysis
    branchParticle  = TreeReader.UseBranch('Particle')
    branchGenJet    = TreeReader.UseBranch('GenJet')
    branchElectron  = TreeReader.UseBranch('Electron')
    branchMuon      = TreeReader.UseBranch('Muon')
    branchJet       = TreeReader.UseBranch('Jet')
    branchMissingET = TreeReader.UseBranch('MissingET')

    TreeDict =  {
                    'Tree'          :       chain,
                    'TreeReader'    :       TreeReader,
                    'NEvents'       :       NEvents,
                    'Branches'      :       {
                        'Particle'          :   branchParticle,
                        'GenJet'            :   branchGenJet,
                        'Electron'          :   branchElectron,
                        'Muon'              :   branchMuon,
                        'Jet'               :   branchJet,
                        'MissingET'         :   branchMissingET,
                    }
                }

    return TreeDict

def ParticleLoop(TreeDict, EventNum, LevelRun, LoopRun):
    '''
    Main particle loop.
    Given a TreeDict, the event number and type of run, will return an EventDict
    '''

    # Loading loop cuts for this run
    Cuts = config.EventLoopParams['Level']['Loop'][LoopRun]

    # Reading a specific event 
    TreeDict['TreeReader'].ReadEntry(EventNum)

    # Number ot particular particles in eventNbins
    e_count = 0
    mu_count = 0
    jet_count = 0
    
    # List of all final state leptons
    FinalLeptons = []
    
    # MissingET 4momentum list (truth level)
    MissingParticle = []

    # Lists for sorting by PT in this event
    ElectronPT = []
    MuonPT = []
    JetPT = []
    
    if LevelRun == 'Generator':
        # Loop through generated particles
        for i in range(TreeDict['Branches']['Particle'].GetEntries()) :
            particle = TreeDict['Branches']['Particle'].At(i)
                        
            # i == 0 corresponds to beam quark
            if i == 0:
                BeamQuark = particle.P4()
            # i == 1 corresponds to beam electron
            elif i == 1:         
                BeamElectron = particle.P4()
            
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
                
            # MissingE is the sum of all neutrino momenta in the event
            MissingET = TLorentzVector()
            for particle in MissingParticle:
                MissingET = particle.P4() + MissingET
            
    elif LevelRun == 'Detector':
        
        # Making BeamElectron 4vector moving with 50GeV in -z direction
        BeamElectron = TLorentzVector(0, 0, -50, 50)
        # Impossible to know the momenta of the collided quark
        BeamQuark = False

        # Loop through detected electrons
        for i in range(TreeDict['Branches']['Electron'].GetEntries()) :
            electron = TreeDict['Branches']['Electron'].At(i)        
            
            # Electron cuts
            if Cuts['e_Eta'][0] <= electron.P4().Eta() <= Cuts['e_Eta'][1]:
                if electron.P4().Pt() >= Cuts['e_Pt']:

                    # Electrons
                    if electron.Charge == -1:
                        e_count += 1
                        # Adding the electron to the sorting list 
                        ElectronPT.append( (electron.P4().Pt(), electron) )

                    # Adding the particle to the final state list
                    FinalLeptons.append(electron)  

        # Loop through detected muons
        for i in range(TreeDict['Branches']['Muon'].GetEntries()) :
            muon = TreeDict['Branches']['Muon'].At(i)        
            
            # Muon cuts
            if Cuts['mu_Eta'][0] <= muon.P4().Eta() <= Cuts['mu_Eta'][1]:
                if muon.P4().Pt() >= Cuts['mu_Pt']:

                    mu_count += 1                
                    # Adding the muon to the sorting list
                    MuonPT.append( (muon.P4().Pt(), muon) )   
                    # Adding the particle to the final state list
                    FinalLeptons.append(muon)              
        
        # Only one MissingET entry per event
        MissingET = TreeDict['Branches']['MissingET'].At(0).P4()    

    # Reco or truth jet branch
    if LevelRun == 'Generator':
        JetBranch = 'GenJet'
    elif LevelRun == 'Detector':
        JetBranch = 'Jet'

    # Loop through jets
    for i in range(TreeDict['Branches'][JetBranch].GetEntries()):
        jet = TreeDict['Branches'][JetBranch].At(i)
        
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
                    JetPT.append( (jet.P4().Pt(), jet) )
    
    # Sorts particle based on the 1st element in each tuple (the Pt) in ascending order
    ElectronPT_sorted = sorted(ElectronPT, key=lambda x: x[0])
    MuonPT_sorted = sorted(MuonPT, key=lambda x: x[0])
    JetPT_sorted = sorted(JetPT, key=lambda x: x[0])

    EventDict   =   {
        'Count'     :   {
            'Electrons'  :   e_count,
            'Muons'      :   mu_count,
            'Jets'       :   jet_count
        },
        'BeamElectron'  :   BeamElectron,
        'BeamQuark'     :   BeamQuark,
        'MissingET'     :   MissingET,
        'PTSorted'  :   {
            'Electrons'  :   ElectronPT_sorted,
            'Muons'      :   MuonPT_sorted,
            'Jets'       :   JetPT_sorted
        }
    }

    return EventDict

def GetParticles(TreeDict, LevelRun, LoopRun, HistDict, EventNum):
    '''
    Fills ParticleDict for a specific event.
    '''

    ParticleKeywords = requests.ParticleKeywords
    # Reset particle list for the new event
    for _, dictionary in HistDict.items():
        dictionary['Particles'] = []

    # Reset ParticeDict for this event
    ParticleDict = {}
    for keyword in ParticleKeywords:
        ParticleDict = ParticleFuncs.AddParticle(keyword, ParticleDict)

    # Loop through all particles in the event
    EventDict = ParticleLoop(TreeDict, EventNum, LevelRun, LoopRun)

    # BeamElectron and BeamQuark
    ParticleDict = ParticleFuncs.AddParticle('BeamElectron', ParticleDict, EventDict['BeamElectron'])
    ParticleDict = ParticleFuncs.AddParticle('BeamQuark', ParticleDict, EventDict['BeamQuark'])

    # Detected electrons in event 
    numbElectrons = EventDict['Count']['Electrons']
    # Leading electron
    for i in range(0, numbElectrons):
        # Checking that there is at least one electron present
        if numbElectrons != 0:
            # Take the leading electron from the PTSorted list
            LeadingElectron = EventDict['PTSorted']['Electrons'][-1][1]
            ParticleDict = ParticleFuncs.AddParticle('LeadingElectron', ParticleDict, LeadingElectron.P4())

    # Detected muons in event 
    numbMuons = EventDict['Count']['Muons']
    # Leading muons
    for i in range(0, numbMuons):
        # Checking that there is at least one muon present
        if numbMuons != 0:
            # Take the ith leading muon from the PTSorted list
            Muon = EventDict['PTSorted']['Muons'][i][1]

            if i == numbMuons - 1:
                ParticleDict = ParticleFuncs.AddParticle('LeadingMuon', ParticleDict, Muon.P4(), Muon.Charge)
            elif i == numbMuons - 2 and numbMuons - 2 >= 0:
                ParticleDict = ParticleFuncs.AddParticle('SubLeadingMuon', ParticleDict, Muon.P4(), Muon.Charge)
            elif i == numbMuons - 3 and numbMuons - 3 >= 0:
                ParticleDict = ParticleFuncs.AddParticle('ThirdMuon', ParticleDict, Muon.P4(), Muon.Charge)

    # Detected jets in event (after jet overlap removal) 
    numbJets = EventDict['Count']['Jets']
    # Leading jets
    for i in range(0, numbJets):
        # Checking that there is at least one jet present
        if numbJets != 0:
            # Take the ith leading jet from the PTSorted list
            Jet = EventDict['PTSorted']['Jets'][i][1]

            if i == numbJets - 1:
                ParticleDict = ParticleFuncs.AddParticle('LeadingJet', ParticleDict, Jet.P4())
            elif i == numbJets - 2 and numbJets - 2 >= 0:
                ParticleDict = ParticleFuncs.AddParticle('SubLeadingJet', ParticleDict, Jet.P4())
            elif i == numbJets - 3 and numbJets - 3 >= 0:
                ParticleDict = ParticleFuncs.AddParticle('ThirdJet', ParticleDict, Jet.P4())
            elif i == numbJets - 4 and numbJets - 4 >= 0:
                ParticleDict = ParticleFuncs.AddParticle('FourthJet', ParticleDict, Jet.P4())
            else:
                ParticleDict = ParticleFuncs.AddParticle(str(i+1)+'Jet', ParticleDict, Jet.P4())

    # MET
    ParticleDict = ParticleFuncs.AddParticle('MissingET', ParticleDict, EventDict['MissingET'])

    # Count hists
    HistDict['Electrons']['Count'] = numbElectrons
    HistDict['Muons']['Count'] = numbMuons
    HistDict['Jets']['Count'] = numbJets

    return HistDict, ParticleDict, EventDict

def EventLoop(TreeDict, Xsec, outfilename, LevelRun, LoopRun, EventRun, AnalysisRun):
    '''
    Loops over all events to fill hists.
    Includes further analysis on each event to decide what to keep and discard.
    Some more complicated particles are also calculated here. (eg. sum of multiple particles)
    '''

    # Open output
    outfile = TFile(outfilename+'.root','RECREATE')

    # Get HistDict
    HistDict = requests.HistDict

    # Initialise requested hists from HistDict
    HistDict = HistFuncs.MakeHists(HistDict)

    # Get event and analysis cuts for this run
    EventCuts = config.EventLoopParams['Level']['Event'][EventRun]
    AnalysisCuts = config.EventLoopParams['Level']['Analysis'][AnalysisRun] 

    # Get the expected boson decays for this process
    Zdecays = config.EventLoopParams['Z']['Decays']
    WPlusdecays = config.EventLoopParams['WPlus']['Decays']
    WMinusdecays = config.EventLoopParams['WMinus']['Decays']
    
    # Initialise some useful debugging variables
    BeamElectronSelection = 0
    EventKeptNum = 0
    EventCutNum = 0

    ContinueCut = 0
    Continue = False

    # Looping through events
    for EventNum in range(TreeDict['TreeReader'].GetEntries()):
        
        # Progress output every 10000 events
        if EventNum % 10000 == 0:
            print(EventNum, ' events completed.')

        # Fill the ParticleDict for this event
        HistDict, ParticleDict, EventDict = GetParticles(TreeDict, LevelRun, LoopRun, HistDict, EventNum)

        # Event cuts
        if EventDict['Count']['Electrons'] < EventCuts['Electrons'] or EventDict['Count']['Muons'] < EventCuts['Muons'] or EventDict['Count']['Jets'] < EventCuts['Jets']:
            continue

        # MET cuts
        if EventDict['MissingET'].Et() < AnalysisCuts['MissingET']['Et'][0] or AnalysisCuts['MissingET']['Et'][1] < EventDict['MissingET'].Et():
            continue
        
        # LeadingJet SubLeadingJet Cut
        if ParticleDict['LeadingJet']['Check']:
            if ParticleDict['LeadingJet']['Pt'] < AnalysisCuts['LeadingJet']['Pt'][0] or AnalysisCuts['LeadingJet']['Pt'][1] < ParticleDict['LeadingJet']['Pt']:
                continue
        if ParticleDict['SubLeadingJet']['Check']:
            if ParticleDict['SubLeadingJet']['Pt'] < AnalysisCuts['SubLeadingJet']['Pt'][0] or AnalysisCuts['SubLeadingJet']['Pt'][1] < ParticleDict['SubLeadingJet']['Pt']:
                continue        

        # MuonSum
        MuonSum = TLorentzVector() 
        for Particle in EventDict['PTSorted']['Muons']:
            muon = Particle[1]
            MuonSum += muon.P4()
        ParticleDict = ParticleFuncs.AddParticle('MuonSum', ParticleDict, MuonSum)

        # Checking Zdecays
        EventCutNum += 1
        for Zdecay in Zdecays:
            if Zdecay == None:
                continue
            elif Zdecays[0] == Zdecays[1]:
                continue
            else:
                # If the decay does occur in this process, use an InvMassCheck to decide what particles to tag
                ParticleDict, EventDict = ParticleFuncs.InvMassCheck(Zdecay, 'Z', ParticleDict, EventDict, EventCuts)            

        # Checking W+ decays
        for WPlusdecay in WPlusdecays:
            if WPlusdecay == None:
                continue
            elif WPlusdecay == 'Jets':
                # If the decay is to jets, use an InvMassCheck
                ParticleDict, EventDict = ParticleFuncs.InvMassCheck(WPlusdecay, 'WPlus', ParticleDict, EventDict, EventCuts)          
            else:
                # If the decays is to leptons, take the leading lepton with the correct charge
                WPlusLeptons = EventDict['PTSorted'][WPlusdecay]
                numbWPlusLeptons = len(WPlusLeptons)
                for i in range(0, numbWPlusLeptons):
                    
                    if numbWPlusLeptons != 0:
                        WPlusLepton = WPlusLeptons[i][1]
                        if WPlusLepton.Charge == 1:
                            ParticleDict = ParticleFuncs.AddParticle('WPlus'+WPlusdecay[0:-1], ParticleDict, WPlusLepton.P4(), WPlusLepton.Charge)      
                
                if not ParticleDict['WPlus'+WPlusdecay[0:-1]]['Check']:
                    # If no leptons were tagged (usually due to lack of leptons with correct charge), discard event
                    Continue = True
                            
        # Checking W- decays
        for WMinusdecay in WMinusdecays:
            if WMinusdecay == None:
                continue     
            elif WMinusdecay == 'Jets':
                # If the decay is to jets, use an InvMassCheck            
                ParticleDict, EventDict = ParticleFuncs.InvMassCheck(WMinusdecay, 'WMinus', ParticleDict, EventDict, EventCuts)
            else:
                # If the decays is to leptons, take the leading lepton with the correct charge

                # If the boson could decay to electrons, 
                # differentiation between the beam electron and decay election would have to be implimented
                WMinusLeptons = EventDict['PTSorted'][WMinusdecay]
                numbWMinusLeptons = len(WMinusLeptons)
                for i in range(0, numbWMinusLeptons):
                    
                    if numbWMinusLeptons != 0:
                        WMinusLepton = WMinusLeptons[i][1]
                        if WMinusLepton.Charge == -1:
                            ParticleDict = ParticleFuncs.AddParticle('WMinus'+WMinusdecay[0:-1], ParticleDict, WMinusLepton.P4(), WMinusLepton.Charge)      
                
                if not ParticleDict['WMinus'+WMinusdecay[0:-1]]['Check']:
                    # If no leptons were tagged (usually due to lack of leptons with correct charge), discard event
                    Continue = True

        if Continue:
            # Continue variable is used within loops to indicate whether
            # the event is to be discarded
            ContinueCut += 1
            continue

        # FinalBeamElectron selection
        if len(EventDict['PTSorted']['Electrons']) != 0:
            ParticleDict = ParticleFuncs.AddParticle('FinalBeamElectron', ParticleDict, EventDict['PTSorted']['Electrons'][-1][1].P4())
        else:
            continue

        # FinalBeamElectron cuts
        if ParticleDict['FinalBeamElectron']['Eta'] < AnalysisCuts['FinalBeamElectron']['Eta'][0] or AnalysisCuts['FinalBeamElectron']['Eta'][1] < ParticleDict['FinalBeamElectron']['Eta']:
            continue

        # FinalBeamJet selection
        if len(EventDict['PTSorted']['Jets']) != 0:
            ParticleDict = ParticleFuncs.AddParticle('FinalBeamJet', ParticleDict, EventDict['PTSorted']['Jets'][-1][1].P4())

        # FinalBeamJet cuts
        if ParticleDict['FinalBeamJet']['Pt'] < AnalysisCuts['FinalBeamJet']['Pt'][0] or AnalysisCuts['FinalBeamJet']['Pt'][1] < ParticleDict['FinalBeamJet']['Pt']:
            continue

        # ZJets cuts
        if ParticleDict['ZLeadingJet']['Check']:
            if ParticleDict['ZSubLeadingJet']['Check']:
                # ZJets InvMass cut
                ZJets_M = ( ParticleDict['ZLeadingJet']['P4'] + ParticleDict['ZSubLeadingJet']['P4'] ).M()
                if ZJets_M < AnalysisCuts['ZJets']['M'][0] or AnalysisCuts['ZJets']['M'][1] < ZJets_M:
                    continue
            
        # ZJet-FinalBeamElectron cuts
        if ParticleDict['FinalBeamJet']['Check']:
            if ParticleDict['ZLeadingJet']['Check']:
                ZLeading_FinalBeam_Jets_dR_Eta = ParticleFuncs.GetParticleVariable(ParticleDict, [ParticleDict['ZLeadingJet'], ParticleDict['FinalBeamJet']], 'dR_Eta')
                if ZLeading_FinalBeam_Jets_dR_Eta < AnalysisCuts['ZLeading_FinalBeam_Jets']['dR_Eta'][0] or AnalysisCuts['ZLeading_FinalBeam_Jets']['dR_Eta'][1] < ZLeading_FinalBeam_Jets_dR_Eta:
                    continue

                ZLeading_FinalBeam_Jets_M = ( ParticleDict['ZLeadingJet']['P4'] + ParticleDict['FinalBeamJet']['P4'] ).M()
                if ZLeading_FinalBeam_Jets_M < AnalysisCuts['ZLeading_FinalBeam_Jets']['M'][0] or AnalysisCuts['ZLeading_FinalBeam_Jets']['M'][1] < ZLeading_FinalBeam_Jets_M:
                    continue           

                ZLeading_FinalBeam_Jets_Mt = ( ParticleDict['ZLeadingJet']['P4'] + ParticleDict['FinalBeamJet']['P4'] ).Mt()
                if ZLeading_FinalBeam_Jets_Mt < AnalysisCuts['ZLeading_FinalBeam_Jets']['Mt'][0] or AnalysisCuts['ZLeading_FinalBeam_Jets']['Mt'][1] < ZLeading_FinalBeam_Jets_Mt:
                    continue      

                ZLeading_FinalBeam_Jets_Pt = ( ParticleDict['ZLeadingJet']['P4'] + ParticleDict['FinalBeamJet']['P4'] ).Pt()
                if ZLeading_FinalBeam_Jets_Pt < AnalysisCuts['ZLeading_FinalBeam_Jets']['Pt'][0] or AnalysisCuts['ZLeading_FinalBeam_Jets']['Pt'][1] < ZLeading_FinalBeam_Jets_Pt:
                    continue                                                  

            if ParticleDict['ZSubLeadingJet']['Check']:
                ZSubLeading_FinalBeam_Jets_dR_Eta = ParticleFuncs.GetParticleVariable(ParticleDict, [ParticleDict['ZSubLeadingJet'], ParticleDict['FinalBeamJet']], 'dR_Eta')
                if ZSubLeading_FinalBeam_Jets_dR_Eta < AnalysisCuts['ZSubLeading_FinalBeam_Jets']['dR_Eta'][0] or AnalysisCuts['ZSubLeading_FinalBeam_Jets']['dR_Eta'][1] < ZSubLeading_FinalBeam_Jets_dR_Eta:
                    continue

                ZSubLeading_FinalBeam_Jets_M = ( ParticleDict['ZSubLeadingJet']['P4'] + ParticleDict['FinalBeamJet']['P4'] ).M()
                if ZSubLeading_FinalBeam_Jets_M < AnalysisCuts['ZSubLeading_FinalBeam_Jets']['M'][0] or AnalysisCuts['ZSubLeading_FinalBeam_Jets']['M'][1] < ZSubLeading_FinalBeam_Jets_M:
                    continue            

                ZSubLeading_FinalBeam_Jets_Mt = ( ParticleDict['ZSubLeadingJet']['P4'] + ParticleDict['FinalBeamJet']['P4'] ).Mt()
                if ZSubLeading_FinalBeam_Jets_Mt < AnalysisCuts['ZSubLeading_FinalBeam_Jets']['Mt'][0] or AnalysisCuts['ZSubLeading_FinalBeam_Jets']['Mt'][1] < ZSubLeading_FinalBeam_Jets_Mt:
                    continue     

                ZSubLeading_FinalBeam_Jets_Pt = ( ParticleDict['ZSubLeadingJet']['P4'] + ParticleDict['FinalBeamJet']['P4'] ).Pt()
                if ZSubLeading_FinalBeam_Jets_Pt < AnalysisCuts['ZSubLeading_FinalBeam_Jets']['Pt'][0] or AnalysisCuts['ZSubLeading_FinalBeam_Jets']['Pt'][1] < ZSubLeading_FinalBeam_Jets_Pt:
                    continue                                                          

        # Adds particle for W+ - W- muons and W+ - Electron 
        if ParticleDict['WPlusMuon']['Check'] and ParticleDict['WMinusMuon']['Check']:
            DiMuon = ParticleDict['WPlusMuon']['P4'] + ParticleDict['WMinusMuon']['P4']
            WPlusMuonFinalBeamElectron = ParticleDict['WPlusMuon']['P4'] + ParticleDict['FinalBeamElectron']['P4']
            ParticleDict = ParticleFuncs.AddParticle('DiMuon', ParticleDict, DiMuon)
            ParticleDict = ParticleFuncs.AddParticle('WPlusMuonFinalBeamElectron', ParticleDict, WPlusMuonFinalBeamElectron)

        # Adds particle for W+ - W- muons and W+ - Electron 
        if ParticleDict['WMinusMuon']['Check']:
            WMinusMuon_qLepton = GetParticleVariable(ParticleDict, [ParticleDict['WMinusMuon']], 'qLepton')
            FinalBeamElectron_qLepton = GetParticleVariable(ParticleDict, [ParticleDict['FinalBeamElectron']], 'qLepton')

            # Keeps track of how many events have correct
            # selection of the beam electron vs the decay muon
            if FinalBeamElectron_qLepton < WMinusMuon_qLepton:
                BeamElectronSelection += 1

        # Filling HistDict with particles then filling the hists
        HistDict = ParticleFuncs.RequestParticles(HistDict, ParticleDict)
        HistFuncs.FillHists(HistDict, ParticleDict)

        EventKeptNum += 1

    # Get scaling factor for histograms
    # L_int(Data) = 1 [ab-1] = 1000000 [pb-1]
    # L_int(MC) = N/Xsec [pb-1]
    # Scale = L_int(Data) / L_int(MC)
    Scale = 1000000 / (TreeDict['NEvents']/Xsec)

    # Scaling and altering hist lims
    for category, attributes in HistDict.items():
        for var, hist in attributes['Hists'].items():
            hist = HistFuncs.HistLims(hist, category, var, Scale=Scale, Diff2D=False)[0]

    # Writing and closing file
    outfile.Write()
    outfile.Close()
    gSystem.Exec('rootprint -f png -d '+outfilename+'/ '+outfilename+'.root')

    print('NEvents kept =', EventKeptNum)
    print('NEvents where boson cut discaded event =', ContinueCut)
    print('NEvents where beam electron correctly selected =', BeamElectronSelection)
