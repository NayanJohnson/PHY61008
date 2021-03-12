
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

def GetScale(PythiaLogPath, NEvents):
    '''
        Given the parth to the pythia log file and the number of events,
        will return the scaling factor calculated from the process 
        cross section. 
    '''

    with open(PythiaLogPath, "r") as file:
        lines = file.read().splitlines()
        # Xsec is the last element of the last line
        Xsec = float(lines[-1].split()[-1])
    
    # L_int (Data) = 1 [ab-1] = 1000000 [pb-1]
    # L_int (MC) = N/Xsec [pb-1]
    Scale = 1000000 / (NEvents/Xsec)

    return Scale

def MakeHists(HistDict, Scale):
    '''
        Given a dictionary with names being keys for a list histogram
        properties:
        HistDict = {
            name    :   {
                'Vars'  :   []
            }
        }
        Will use the 'Vars' list to initialise histograms and add them
        to the dictionary.
    '''

    for name, properties in HistDict.items():
        properties['Hists'] = {}
        for var in properties['Requests']['Vars']:
            hist = None
            
            # Checks the variable and initialises a custom histogram
            # Set the limits much larger than they need to be since they're reset later
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
                hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 1000, 0, 1000)
            
            elif var == 'Et':
                hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 1500, 0, 1500)

            elif var == 'q':
                hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 1000, 0, 10000)

            elif var == 'dR_Eta' or var == 'dR_Rap':
                hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 1000, 0, 100)
            
            elif var == 'InvMass':
                hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 2000, 0, 10000)
            
            # Scales the histogram forces the graph to be drawn as 'hist'
            hist.Scale(Scale)
            hist.SetOption('hist')
            # Adds the hist to the dict
            HistDict[name]['Hists'][var] = hist
    
    return HistDict

def RequestParticles(HistDict, ParticleDict):
    '''
        Adds requested particles to the HistDict
    '''

    # Itterating through histogram categories
    for category, properties in HistDict.items():
        
        # Itterating through particle requests
        for particle in properties['Requests']['Particles']:

            # Special check for AllJet request
            # Ignore BeamJet to prevent double counting
            if particle == 'AllJets' and particle != 'BeamJet':
                for key, jet in ParticleDict.items():
                    if jet['Check']:
                        if jet['isJet']:
                            properties['Particles'].append(jet)

            # Normal particle check
            elif ParticleDict[particle]['Check']:
                properties['Particles'].append(ParticleDict[particle])               

    return HistDict

def FillHists(HistDict):
    '''
        Given a dictionary of histograms, will fill them.
        Histogram dictionary should be in the following format:
        HistDict = {
            Catagory    :   {
                vars    :   [],
                particles   :   {}
                hists       :   {
                    var     :   hist
                }
            }
        }
    '''
    
    # List of variables that are stored in all particles.
    ParticleProperties = ['PID', 'E', 'Eta', 'Phi', 'Rapidity', 'Theta', 'Pt', 'Et']

    for catagory, properties in HistDict.items():
        for var, hist in properties['Hists'].items():

            # Checks the variable and fills the histogram
            if var == 'Count': 
                hist.Fill(properties['Count'])

            # Variables that can be calculated from one or multiple
            # particles.
            if len(properties['Particles']) != 0:
                if var in ParticleProperties:
                    for i in range(0, len(properties['Particles'])):
                        hist.Fill(properties['Particles'][i][var])
                elif var == 'InvMass':
                    ParticleSum = TLorentzVector()
                    for paritcle in properties['Particles']:
                        ParticleSum = paritcle['P4'] + ParticleSum
                    hist.Fill(ParticleSum.M())

            # Seperates hists into the number of required particles
            if len(properties['Particles']) == 2:

                if var == 'q':
                    if catagory == 'q_Lepton' or catagory == 'q_Quark':
                        q = (properties['Particles'][0]['P4'] - properties['Particles'][1]['P4']).Mag()
                    elif catagory == 'q_eMethod':
                        q = TMath.Sqrt(2*properties['Particles'][0]['E']*properties['Particles'][1]['E']*(1 - TMath.Cos(properties['Particles'][0]['Theta'])))
                    hist.Fill(abs(q))

                elif var == 'dEta':
                    dEta = properties['Particles'][0]['Eta'] - properties['Particles'][1]['Eta']
                    hist.Fill(dEta)
                
                elif var == 'dPhi':
                    dPhi = properties['Particles'][0]['P4'].DeltaPhi(properties['Particles'][1]['P4'])
                    hist.Fill(dPhi)

                elif var == 'dRapidity':
                    dRap = properties['Particles'][0]['Rapidity'] - properties['Particles'][1]['Rapidity']
                    hist.Fill(dRap)

                elif var == 'dR_Eta':
                    dR_Eta = properties['Particles'][0]['P4'].DrEtaPhi(properties['Particles'][1]['P4'])
                    hist.Fill(dR_Eta)

                elif var == 'dR_Rap':
                    dPhi = properties['Particles'][0]['P4'].DeltaPhi(properties['Particles'][1]['P4'])
                    dRap = properties['Particles'][0]['Rapidity'] - properties['Particles'][1]['Rapidity']
                    # DrRapidityPhi function doesnt seem to work
                    dR_Rap = TMath.Sqrt( dPhi**2 + dRap**2 )
                    hist.Fill(dR_Rap)                          

def HistLims(HistDict):
    '''
        Rescales hist lims depending on the data in the hists
    '''
    for Catagory, HistSubDict in HistDict.items():
        for var, hist in HistSubDict['Hists'].items():

            # Get the index of the min/max bin and the read off the value of the 
            # low edge
            # Set FindLastBinAbove threshold to 5 since otherwise the 
            # hist goes on for way too long
            BinMax = hist.GetBinLowEdge(hist.FindLastBinAbove(5))
            BinMin = hist.GetBinLowEdge(hist.FindFirstBinAbove())
            # Max/min = BinMax/min +- 5% +- 5 (prevents max=min for BinMax/Min=0)
            XMax = BinMax + abs(BinMax/10) + 5
            XMin = BinMin - abs(BinMin/10) - 5
            hist.SetAxisRange(XMin, XMax)


def AddParticle(name, ParticleDict, P4=None, PID=None, isJet=False):
        '''
            Given a name, PID, 4-momenta of a particle,
            will add a particle dict of various properties to an existing
            dict:
            ParticleDict[name] = {
                'Check'     :   check,
                'Name'      :   name,
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
        '''

        # Checks if a particle is present
        if P4 == None:
            ParticleDict[name] = {
                'Check'     :   False
            }

        else:
            ParticleDict[name] = {
                'Check'     :   True,
                'Name'      :   name,
                'PID'       :   PID,
                'P4'        :   P4,
                'E'         :   P4.E(),
                'Eta'       :   P4.Eta(),
                'Phi'       :   P4.Phi(),
                'Rapidity'  :   P4.Rapidity(),
                'Theta'     :   P4.Theta(),
                'Pt'        :   P4.Pt(),
                'Et'        :   P4.Et(),
                'isJet'     :   isJet,
            }
        
        return ParticleDict


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
            jet_count += 1
            JetPT.append( ( jet.PT, jet) )
    
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