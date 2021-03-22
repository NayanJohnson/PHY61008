
from ROOT import gSystem, gInterpreter, TChain, TH1F, TH2F, TMath, TLorentzVector, TCanvas, TLegend, SetOwnership, TColor

# Path of Delphes directory 
gSystem.AddDynamicPath("/home/nayan/MG5_aMC_v2_8_2/Delphes/")
gSystem.Load("libDelphes")

gInterpreter.Declare('#include "classes/DelphesClasses.h"')
gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')

from ROOT import ExRootTreeReader
import config, itertools


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



def MakeHists(HistDict):
    '''
        Will initialise histograms using HistDict[Category][Requests][Vars] list
        and add them to HistDict[Category][Hists].
        Will also scale the hist using the GetScale() function.

        Histogram dictionary should be in the following format:
        HistDict =        {
            category        :   {
                Requests        :   {
                    Vars            :   [],
                    Particles       :   []
                },

                Vars        :   [],
                Particles   :   [],
                Hists       :   {
                    Var1        :   Hist1,
                    Var2        :   Hist2
                }
            }
        }
    '''

    VarParams = config.VarParams
    NbinsDefault = VarParams['Nbins']
    BinScale = VarParams['NbinsScale']

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
                    histXrange = histXup-histXlow

                    if histXrange <= 10:
                        histXNbins = int(NbinsDefault * histXrange*2/BinScale)
                    elif histXrange <= 100:
                        # Scales number of bins dependng on var range
                        histXNbins = int(NbinsDefault * histXrange/BinScale)
                    else:
                        histXNbins = 300

                    histYlow = VarParams[var[1]]['Range'][0]
                    histYup = VarParams[var[1]]['Range'][1]        
                    histYrange = histYup-histYlow

                    if histYrange <= 10:
                        histYNbins = int(NbinsDefault * histYrange*2/BinScale)
                    elif histYrange <= 100:
                        # Scales number of bins dependng on var range
                        histYNbins = int(NbinsDefault * histYrange/BinScale)
                    else:
                        histYNbins = 300                    

                    hist = TH2F(histName, histTitle, histXNbins, histXlow, histXup, histYNbins, histYlow, histYup)
                    
                    hist.SetOption('HIST COLZ')
                    # Adds the hist to the dict
                    HistDict[name]['Hists'][var[0]+'_'+var[1]] = hist

            elif type(var) == str:
                histName = name+'_'+var
                histTitle = histName+';'+var+';Frequency'

                histXlow = VarParams[var]['Range'][0]
                histXup = VarParams[var]['Range'][1]
                histXrange = histXup-histXlow

                if histXrange <= 10:
                    histXNbins = int(NbinsDefault * histXrange*2/BinScale)
                elif histXrange <= 100:
                    # Scales number of bins dependng on var range
                    histXNbins = int(NbinsDefault * histXrange/BinScale)
                else:
                    histXNbins = 300

                hist = TH1F(histName, histTitle, histXNbins, histXlow, histXup)


                hist.SetOption('HIST')
                # Adds the hist to the dict
                HistDict[name]['Hists'][var] = hist

    return HistDict

def RequestParticles(HistDict, ParticleDict):
    '''
        Adds requested particles to the HistDict.
        Histogram dictionary should be in the following format:
        HistDict =        {
            category        :   {
                Requests        :   {
                    Vars            :   [],
                    Particles       :   []
                },

                Vars        :   [],
                Particles   :   [],
                Hists       :   {
                    Var1        :   Hist1,
                    Var2        :   Hist2
                }
            }
        }
        
        Particle dictionary should be in the following format:
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

    # Itterating through histogram categories
    for category, properties in HistDict.items():
        
        # Itterating through particle requests
        for particle in properties['Requests']['Particles']:

            # Particle check
            if ParticleDict[particle]['Check']:
                properties['Particles'].append(ParticleDict[particle])               

    return HistDict

def FillHists(HistDict):
    '''
        Given a dictionary of histograms, will fill them.
        Histogram dictionary should be in the following format:
        HistDict =        {
            category        :   {
                Requests        :   {
                    Vars            :   [],
                    Particles       :   []
                },

                Vars        :   [],
                Particles   :   [],
                Hists       :   {
                    Var1        :   Hist1,
                    Var2        :   Hist2
                }
            }
        }
    '''
    
    # List of variables that are stored in all particles.
    ParticleProperties = ['PID', 'E', 'Eta', 'Phi', 'Rapidity', 'Theta', 'Pt', 'Et']

    for category, properties in HistDict.items():
        for var, hist in properties['Hists'].items():

            # Count var can be read straight from properties
            if var == 'Count': 
                hist.Fill(properties['Count'])

            # If var contains 2 variables
            elif len(var.split('_')) == 2:
                xVar = GetParticleVariable(var.split('_')[0], properties['Particles'], category, 2)
                yVar = GetParticleVariable(var.split('_')[1], properties['Particles'], category, 2)
                if xVar and yVar:
                    hist.Fill(xVar, yVar)

            else:
                xVar = GetParticleVariable(var, properties['Particles'], category)
                if xVar != False:
                    # If the function returns a list fill the hist for each
                    # element in list
                    if type(xVar) == list:
                        for V in xVar:
                            hist.Fill(V)
                    else:
                        hist.Fill(xVar)


def GetParticleVariable(var, ParticleList, category=None, dims=1):
    '''
        Returns the value or list of variables for the given category : var
        Category is only used for q calcs.
        var is a string.
        properties is in the format:
        properties = {
            Requests        :   {
                Vars            :   [],
                Particles       :   []
            },

            Vars        :   [],
            Particles   :   [],
            Hists       :   {
                Var1        :   Hist1,
                Var2        :   Hist2
            }
        }
    '''

    # List of variables that are stored in all particles.
    ParticleProperties = ['PID', 'E', 'Eta', 'Phi', 'Rapidity', 'Theta', 'Pt', 'Et']

    # Variables that can be calculated from one or multiple
    # particles.
    if len(ParticleList) != 0:

        # Variables in ParticleProperties only require one particle so
        # the hist can be filled by all particles in the list.
        if var in ParticleProperties:
            # Only alow 1D hists to return a list
            if dims ==1:
                ParticleVars = []
                for i in range(0, len(ParticleList)):
                    ParticleVars.append(ParticleList[i][var])
                return ParticleVars
            else:
                return ParticleList[0][var]

        elif var == 'InvMass':
            ParticleSum = TLorentzVector()
            for particle in ParticleList:
                ParticleSum = particle['P4'] + ParticleSum
            return ParticleSum.M()

    # Seperates hists into the number of required particles
    if len(ParticleList) == 2:

        if var == 'q':
            if category == 'qLepton' or category == 'qQuark':
                q = (ParticleList[0]['P4'] - ParticleList[1]['P4']).Mag()
            elif category == 'qeMethod':
                q = TMath.Sqrt(2*ParticleList[0]['E']*ParticleList[1]['E']*(1 - TMath.Cos(ParticleList[0]['Theta'])))
            return abs(q)

        elif var == 'dEta':
            dEta = ParticleList[0]['Eta'] - ParticleList[1]['Eta']
            return dEta
        
        elif var == 'dPhi':
            dPhi = ParticleList[0]['P4'].DeltaPhi(ParticleList[1]['P4'])
            return dPhi

        elif var == 'dRapidity':
            dRap = ParticleList[0]['Rapidity'] - ParticleList[1]['Rapidity']
            return dRap

        elif var == 'dR_Eta':
            dR_Eta = ParticleList[0]['P4'].DrEtaPhi(ParticleList[1]['P4'])
            return dR_Eta

        elif var == 'dR_Rap':
            dPhi = ParticleList[0]['P4'].DeltaPhi(ParticleList[1]['P4'])
            dRap = ParticleList[0]['Rapidity'] - ParticleList[1]['Rapidity']
            # DrRapidityPhi function doesnt seem to work
            dR_Rap = TMath.Sqrt( dPhi**2 + dRap**2 )
            return dR_Rap    
    return False

def GetDivisors(n):
    '''
        Given an int, will return a list of perfect divisors.
    '''
    Divisors = []
    i = 1
    while i <= n : 
        if (n % i==0) : 
            Divisors.append(i), 
        i += 1
    return Divisors

def GetScale(PythiaLogPath, NEvents):
    '''
        Given the path to the pythia log file and the number of events,
        will return the scaling factor calculated from the process 
        cross section. 
    '''

    with open(PythiaLogPath, "r") as file:
        lines = file.read().splitlines()
        # Xsec is the last element of the last line
        Xsec = float(lines[-1].split()[-1])
    
    # L_int(Data) = 1 [ab-1] = 1000000 [pb-1]
    # L_int(MC) = N/Xsec [pb-1]
    # Scale = L_int(Data) / L_int(MC)
    Scale = 1000000 / (NEvents/Xsec)

    return Scale

def HistLims(hist, var, Scale=1, RelativeScale='Rel' ):

    '''
        Rescales hist lims depending on the data in the hists.
        Histogram dictionary should be in the following format:
        HistDict =        {
            category        :   {
                Requests        :   {
                    Vars            :   [],
                    Particles       :   []
                },

                Vars        :   [],
                Particles   :   [],
                Hists       :   {
                    Var1        :   Hist1,
                    Var2        :   Hist2
                }
            }
        }
    '''    
    XMin, XMax, YMin, YMax = None, None, None, None

    if RelativeScale == 'Rel':
        hist.Scale(Scale)
    elif RelativeScale == 'Norm' and hist.Integral() != 0:
        hist.Scale(1./hist.Integral())

    ThresholdMin = (hist.Integral()/200) * 1/100                # Skip if hist = False

    if hist:
        if hist.GetDimension() == 1:
                        # Recalculating Max Min with higher threshold - this is possible as 
            # the hists have been rebinned to a large width
            # Get the index of the min/max bin and the read off the value of the 
            # low edge
            # Set FindLastBinAbove threshold to 5 since otherwise the 
            # hist goes on for way too long
            BinMaxX = hist.GetBinLowEdge(hist.FindLastBinAbove(ThresholdMin, 1))
            BinMinX = hist.GetBinLowEdge(hist.FindFirstBinAbove(0, 1))
            # Max/min = BinMax/min +- 5% +- 5 (prevents max=min for BinMax/Min=0)
            XMax = BinMaxX + 5
            XMin = BinMinX - 5


            hist.SetAxisRange(XMin, XMax, 'X')
        
        elif hist.GetDimension() == 2:

            xVar  = var.split('_')[-2]
            yVar  = var.split('_')[-1]

            # Recalculating Max Min with higher threshold - this is possible as 
            # the hists have been rebinned to a large width
            # Get the index of the min/max bin and the read off the value of the 
            # low edge
            # Set FindLastBinAbove threshold to 2 since the particles are now spread
            # between two vars so the bins will be less filled 
            # hist goes on for way too long
            # For 2D hist must first get axis before using TH1 methods
            BinMaxX = hist.GetXaxis().GetBinLowEdge(hist.FindLastBinAbove(ThresholdMin, 1))
            BinMinX = hist.GetXaxis().GetBinLowEdge(hist.FindFirstBinAbove(0, 1))
            BinMaxY = hist.GetYaxis().GetBinLowEdge(hist.FindLastBinAbove(ThresholdMin, 2))
            BinMinY = hist.GetYaxis().GetBinLowEdge(hist.FindFirstBinAbove(0, 2))                
            # Max/min = BinMax/min +- 5 (prevents max=min for BinMax/Min=0)
            XMax = BinMaxX + 5
            XMin = BinMinX - 5
            YMax = BinMaxY + 5
            YMin = BinMinY - 5        

            hist.SetAxisRange(XMin, XMax, 'X')
            hist.SetAxisRange(YMin, YMax, 'Y')
    return hist, [(XMin, XMax), (YMin, YMax)]


def CompareHist(HistProps):
    '''
        Given a histogram dictionary and 
     
        Histogram dictionary should be in the following format:
        HistDict =        {
            category        :   {
                Requests        :   {
                    Vars            :   [],
                    Particles       :   []
                },

                Vars        :   [],
                Particles   :   [],
                Hists       :   {
                    Var1        :   Hist1,
                    Var2        :   Hist2
                }
            }
        }
         
        Histogram properties dictionary should be in the following format:
        HistProps =     {
            'Hist1'     :       {
                'Hist'          :   Hist1,
                'HistName'      :   Hist1Name,
                'HistVar'       :   HistVar,
                'HistFileName'  :   Hist1FileName    
            },

            'Hist2'     :       {
                'Hist'          :   Hist2,
                'HistName'      :   Hist2Name,
                'HistVar'       :   HistVar,
                'HistFileName'  :   Hist2FileName    
            }
        }
    '''
    
    RelativeScale = HistProps['RelScale']

    Hist1Name = HistProps['Hist1']['HistName']
    Hist1Var = HistProps['Hist1']['HistVar']
    Hist1 = HistProps['Hist1']['FileDict']['File'].Get(Hist1Name+'_'+Hist1Var+';1')

    Hist1File_Prefix = HistProps['Hist1']['FileDict']['Prefix']
    Hist1File_EventRun = HistProps['Hist1']['FileDict']['EventRun']
    Hist1File_ParticleRun = HistProps['Hist1']['FileDict']['ParticleRun']

    Hist2Name = HistProps['Hist2']['HistName']
    Hist2Var = HistProps['Hist2']['HistVar']
    Hist2 = HistProps['Hist2']['FileDict']['File'].Get(Hist2Name+'_'+Hist2Var+';1')
    
    Hist2File_Prefix = HistProps['Hist2']['FileDict']['Prefix']
    Hist2File_EventRun = HistProps['Hist2']['FileDict']['EventRun']
    Hist2File_ParticleRun = HistProps['Hist2']['FileDict']['ParticleRun']


    Hist1, Lims1 = HistLims(Hist1, Hist1Var, RelativeScale=RelativeScale)
    Hist2, Lims2 = HistLims(Hist2, Hist2Var, RelativeScale=RelativeScale)

    # Clear canvas
    HistCan = TCanvas()
    HistCan.cd()

    XMin = min(Lims1[0][0], Lims2[0][0])
    XMax = max(Lims1[0][1], Lims2[0][1])

    Hist1.SetAxisRange(XMin, XMax, 'X')
    Hist2.SetAxisRange(XMin, XMax, 'X')

    #2D hists
    if Hist1.GetDimension() == 2:
        YMin = min(Lims1[1][0], Lims2[1][0])
        YMax = max(Lims1[1][1], Lims2[1][1])
        Hist1.SetAxisRange(YMin, YMax, 'Y')
        Hist2.SetAxisRange(YMin, YMax, 'Y')



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


    # Legend properties
    LegendX1 = .8
    LegendX_interval = 0.2
    LegendY1 = .95
    LegendY_interval = 0.1

    Legend1 = TLegend(LegendX1, LegendY1 , LegendX1+LegendX_interval, LegendY1-LegendY_interval)
    # Stops legend overwriting canvas
    SetOwnership(Legend1,False)
    Legend1.SetBorderSize(1)
    Legend1.SetShadowColor(2)
    Legend1.SetHeader(Hist1Name)
    # Entries
    Legend1.AddEntry("entries","Entries: "+str(int(Hist1.GetEntries())))
    Legend1.AddEntry(Hist1, "Line Color", "l")
    Legend1.SetTextSize(0.025)
    Legend1.SetTextColor(1)
    # Seperation is small, but will be maximised to the bounds of the TLegend
    # box
    Legend1.SetEntrySeparation(.1)

    Legend2 = TLegend(LegendX1, LegendY1-LegendY_interval , LegendX1+LegendX_interval, LegendY1-2*LegendY_interval)
    # Stops legend overwriting canvas    
    SetOwnership(Legend2,False)
    Legend2.SetBorderSize(1)
    Legend2.SetShadowColor(2)
    # Entries
    Legend2.AddEntry("entries","Entries: "+str(int(Hist2.GetEntries())))
    Legend2.AddEntry(Hist2, "Line Color", "l")
    Legend2.SetTextSize(0.025)       
    # Seperation is small, but will be maximised to the bounds of the TLegend
    # box
    Legend2.SetEntrySeparation(.1)

    if Hist1File_Prefix == Hist2File_Prefix:
        Hist1.SetTitle(Hist1Name+'_'+Hist1Var)
        if Hist1Name == Hist2Name:
            Legend1.SetHeader('Event'+Hist1File_EventRun+'Particle'+Hist1File_ParticleRun)
            Legend2.SetHeader('Event'+Hist2File_EventRun+'Particle'+Hist2File_ParticleRun)
        
        else:
            Legend1.SetHeader(Hist1Name)
            Legend2.SetHeader(Hist2Name)

    else:
        Hist1.SetTitle(Hist1Name+'_'+Hist2Name)
        if Hist1Name == Hist2Name:
            Legend1.SetHeader(Hist1File_Prefix)
            Legend2.SetHeader(Hist2File_Prefix)
        else:
            Legend1.SetHeader(Hist1File_Prefix+'_'+Hist1Name)
            Legend1.SetHeader(Hist2File_Prefix+'_'+Hist2Name)


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

    Legend1.Draw("same")
    Legend2.Draw("same")

    HistCan.Update()
    
    if Hist1Name == Hist2Name:
        HistCan.SaveAs(RelativeScale+'_'+Hist1File_Prefix+'-'+Hist2File_Prefix+'/Event'+Hist1File_EventRun+'-'+Hist2File_EventRun+'/Particle'+Hist1File_ParticleRun+'-'+Hist2File_ParticleRun+'/'+Hist1Name+Hist1Var+'.png')
    else:
        HistCan.SaveAs(RelativeScale+'_'+Hist1File_Prefix+'-'+Hist2File_Prefix+'/Event'+Hist1File_EventRun+'-'+Hist2File_EventRun+'/Particle'+Hist1File_ParticleRun+'-'+Hist2File_ParticleRun+'/'+Hist1Name+Hist2Name+Hist1Var+'.png')

  



def AddParticle(name, ParticleDict, P4=None, PID=None):
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
            }
        
        return ParticleDict


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
    Cuts = config.EventLoopParams['Runs']['ParticleLevel'][Run]

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
                        ElectronPT.append( (particle.PT, particle) )


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
            # Jet cuts
            if Cuts['jet_Eta'][0] <= jet.P4().Eta() <= Cuts['e_Eta'][1]:
                if jet.P4().Pt() >= Cuts['jet_Pt']:
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

def InvMassCheck(particles, Boson, ParticleDict, EventDict):
    '''
    '''

    if particles == 'Electrons' and EventDict['Count']['Electrons'] <= 2:
        return ParticleDict, EventDict

    elif particles == 'Muons' and EventDict['Count']['Muons'] <= 1:
        return ParticleDict, EventDict

    elif particles == 'Jets' and EventDict['Count']['Jets'] <= 2:
        return ParticleDict, EventDict

    BosonMass = config.EventLoopParams[Boson]['Mass']

    # Setting up list of possible Boson decay products
    # When indexing ParticleDict remove the 's' from particle
    # Size of particlesList depends of number of expected particles
    # of that type

    # Getting the sorted particles from list
    # List will be a list of tuples (Pt, particle)
    particlesList = EventDict['PTSorted'][particles[0:-1]]
    # Possible pairs of Z decay products
    Permutations = list( itertools.combinations(particlesList, 2))

    InvMassList = []
    # Calculating InvMass of different possible pairs
    for ParticlePair in Permutations:
        InvMassList.append( (ParticlePair[0][1].P4()+ParticlePair[1][1].P4()).Mag() )

    # Find the closest InvMass to the BosonMass
    PairInvMass = min(InvMassList, key=lambda x:abs(x-BosonMass))
    PairIndex = InvMassList.index(PairInvMass)
    if Permutations[PairIndex][0][0] < Permutations[PairIndex][1][0]:
        ParticleDict = AddParticle(Boson+'Leading'+particles[0:-1], ParticleDict, Permutations[PairIndex][1][1].P4())
        ParticleDict = AddParticle(Boson+'SubLeading'+particles[0:-1], ParticleDict, Permutations[PairIndex][0][1].P4())

    else:        
        ParticleDict = AddParticle(Boson+'Leading'+particles[0:-1], ParticleDict, Permutations[PairIndex][0][1].P4())
        ParticleDict = AddParticle(Boson+'SubLeading'+particles[0:-1], ParticleDict, Permutations[PairIndex][1][1].P4())

    # Removing boson particles from list of particle
    particlesList.remove(Permutations[PairIndex][0])
    particlesList.remove(Permutations[PairIndex][1])
    EventDict['PTSorted'][particles[0:-1]] = particlesList

    return ParticleDict, EventDict

