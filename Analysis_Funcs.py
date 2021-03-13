
from ROOT import gSystem, gInterpreter, TChain, TH1F, TH2F, TMath, TLorentzVector, TCanvas, TLegend, SetOwnership, TColor

# Path of Delphes directory 
gSystem.AddDynamicPath("/home/nayan/MG5_aMC_v2_8_2/Delphes/")
gSystem.Load("libDelphes")

gInterpreter.Declare('#include "classes/DelphesClasses.h"')
gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')

from ROOT import ExRootTreeReader
import config


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
    VarParams = config.VarParams
    histNbins = VarParams['Nbins']

    for name, properties in HistDict.items():
        properties['Hists'] = {}

        for var in properties['Requests']['Vars']:
            
            # If var is a tuple the hist is multiple dims
            if type(var) == tuple:
                if len(var) == 2:
                    histName = name+'_'+var[0]+'_'+var[1]
                    histTitle = histName+';'+var[0]+';'+var[1]+';Frequency'
                    histXlow = VarParams[var[0]]['Range'][0]
                    histXup = VarParams[var[0]]['Range'][1]
                    histYlow = VarParams[var[1]]['Range'][0]
                    histYup = VarParams[var[1]]['Range'][1]        

                    hist = TH2F(histName, histTitle, histNbins, histXlow, histXup, histNbins, histYlow, histYup)
                    
                    # Scales the histogram forces the graph to be drawn as 'hist'
                    hist.Scale(Scale)
                    hist.SetOption('HIST COLZ')
                    # Adds the hist to the dict
                    HistDict[name]['Hists'][var[0]+'_'+var[1]] = hist

            elif type(var) == str:
                histName = name+'_'+var
                histTitle = histName+';'+var+';Frequency'
                histXlow = VarParams[var]['Range'][0]
                histXup = VarParams[var]['Range'][1]
                 
                hist = TH1F(histName, histTitle, histNbins, histXlow, histXup)


                # Scales the histogram forces the graph to be drawn as 'hist'
                hist.Scale(Scale)
                hist.SetOption('HIST')
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
            
            # If var contains 2 variables
            if len(var.split('_')) == 2:
                xVar = GetVariable(catagory, var.split('_')[0], properties, 2)
                yVar = GetVariable(catagory, var.split('_')[1], properties, 2)
                if xVar and yVar:
                    hist.Fill(xVar, yVar)

            else:
                xVar = GetVariable(catagory, var, properties)
                if xVar != False:
                    # If the function returns a list fill the hist for each
                    # element in list
                    if type(xVar) == list:
                        for V in xVar:
                            hist.Fill(V)
                    else:
                        hist.Fill(xVar)


def GetVariable(catagory, var, properties, dims=1):
    '''
    '''

    # List of variables that are stored in all particles.
    ParticleProperties = ['PID', 'E', 'Eta', 'Phi', 'Rapidity', 'Theta', 'Pt', 'Et']

    # Checks the variable and fills the histogram
    if var == 'Count': 
        return properties['Count']

    # Variables that can be calculated from one or multiple
    # particles.
    if len(properties['Particles']) != 0:

        # Variables in ParticleProperties only require one particle so
        # the hist can be filled by all particles in the list.
        if var in ParticleProperties:
            # Only alow 1D hists to return a list
            if dims ==1:
                ParticleVars = []
                for i in range(0, len(properties['Particles'])):
                    ParticleVars.append(properties['Particles'][i][var])
                return ParticleVars
            else:
                return properties['Particles'][0][var]

        elif var == 'InvMass':
            ParticleSum = TLorentzVector()
            for paritcle in properties['Particles']:
                ParticleSum = paritcle['P4'] + ParticleSum
            return ParticleSum.M()

    # Seperates hists into the number of required particles
    if len(properties['Particles']) == 2:

        if var == 'q':
            if catagory == 'qLepton' or catagory == 'qQuark':
                q = (properties['Particles'][0]['P4'] - properties['Particles'][1]['P4']).Mag()
            elif catagory == 'qeMethod':
                q = TMath.Sqrt(2*properties['Particles'][0]['E']*properties['Particles'][1]['E']*(1 - TMath.Cos(properties['Particles'][0]['Theta'])))
            return abs(q)

        elif var == 'dEta':
            dEta = properties['Particles'][0]['Eta'] - properties['Particles'][1]['Eta']
            return dEta
        
        elif var == 'dPhi':
            dPhi = properties['Particles'][0]['P4'].DeltaPhi(properties['Particles'][1]['P4'])
            return dPhi

        elif var == 'dRapidity':
            dRap = properties['Particles'][0]['Rapidity'] - properties['Particles'][1]['Rapidity']
            return dRap

        elif var == 'dR_Eta':
            dR_Eta = properties['Particles'][0]['P4'].DrEtaPhi(properties['Particles'][1]['P4'])
            return dR_Eta

        elif var == 'dR_Rap':
            dPhi = properties['Particles'][0]['P4'].DeltaPhi(properties['Particles'][1]['P4'])
            dRap = properties['Particles'][0]['Rapidity'] - properties['Particles'][1]['Rapidity']
            # DrRapidityPhi function doesnt seem to work
            dR_Rap = TMath.Sqrt( dPhi**2 + dRap**2 )
            return dR_Rap    
    return False

def GetDivisors(n):
    '''
    '''
    Divisors = []
    i = 1
    while i <= n : 
        if (n % i==0) : 
            Divisors.append(i), 
        i += 1
    return Divisors

def HistLims(HistDict):
    '''
        Rescales hist lims depending on the data in the hists
    '''

    # Will return a list of the dividers of NBins
    

    for catagory, properties in HistDict.items():
        for var, hist in properties['Hists'].items():

            # Skip if hist = False
            if hist:
                if hist.GetDimension() == 1:
                    
                    # First version of Max Min using a threshold of 0 since the 
                    # bin width is very small
                    BinMaxX = hist.GetBinLowEdge(hist.FindLastBinAbove(0, 1)) + 1
                    BinMinX = hist.GetBinLowEdge(hist.FindFirstBinAbove(0, 1))

                    # Rescales bin number so the plotted range has Nbins = 200
                    XRange = (config.VarParams[var]['Range'][1]-config.VarParams[var]['Range'][0])
                    NewNbinsX = 100/(BinMaxX-BinMinX) * XRange
                    NGroupX = hist.GetNbinsX()/NewNbinsX
                    NbinsDivisors = GetDivisors(hist.GetNbinsX())
                    # Finds divisor closest to NGroup
                    NGroupDivisorX = min(NbinsDivisors, key=lambda x:abs(x-NGroupX))
                    hist.RebinX(int(NGroupDivisorX))

                    # Recalculating Max Min with higher threshold - this is possible as 
                    # the hists have been rebinned to a large width
                    # Get the index of the min/max bin and the read off the value of the 
                    # low edge
                    # Set FindLastBinAbove threshold to 5 since otherwise the 
                    # hist goes on for way too long
                    BinMaxX = hist.GetBinLowEdge(hist.FindLastBinAbove(5, 1))
                    BinMinX = hist.GetBinLowEdge(hist.FindFirstBinAbove(0, 1))
                    # Max/min = BinMax/min +- 5% +- 5 (prevents max=min for BinMax/Min=0)
                    XMax = BinMaxX + abs(BinMaxX/10) + 5
                    XMin = BinMinX - abs(BinMinX/10) - 5


                    hist.SetAxisRange(XMin, XMax, 'X')
                
                elif hist.GetDimension() == 2:

                    xVar  = var.split('_')[-2]
                    yVar  = var.split('_')[-1]

                    # First version of Max Min using a threshold of 0 since the 
                    # bin width is very small
                    BinMaxX = hist.GetXaxis().GetBinLowEdge(hist.FindLastBinAbove(0, 1)) + 1
                    BinMinX = hist.GetXaxis().GetBinLowEdge(hist.FindFirstBinAbove(0, 1))
                    BinMaxY = hist.GetYaxis().GetBinLowEdge(hist.FindLastBinAbove(0, 2)) + 1
                    BinMinY = hist.GetYaxis().GetBinLowEdge(hist.FindFirstBinAbove(0, 2))     

                    # Rescales bin number so the plotted range has Nbins = 200
                    XRange = (config.VarParams[xVar]['Range'][1]-config.VarParams[xVar]['Range'][0])
                    NewNbinsX = 100/(BinMaxX-BinMinX) * XRange
                    NGroupX = hist.GetNbinsX()/NewNbinsX
                    NbinsDivisors = GetDivisors(hist.GetNbinsX())
                    # Finds divisor closest to NGroup
                    NGroupDivisorX = min(NbinsDivisors, key=lambda x:abs(x-NGroupX))
                    hist.RebinX(int(NGroupDivisorX))

                    # Rescales bin number so the range has Nbins 200
                    YRange = (config.VarParams[yVar]['Range'][1]-config.VarParams[yVar]['Range'][0])
                    NewNbinsY = 200/(BinMaxY-BinMinY) * YRange
                    NGroupY = hist.GetNbinsY()/NewNbinsY
                    NbinsDivisors = GetDivisors(hist.GetNbinsY())
                    # Finds divisor closest to NGroup
                    NGroupDivisorY = min(NbinsDivisors, key=lambda x:abs(x-NGroupY))
                    hist.RebinY(int(NGroupDivisorY))

                    # Recalculating Max Min with higher threshold - this is possible as 
                    # the hists have been rebinned to a large width
                    # Get the index of the min/max bin and the read off the value of the 
                    # low edge
                    # Set FindLastBinAbove threshold to 2 since the particles are now spread
                    # between two vars so the bins will be less filled 
                    # hist goes on for way too long
                    # For 2D hist must first get axis before using TH1 methods
                    BinMaxX = hist.GetXaxis().GetBinLowEdge(hist.FindLastBinAbove(2, 1))
                    BinMinX = hist.GetXaxis().GetBinLowEdge(hist.FindFirstBinAbove(0, 1))
                    BinMaxY = hist.GetYaxis().GetBinLowEdge(hist.FindLastBinAbove(2, 2))
                    BinMinY = hist.GetYaxis().GetBinLowEdge(hist.FindFirstBinAbove(0, 2))                
                    # Max/min = BinMax/min +- 5% +- 5 (prevents max=min for BinMax/Min=0)
                    XMax = BinMaxX + abs(BinMaxX/10) + 5
                    XMin = BinMinX - abs(BinMinX/10) - 5
                    YMax = BinMaxY + abs(BinMaxY/10) + 5
                    YMin = BinMinY - abs(BinMinY/10) - 5        

                    hist.SetAxisRange(XMin, XMax, 'X')
                    hist.SetAxisRange(YMin, YMax, 'Y')

def CompareHist(Hist1, Hist2, HistDict, hist1name, hist2name, MediaDir_name):
    '''
    '''
    
    HistDict1 = config.HistDict.copy()
    HistDict2 = config.HistDict.copy()

    for key, properties in HistDict2.items():
        properties['Hists'] = {}
    for key, properties in HistDict1.items():
        properties['Hists'] = {}

    # If hist 1D
    if len(hist1name.split('_')) == 2:
        name = '_'.join(hist1name.split('_')[0:-1])
        hist1var = hist1name.split('_')[-1]
        hist2var = hist1name.split('_')[-1]

    # If hist is 2D
    elif len(hist1name.split('_')) == 3:
        name = '_'.join(hist1name.split('_')[0:-2])
        hist1var = '_'.join(hist1name.split('_')[-2:])
        hist2var = '_'.join(hist1name.split('_')[-2:])

    HistDict1[name]['Hists'][hist1var] = Hist1
    HistDict2[name]['Hists'][hist2var] = Hist2

    HistLims(HistDict1)
    HistLims(HistDict2)

    # Clear canvas
    HistCan = TCanvas()
    HistCan.cd()

    # max frequency
    Max1 = Hist1.GetMaximum() + Hist1.GetMaximum()/10
    Max2 = Hist2.GetMaximum() + Hist2.GetMaximum()/10
    # Take the larger value from the two hists
    Max = max(Max1, Max2)

    # Setting universal hist options
    for hist in (Hist1, Hist2):
        # SetBins actually introduces an offset into the graph
        hist.SetStats(False)
        hist.SetMaximum(Max)

    if Hist1.GetDimension() == 1:
        # Force both to be drawn as hist and on the same canvas
        Hist1.SetLineColor(4)        
        Hist1.Draw("HIST same")
        Hist2.SetLineColor(2)
        Hist2.Draw("HIST same")
    elif Hist1.GetDimension() == 2:
        TColor.SetPalette(59, 0)
        Hist1.Draw("COLZ same")
        
        TColor.SetPalette(60, 0)
        Hist2.Draw("COLZ same")

    # Legend properties
    LegendX1 = .8
    LegendX_interval = 0.15
    LegendY1 = .95
    LegendY_interval = 0.1

    Legend1 = TLegend(LegendX1, LegendY1 , LegendX1+LegendX_interval, LegendY1-LegendY_interval)
    # Stops legend overwriting canvas
    SetOwnership(Legend1,False)
    Legend1.SetBorderSize(1)
    Legend1.SetShadowColor(2)
    Legend1.SetHeader("Cuts")
    # Entries
    Legend1.AddEntry("entries","Entries: "+str(int(Hist1.GetEntries())))
    Legend1.AddEntry(Hist1, "Line Color", "l")
    Legend1.SetTextSize(0.025)
    Legend1.SetTextColor(1)
    # Seperation is small, but will be maximised to the bounds of the TLegend
    # box
    Legend1.SetEntrySeparation(.1)
    Legend1.Draw("same")

    Legend2 = TLegend(LegendX1, LegendY1-LegendY_interval , LegendX1+LegendX_interval, LegendY1-2*LegendY_interval)
    # Stops legend overwriting canvas    
    SetOwnership(Legend2,False)
    Legend2.SetBorderSize(1)
    Legend2.SetShadowColor(2)
    Legend2.SetHeader("No Cuts")
    # Entries
    Legend2.AddEntry("entries","Entries: "+str(int(Hist2.GetEntries())))
    Legend2.AddEntry(Hist2, "Line Color", "l")
    Legend2.SetTextSize(0.025)       

    # Write canvas to outfile, needs the name for some reason.
    HistCan.SaveAs(MediaDir_name+hist1name+'_'+hist2name+'.png')
  



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