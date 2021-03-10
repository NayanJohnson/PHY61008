
from ROOT import gSystem, gInterpreter, TChain, TH1F, TMath, TLorentzVector

# Path of Delphes directory 
gSystem.AddDynamicPath("/home/nayan/MG5_aMC_v2_8_2/Delphes/")
gSystem.Load("libDelphes")

gInterpreter.Declare('#include "classes/DelphesClasses.h"')
gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')

from ROOT import ExRootTreeReader

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

def GetXSec(PythiaLogPath):
    '''
        Given the parth to the pythia log file, will return the cross section
        of the process. 
    '''

    with open(PythiaLogPath, "r") as file:
        lines = file.read().splitlines()
        # Xsec is the last element of the last line
        Xsec = float(lines[-1].split()[-1])

    return Xsec

def MakeHists(HistDict, Scale):
    '''
        Given a dictionary with names being keys for a list of variables.
    '''

    for name, properties in HistDict.items():
        for var in properties['Vars']:
            hist = None
            
            if var == 'Count': 
                hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 200, 0, 10)
            
            elif var == 'Eta':
                hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 200, -10, 10)
            
            elif var == 'dEta':
                hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 200, -20, 20)

            elif var == 'Phi' or var == 'dPhi':
                hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 200, -3.5, 3.5)

            elif var == 'Rapidity':
                hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 200, -10, 10)
            
            elif var == 'dRapidity':
                hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 200, -20, 20)

            elif var == 'Pt':
                hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 200, 0, 200)
            
            elif var == 'Et':
                hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 200, 0, 200)

            elif var == 'q':
                hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 200, 0, 1200)

            elif var == 'dR_Eta' or var == 'dR_Rap':
                hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 200, 0, 10)
            
            elif var == 'InvMass':
                hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 200, 0, 1000)
            hist.Scale(Scale)
            hist.SetOption('hist')
            HistDict[name]['Hists'][var] = hist
    
    return HistDict
    
def FillHists(HistDict):
    '''
        Given a dictionary of histograms, will fill them.
        Histogram dictionary should be in the following format:
        HistDict = {
            HistCatagory    :   {
                vars    :   [],
                particles   :   {}
                hists       :   {
                    var     :   hist
                }
            }
        }
    '''
    
    ParticleProperties = ['PID', 'E', 'Eta', 'Phi', 'Rapidity', 'Theta', 'Pt', 'Et']

    for Catagory, HistSubDict in HistDict.items():
        if len(HistSubDict['Particles']) != 0:
            for var, hist in HistSubDict['Hists'].items():
                if var == 'Count': 
                    hist.Fill(HistSubDict['Count'])

                elif var in ParticleProperties:
                    # print(Catagory, var)
                    hist.Fill(HistSubDict['Particles'][0][var])

                elif var == 'q':
                    if Catagory == 'q_Lepton' or Catagory == 'q_Quark':
                        q = (HistSubDict['Particles'][0]['P4'] - HistSubDict['Particles'][1]['P4']).Mag()
                    elif Catagory == 'q_eMethod':
                        q = TMath.Sqrt(2*HistSubDict['Particles'][0]['E']*HistSubDict['Particles'][1]['E']*(1 - TMath.Cos(HistSubDict['Particles'][0]['Theta'])))
                    hist.Fill(abs(q))

                elif var == 'dEta':
                    dEta = HistSubDict['Particles'][0]['Eta'] - HistSubDict['Particles'][1]['Eta']
                    hist.Fill(dEta)
                
                elif var == 'dPhi':
                    dPhi = HistSubDict['Particles'][0]['P4'].DeltaPhi(HistSubDict['Particles'][1]['P4'])
                    hist.Fill(dPhi)

                elif var == 'dRapidity':
                    dRap = HistSubDict['Particles'][0]['Rapidity'] - HistSubDict['Particles'][1]['Rapidity']
                    hist.Fill(dRap)

                elif var == 'dR_Eta':
                    dR_Eta = HistSubDict['Particles'][0]['P4'].DrEtaPhi(HistSubDict['Particles'][1]['P4'])
                    hist.Fill(dR_Eta)
                elif var == 'dR_Rap':
                    dPhi = HistSubDict['Particles'][0]['P4'].DeltaPhi(HistSubDict['Particles'][1]['P4'])
                    dRap = HistSubDict['Particles'][0]['Rapidity'] - HistSubDict['Particles'][1]['Rapidity']
                    # DrRapidityPhi function doesnt seem to work
                    dR_Rap = TMath.Sqrt( dPhi**2 + dRap**2 )
                    hist.Fill(dR_Rap)                          
                
                elif var == 'InvMass':
                    ParticleSum = TLorentzVector()
                    for paritcle in HistSubDict['Particles']:
                        ParticleSum = paritcle['P4'] + ParticleSum
                    hist.Fill(ParticleSum.M())

def DictMerge(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def AddParticle(name, PID, P4, OldDict):
        '''
            Given a dictionary with names being keys for a list of variables.
        '''

        ParticleDict = {
            name    :   {
                'name'      :   name,
                'PID'       :   PID,
                'P4'        :   P4,
                'E'         :   P4.E(),
                'Eta'       :   P4.Eta(),
                'Phi'       :   P4.Phi(),
                'Rapidity'  :   P4.Rapidity(),
                'Theta'     :   P4.Theta(),
                'Pt'        :   P4.Pt(),
                'Et'        :   P4.Et()
            }

        }
        
        NewDict = DictMerge(ParticleDict, OldDict)
        return NewDict

def ParticleLoop(TreeDict, EventNum):
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

    # Reading a specific event 
    TreeDict['Tree'].ReadEntry(EventNum)

    # Number ot particular particles in eventNbins
    e_count = 0
    mu_count = 0
    jet_count = 0
    
    # List of all final state leptons
    FinalLeptons = []
    
    # Neutrino 4momentum list
    Neutrinos_P = []

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
                Neutrinos_P.append(particle.P4())
                FinalLeptons.append(particle)
                
            
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
            jet_count += 1
            JetPT.append( ( jet.PT, jet) )
    
    # Sorts ElectronPT based on the 1st element in each tuple in ascending order
    ElectronPT_sorted = sorted(ElectronPT, key=lambda x: x[0])
    MuonPT_sorted = sorted(MuonPT, key=lambda x: x[0])
    JetPT_sorted = sorted(JetPT, key=lambda x: x[0])

    # MissingE is the sum of all neutrino momenta in the event
    MissingE_P = TLorentzVector()
    for neutrino in Neutrinos_P:
        neutrino.SetPz(0)
        neutrino.SetE(neutrino.Et())
        MissingET_P = MissingE_P + neutrino

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