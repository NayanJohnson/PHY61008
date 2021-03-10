
from ROOT import gSystem, gInterpreter, TChain, TH1F, TLorentzVector

# Path of Delphes directory 
gSystem.AddDynamicPath("/home/nayan/MG5_aMC_v2_8_2/Delphes/")
gSystem.Load("libDelphes")

gInterpreter.Declare('#include "classes/DelphesClasses.h"')
gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')

class Histogram:
    '''
    '''

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __init__(self, name, bins, var, xmin, xmax):
        '''
        '''

        self.name = name
        self.hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', bins, xmin, xmax)

    return self

    def MakeHists(Dict):
        '''
            Given a dictionary with names being keys for a list of variables.
        '''

        HistDict = {}

        for name, vars in Dict:
            HistDict[name] = {}

            for var in vars:
                hist = False

                if var == 'Count': 
                    hist = Histogram(name, 200, var, 0, 10)

                elif var == 'Eta' or 'dEta':
                    hist = Histogram(name, 200, var, -8, 8)

                elif var == 'Phi' or 'dPhi':
                    hist = Histogram(name, 200, var, -3.5, 3.5)
                
                elif var == 'Rapidity' or 'dRapidity':
                    hist = Histogram(name, 200, var, -10, 10)
                
                elif var == 'PT':
                    hist = Histogram(name, 200, var, 0, 200)
                
                elif var == 'q':
                    hist = Histogram(name, 200, var, 0, 1200)

                elif var == 'dR_Eta' or 'dR_Rap':
                    hist = Histogram(name, 200, var, 0, 10)                
                
                elif var == 'InvMass':
                    hist = Histogram(name, 200, var, 0, 10)   
                
                HistDict[name][var] = hist
        
        return HistDict

  
