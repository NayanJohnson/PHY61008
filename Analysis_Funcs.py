
from ROOT import gSystem, gInterpreter

# Path of Delphes directory 
gSystem.AddDynamicPath("/home/nayan/MG5_aMC_v2_8_2/Delphes/")
gSystem.Load("libDelphes")

gInterpreter.Declare('#include "classes/DelphesClasses.h"')
gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')

from ROOT import TChain, ExRootTreeReader, TH1F, TMath


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
    Events = myTree.GetEntries()

    # Get pointers to branches used in this analysis
    branchParticle = myTree.UseBranch("Particle")
    branchGenJets = myTree.UseBranch("GenJet")
    branchMissingET = myTree.UseBranch("MissingET")

    TreeDict =  {
                    'Tree'      :   myTree,
                    'Events'    :   Events,
                    'Branches'  :   {
                        'Particle'          :   branchParticle,
                        'GenJets'           :   branchGenJets,
                        'MissingET'   :   branchMissingET
                    }
                }

    return TreeDict



def Histograms(name, Nbins=200, HistVariables=['Eta', 'Phi', 'Rapidity', 'PT'], HistLimits=[(-10, 10), (-3.5, 3.5), (-10, 10), (-200, 300)]):
    '''
    Takes:
    - name:str() base name of histogram.
    - Nbins:int() Number of bins in each histogram.
    - HistVariables:list(str(), str(), ...) List of the variables plotted in each histogram
    - HistLimits:list(tuple(2), tuple(2), ...) List of tuples length two. Each tuple represents the 
        min and max values of the corresponding variable. In the same order as HistVariables.

    Returns a list of all hists in the same order as HistVariables.
    '''
    
    Hists = []

    # Loops through all variables in HistVariables list
    for i in range(len(HistVariables)):
        
        variable = str(HistVariables[i])
        h = TH1F(str(name)+'_'+variable, str(name)+'_'+variable+';'+variable+';Frequency', Nbins, HistLimits[i][0], HistLimits[i][1])
        Hists.append(h)

    
    return Hists


def Comparison(A, B, Eta=True, Phi=True, Rapidity=True, R_Eta=True, R_Rap=True):
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

def InvMass(Particles):
    '''
    Given a list of particles, will calculate the invariant mass.
    '''

    Momenta = []
    for particle in Particles:
        Momenta.append((particle.E, particle.Px, particle.Py, particle.Pz))

    ESum = sum([x[0] for x in Momenta])
    PxSum = sum([x[1] for x in Momenta])
    PySum = sum([x[2] for x in Momenta])
    PzSum = sum([x[3] for x in Momenta])
    
    InvMass = ( ESum**2 - PxSum**2 - PySum**2 - PzSum**2 )**0.5
    return InvMass

def ParticleLoop(TreeDict, EventNum):
    '''
    '''

    TreeDict['Tree'].ReadEntry(EventNum)

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
    
    
    # Loop through generated particles
    for i in range(TreeDict['Branches']['Particle'].GetEntries()) :
        particle = TreeDict['Branches']['Particle'].At(i)        
                    
        # i == 0 corresponds to beam quark
        # i == 1 corresponds to beam electron
        if i == 1:         
            BeamElectron = particle
                    
        # Final state particles                
        if particle.Status == 1:
            
            # Electrons and positrons
            if abs(particle.PID) == 11:
                # Adding the particle to the final state list
                FinalLeptons.append(particle)                
                e_count += 1

                # Adding the electron to the sorting list 
                ElectronPT.append( (particle.PT, particle) )
                
            # Selecting mu
            elif abs(particle.PID) ==  13:                
                # Adding the particle to the final state list
                FinalLeptons.append(particle)              
                mu_count += 1                
                
                # Adding the muon to the sorting list                 
                MuonPT.append( (particle.PT, particle) )      
                
            # Selecting neutrinos
            elif abs(particle.PID) == 12 or abs(particle.PID) == 14:
                 FinalLeptons.append(particle)
                
            
        # Loop through generated Jets
    for i in range(TreeDict['Branches']['GenJets'].GetEntries()):
        jet = TreeDict['Branches']['GenJets'].At(i)
        
        # Keeps track of how many particles the jet overlaps with
        Overlap = 0
        
        # Compare to final state leptons to look for overlap
        for particle in FinalLeptons:
            
            # Only need dEta and dPhi
            # JetLepton = comparison(A=jet, B=particle, dEta=True, dPhi=True, dRapidity=False, dR=False)
            JetLepton = Comparison(jet, particle, True, True, False, True, False)
            
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
    MuonPT_sorted = sorted(MuonPT, key=lambda x: x[0])
    JetPT_sorted = sorted(JetPT, key=lambda x: x[0])

    EventDict   =   {
        'Count'     :   {
            'Electron'  :   e_count,
            'Muon'      :   mu_count,
            'Jet'       :   jet_count
        },
        'BeamElectron'  :   BeamElectron,
        'PTSorted'  :   {
            'Electron'  :   ElectronPT_sorted,
            'Muon'      :   MuonPT_sorted,
            'Jet'       :   JetPT_sorted
        }
    }

    return EventDict