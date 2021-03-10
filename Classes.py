
from ROOT import TMath, TH1F, TLorentzVector

class Histogram:
    '''
    '''

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def InitHist(self, name, bins, var, xmin, xmax):
        '''
        '''

        self.hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', bins, xmin, xmax)

        return self

    @staticmethod
    def MakeHists(HistDict):
        '''
            Given a dictionary with names being keys for a list of variables.
        '''


        for name, properties in HistDict.items():
            for var in properties['Vars']:
                hist = False

                if var == 'Count': 
                    hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 200, 0, 10)

                elif var == 'Eta' or 'dEta':
                    hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 200, -8, 8)

                elif var == 'Phi' or 'dPhi':
                    hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 200, -3.5, 3.5)
                
                elif var == 'Rapidity' or 'dRapidity':
                    hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 200, -10, 10)
                
                elif var == 'PT':
                    hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 200, 0, 200)
                
                elif var == 'q':
                    hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 200, 0, 1200)

                elif var == 'dR_Eta' or 'dR_Rap':
                    hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 200, 0, 10)
                
                elif var == 'InvMass':
                    hist = TH1F(name+'_'+var, name+'_'+var+';'+var+';Frequency', 200, 0, 10)
                
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

        for Catagory, HistSubDict in HistDict:
            for var, hist in HistSubDict['hists']:
                if var == 'Count': 
                    hist.Fill(HistSubDict['Count'])

                elif var in ParticleProperties:
                    hist.Fill(HistSubDict[var])

                elif var == 'q':
                    if Catagory == 'q_Electron' or 'q_Quark':
                        q = (HistSubDict['Particles'][0]['P4'] - HistSubDict['Particles'][1]['P4']).Mag()
                    elif Catagory == 'q_eMethod':
                        q = TMath.Sqrt(2*HistSubDict['Particles'][0]['E']*HistSubDict['Particles'][1]['E']*(1 - TMath.Cos(HistSubDict['Particles'][0]['Theta'])))
                    hist.Fill(q)

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
                    dR_Rap = HistSubDict['Particles'][0]['P4'].DrRapidityPhi(HistSubDict['Particles'][1]['P4'])
                    hist.Fill(dR_Rap)                          
                
                elif var == 'InvMass':
                    ParticleSum = TLorentzVector()
                    for paritcle in HistSubDict['Particles']:
                        ParticleSum = paritcle['P4'] + ParticleSum
                    hist.Fill(ParticleSum.M())
        