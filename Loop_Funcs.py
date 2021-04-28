# Needed to allow use of kInfo, gErrorIgnoreLevel
import ROOT
class Quiet:
    """Context manager for silencing certain ROOT operations.  Usage:
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

# Path of Delphes directory 
gSystem.AddDynamicPath('/home/nayan/MG5_aMC_v2_8_2/Delphes/')
gSystem.Load('libDelphes')

gInterpreter.Declare('#include "classes/DelphesClasses.h"')
gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')

from ROOT import ExRootTreeReader

import config, requests, itertools
import Particle_Funcs as ParticleFuncs
import Hist_Funcs as HistFuncs

'''
Definitions of used objects:

TreeDict =  {
    'Tree'          :       chain,
    'TreeReader'    :       TreeDict,
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
    'MissingET'   :   MissingET,
    'PTSorted'  :   {
        'Electron'  :   ElectronPT_sorted,
        'Muon'      :   MuonPT_sorted,
        'Jet'       :   JetPT_sorted
    }
}

'''


def LoadTrees(TreeList, prefix):
    '''
    Loads .root file with tree labeled 'Delphes' and outputs dictionary containing the number 
    of events and branches.
    '''

    # Create chain of root trees 
    chain = TChain('Delphes')
    for tree in TreeList:
        chain.Add(tree)

    # Create object of class ExRootTreeReader
    TreeReader = ExRootTreeReader(chain)

    if prefix=='Signal' or prefix=='Background':
        NEvents = config.EventLoopParams[prefix]['NEvents']
    else:
        NEvents = TreeReader.GetEntries()
    # Get pointers to branches used in this analysis
    branchParticle = TreeReader.UseBranch('Particle')
    branchGenJet = TreeReader.UseBranch('GenJet')
    branchElectron = TreeReader.UseBranch('Electron')
    branchMuon = TreeReader.UseBranch('Muon')
    branchJet = TreeReader.UseBranch('Jet')
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

    Cuts = config.EventLoopParams['Level']['Loop'][LoopRun]

    # Reading a specific event 
    TreeDict['TreeReader'].ReadEntry(EventNum)

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
            
        BeamElectron = TLorentzVector(0, 0, -50, 50)
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
    '''

    ParticleKeywords = requests.ParticleKeywords
    # Reset particle list for the new event
    for _, dictionary in HistDict.items():
        dictionary['Particles'] = []
        
    # Reset ParticeDict for this event
    ParticleDict = {}
    for keyword in ParticleKeywords:
        ParticleDict = ParticleFuncs.AddParticle(keyword, ParticleDict)

    # Particle loop with cuts
    EventDict = ParticleLoop(TreeDict, EventNum, LevelRun, LoopRun)

    # Adding BeamElectron and BeamQuark
    ParticleDict = ParticleFuncs.AddParticle('BeamElectron', ParticleDict, EventDict['BeamElectron'])
    ParticleDict = ParticleFuncs.AddParticle('BeamQuark', ParticleDict, EventDict['BeamQuark'])

    # FinalElectron
    numbElectrons = EventDict['Count']['Electrons']
    for i in range(0, numbElectrons):
        # Checking that there is at least one electron present
        if numbElectrons != 0:
            LeadingElectron = EventDict['PTSorted']['Electrons'][-1][1]
            ParticleDict = ParticleFuncs.AddParticle('LeadingElectron', ParticleDict, LeadingElectron.P4())

    # Leading and SubLeading muons
    numbMuons = EventDict['Count']['Muons']
    for i in range(0, numbMuons):

        # Checking that there is at least one muon present
        if numbMuons != 0:
            Muon = EventDict['PTSorted']['Muons'][i][1]
            # Leading Muon
            if i == numbMuons - 1:
                ParticleDict = ParticleFuncs.AddParticle('LeadingMuon', ParticleDict, Muon.P4(), Muon.Charge)

            # SubLeading Muon
            elif i == numbMuons - 2 and numbMuons - 2 >= 0:
                ParticleDict = ParticleFuncs.AddParticle('SubLeadingMuon', ParticleDict, Muon.P4(), Muon.Charge)

            elif i == numbMuons - 3 and numbMuons - 3 >= 0:
                ParticleDict = ParticleFuncs.AddParticle('ThirdMuon', ParticleDict, Muon.P4(), Muon.Charge)

    # Jets
    numbJets = EventDict['Count']['Jets']
    for i in range(0, numbJets):
        
        # Checking that there is at least one jet present
        if numbJets != 0:
            Jet = EventDict['PTSorted']['Jets'][i][1]

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
    ParticleDict = ParticleFuncs.AddParticle('MissingET', ParticleDict, EventDict['MissingET'])

    # Count hists
    HistDict['Electrons']['Count'] = numbElectrons
    HistDict['Muons']['Count'] = numbMuons
    HistDict['Jets']['Count'] = numbJets

    return HistDict, ParticleDict, EventDict

def EventLoop(TreeDict, Xsec, outfilename, LevelRun, LoopRun, EventRun, AnalysisRun):
    '''
    '''

    # Open output
    outfile = TFile(outfilename+'.root','RECREATE')

    HistDict = requests.HistDict

    # Initialise requested hists from HistDict
    HistDict = HistFuncs.MakeHists(HistDict)

    EventCuts = config.EventLoopParams['Level']['Event'][EventRun]
    AnalysisCuts = config.EventLoopParams['Level']['Analysis'][AnalysisRun] 

    Zdecays = config.EventLoopParams['Z']['Decays']
    WPlusdecays = config.EventLoopParams['WPlus']['Decays']
    WMinusdecays = config.EventLoopParams['WMinus']['Decays']
    
    EventCutNum = 0
    # Looping through events
    for EventNum in range(TreeDict['TreeReader'].GetEntries()):
        
        if EventNum % 10000 == 0:
            print(EventNum, ' events completed.')

        HistDict, ParticleDict, EventDict = GetParticles(TreeDict, LevelRun, LoopRun, HistDict, EventNum)
        
        # MissingET cuts
        if EventDict['MissingET'].Et() < AnalysisCuts['MissingET']['Et'][0] or AnalysisCuts['MissingET']['Et'][1] < EventDict['MissingET'].Et():
            continue

        # LeadingJet SubLeadingJet Cut
        if ParticleDict['LeadingJet']['Check']:
            if ParticleDict['LeadingJet']['Pt'] < AnalysisCuts['LeadingJet']['Pt'][0] or AnalysisCuts['LeadingJet']['Pt'][1] < ParticleDict['LeadingJet']['Pt']:
                continue
        if ParticleDict['SubLeadingJet']['Check']:
            if ParticleDict['SubLeadingJet']['Pt'] < AnalysisCuts['SubLeadingJet']['Pt'][0] or AnalysisCuts['SubLeadingJet']['Pt'][1] < ParticleDict['SubLeadingJet']['Pt']:
                continue        

        # Event cuts
        if EventDict['Count']['Electrons'] < EventCuts['Electrons'] or EventDict['Count']['Muons'] < EventCuts['Muons'] or EventDict['Count']['Jets'] < EventCuts['Jets']:
            continue

        # MuonSum
        MuonSum = TLorentzVector() 
        for Particle in EventDict['PTSorted']['Muons']:
            muon = Particle[1]
            MuonSum += muon.P4()
        ParticleDict = ParticleFuncs.AddParticle('MuonSum', ParticleDict, MuonSum)

        EventCutNum += 1
        for Zdecay in Zdecays:
            if Zdecay == None:
                continue
            elif Zdecays[0] == Zdecays[1]:
                continue
            else:
                ParticleDict, EventDict, Continue = ParticleFuncs.InvMassCheck(Zdecay, 'Z', ParticleDict, EventDict, EventCuts)
                if Continue:
                    continue                

        for WPlusdecay in WPlusdecays:
            if WPlusdecay == None:
                continue
            elif WPlusdecays[0] == WPlusdecays[1]:
                continue            
            elif WPlusdecay == 'Jets':
                ParticleDict, EventDict, Continue = ParticleFuncs.InvMassCheck(WPlusdecay, 'WPlus', ParticleDict, EventDict, EventCuts)
                if Continue:
                    continue                
            else:
                particlesList = [ParticleDict['Leading'+WPlusdecay[0:-1]], ParticleDict['SubLeading'+WPlusdecay[0:-1]]]
                for Lepton in particlesList:
                    if Lepton['Check']:
                        if Lepton['Charge'] == 1:
                            ParticleDict = ParticleFuncs.AddParticle('WPlus'+WPlusdecay[0:-1], ParticleDict, Lepton['P4'])

        for WMinusdecay in WMinusdecays:
            if WMinusdecay == None:
                continue
            elif WMinusdecays[0] == WMinusdecays[1]:
                continue            
            elif WMinusdecay == 'Jets':
                ParticleDict, EventDict, Continue = ParticleFuncs.InvMassCheck(WMinusdecay, 'WMinus', ParticleDict, EventDict, EventCuts)
                if Continue:
                    continue
            else:
                particlesList = [ParticleDict['Leading'+WMinusdecay[0:-1]], ParticleDict['SubLeading'+WMinusdecay[0:-1]]]
                for Lepton in particlesList:
                    if Lepton['Check']:
                        if Lepton['Charge'] == -1:
                            ParticleDict = ParticleFuncs.AddParticle('WMinus'+WMinusdecay[0:-1], ParticleDict, Lepton['P4'])      
           

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



        # Adds particle for W+ - W- muons and W+ - Electron 
        if ParticleDict['WPlusMuon']['Check'] and ParticleDict['WMinusMuon']['Check']:
            DiMuon = ParticleDict['WPlusMuon']['P4'] + ParticleDict['WMinusMuon']['P4']
            WPlusMuonFinalBeamElectron = ParticleDict['WPlusMuon']['P4'] + ParticleDict['FinalBeamElectron']['P4']
            ParticleDict = ParticleFuncs.AddParticle('DiMuon', ParticleDict, DiMuon)
            ParticleDict = ParticleFuncs.AddParticle('WPlusMuonFinalBeamElectron', ParticleDict, WPlusMuonFinalBeamElectron)

        # Filling HistDict with particles then filling the hists
        HistDict = ParticleFuncs.RequestParticles(HistDict, ParticleDict)
        HistFuncs.FillHists(HistDict, ParticleDict)

    # Get scaling factor for histograms
    Scale = HistFuncs.GetScale(Xsec, TreeDict['NEvents'])

    # Scaling and altering hist lims
    for category, attributes in HistDict.items():
        for var, hist in attributes['Hists'].items():
            hist = HistFuncs.HistLims(hist, category, var, Scale=Scale)[0]

    # Writing and closing file
    outfile.Write()
    outfile.Close()
    gSystem.Exec('rootprint -f png -d '+outfilename+'/ '+outfilename+'.root')
