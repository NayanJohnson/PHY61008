# This file contains data structures used by functions that are not dependant on the process

# Variable strings recognised
VarKeywords = [
    'Count', 'Eta', 'Phi', 'Rapidity', 'Pt', 'Et', 'E', 'M', 'Mt', 'qeMethod', 'qLepton', 
    'dEta', 'dPhi', 'dRapidity', 'dR_Eta', 'dR_Rap',
    'Eta_Sum', 'Phi_Sum', 'Rapidity_Sum', 'Pt_Sum', 'Et_Sum', 'E_Sum'
]

# Particle strings recognised
ParticleKeywords = [
    'BeamQuark', 'FinalBeamJet', 
    'LeadingJet', 'SubLeadingJet', 'ThirdJet',
    'BeamElectron', 'FinalBeamElectron', 
    'LeadingElectron', 'SubLeadingElectron', 'ThirdElectron', 'FourthElectron', 'FifthElectron',
    'MuonSum', 'AllMuons', 'DiMuon',
    'LeadingMuon', 'SubLeadingMuon', 'ThirdMuon', 'FourthMuon',
    'LeadingJet', 'SubLeadingJet', 'ThirdJet', 'FourthJet',
    'MissingET', 
    'WPlusElectron', 'WPlusMuon', 'WMinusElectron', 'WMinusMuon', 'WMuonSum', 'WPlusMuonFinalBeamElectron',
    'WLeadingJet', 'WSubLeadingJet', 
    'ZLeadingElectron', 'ZSubLeadingElectron', 'ZThirdElectron', 'ZFourthElectron',
    'ZLeadingMuon', 'ZSubLeadingMuon', 'ZThirdMuon', 'ZFourthMuon',
    'ZLeadingJet', 'ZSubLeadingJet', 
]

# Variable dependant histogram parameters 
VarParams = {
    'Nbins'     :   150,
    'LowRangeNbinsScale'    
                :   1,
    'HighRangeNbinsScale'   
                :   1,
    'Count'     :   {
        'Range'     :   [0, 10]
    },

    'Eta'       :   {
        'Range'     :   [-10, 10]
    },

    'Phi'       :   {
        'Range'     :   [-3.5, 3.5]
    },

    'Rapidity'  :   {
        'Range'     :   [-10, 10]
    },

    'E'        :   {
        'Range'     :   [0, 1000]
    },

    'Pt'        :   {
        'Range'     :   [0, 500]
    },
    
    'Et'        :   {
        'Range'     :   [0, 500]
    },

    'Mt'   :   {
        'Range'     :   [0, 500]
    },

    'qLepton'         :   {
        'Range'     :   [0, 1000]
    },

    'qQuark'         :   {
        'Range'     :   [0, 1000]
    },

    'qeMethod'         :   {
        'Range'     :   [0, 1000]
    },

    'dEta'      :   {
        'Range'     :   [-20, 20]
    },
    
    'dPhi'      :   {
        'Range'     :   [-3.5, 3.5]
    },
    
    'dRapidity' :   {
        'Range'     :   [-20, 20]
    },
    
    'dR_Eta'    :   {
        'Range'     :   [0, 20]
    },
    
    'dR_Rap'    :   {
        'Range'     :   [0, 20]
    },
    
    'M'   :   {
        'Range'     :   [0, 500]
    },

    'Eta_Sum'       :   {
        'Range'     :   [-10, 10]
    },

    'Phi_Sum'       :   {
        'Range'     :   [-3.5, 3.5]
    },

    'Rapidity_Sum'  :   {
        'Range'     :   [-10, 10]
    },

    'E_Sum'        :   {
        'Range'     :   [0, 1000]
    },

    'Pt_Sum'        :   {
        'Range'     :   [0, 500]
    },
    
    'Et_Sum'        :   {
        'Range'     :   [0, 500]
    },
}


# Dictionary of all histograms to be filled
# Entries are used to request histograms to be constructed and filled 

'''
HistDict =        {
    category        :   {
        Requests        :   {
            Vars            :   [],
            Particles       :   []
        },
        
        Dimensions  :   int(),
        Particles   :   [],
        Hists       :   {
            name        :   hist, ...
        },
    }
}

for 1D:

    Requests        :   {
        Vars        :   [var1, var2, ...],
    },

    Dimensions  :   1,
    Particles   :   [particle1, particle2, ...],
    Hists       :   {name1 : hist1, ... },

for 2D:

    Requests        :   {
        Vars        :   [(xvar1, yvar1), (xvar2, yvar2) ...],
    },

    Dimensions  :   2,
    Particles   :   [(xParticles1), (yParticles1), (xParticles2), (yParticles2)],
    Hists       :   {name1 : hist1, ... },
'''

HistDict =  {
    'Electrons'     :   {
        'Requests'      :   {
            'Vars'      :   ['Count'],
            'Particles' :   [[]],
        },
        'Dimensions':   1,
    },
    
    'Muons'         :   {
        'Requests'      :   {
            'Vars'      :   ['Count'],
            'Particles' :   [[]],
        },
        'Dimensions':   1,
    },
    
    'Jets'          :   {
        'Requests'      :   {
            'Vars'      :   ['Count'],
            'Particles' :   [[]],
        },
        'Dimensions':   1,
    },
    
    'FinalBeamElectron' 
                    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', 'qLepton', 'qeMethod'],
            'Particles' :   [['FinalBeamElectron']],
        },
        'Dimensions':   1,
    },
    
    'LeadingMuon'   :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   [['LeadingMuon']],
        },
        'Dimensions':   1,
    },
    
    'SubLeadingMuon':   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   [['SubLeadingMuon']],
        },
        'Dimensions':   1,
    },
    
    'ThirdMuon'     :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   [['ThirdMuon']],
        },
        'Dimensions':   1,
    },    
    
    'FourthMuon'    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   [['ThirdMuon']],
        },
        'Dimensions':   1,
    },              

    'DiMuon'    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Pt', 'M', 'Mt', 'qLepton'],
            'Particles' :   [['DiMuon']],
        },
        'Dimensions':   1,
    },

    'WPlusMuonFinalBeamElectron'    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Pt', 'M', 'Mt', 'qLepton'],
            'Particles' :   [['WPlusMuonFinalBeamElectron']],
        },
        'Dimensions':   1,
    },

    'AllJets'       :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', 'E'],
            'Particles' :   [['LeadingJet'], ['SubLeadingJet'], ['ThirdJet'], ['FourthJet']],
        },
        'Dimensions':   1,
    },    

    'FinalBeamJet'    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', 'qQuark'],
            'Particles' :   [['FinalBeamJet']],
        },
        'Dimensions':   1,
    },    

    'LeadingJets'    :   {
        'Requests'      :   {
            'Vars'      :   ['M'],
            'Particles' :   [['LeadingJet', 'SubLeadingJet']],
        },
        'Dimensions':   1,
    },    

    'LeadingJet'    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', 'M'],
            'Particles' :   [['LeadingJet']],
        },
        'Dimensions':   1,
    },    

    'SubLeadingJet' :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', 'M'],
            'Particles' :   [['SubLeadingJet']],
        },
        'Dimensions':   1,
    },    

    'ThirdJet'      :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   [['ThirdJet']],
        },
        'Dimensions':   1,
    },    

    'MissingET'     :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', 'Et'],
            'Particles' :   [['MissingET']],          
        },
        'Dimensions':   1,
    },    

    'WLeadingJet'   :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   [['WLeadingJet']],
        },
        'Dimensions':   1,
    },    

    'WSubLeadingJet':   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   [['WSubLeadingJet']],
        },
        'Dimensions':   1,
    },    

    'WJets':   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   [['WLeadingJet'], ['WSubLeadingJet']],
        },
        'Dimensions':   1,
    },    

    'WPlusMuon'     :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   [['WPlusMuon']],
        },
        'Dimensions':   1,
    },    

    'WMinusMuon'     :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', 'qLepton', 'qeMethod'],
            'Particles' :   [['WMinusMuon']],
        },
        'Dimensions':   1,
    },    

    'ZLeadingMuon'  :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   [['ZLeadingMuon']],
        },
        'Dimensions':   1,
    },    

    'ZSubLeadingMuon'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   [['ZSubLeadingMuon']],
        },
        'Dimensions':   1,
    },    

    'ZMuons'        :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', 'M'],
            'Particles' :   [['ZLeadingMuon', 'ZSubLeadingMuon']],
        },
        'Dimensions':   1,
    },    

    'ZLeadingJet'   :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   [['ZLeadingJet']],
        },
        'Dimensions':   1,
    },

    'ZSubLeadingJet'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   [['ZSubLeadingJet']],
        },
        'Dimensions':   1,
    },    

    'ZJets'         :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', 'Pt_Sum', 'M', 'Mt', 'dR_Eta'],
            'Particles' :   [['ZLeadingJet', 'ZSubLeadingJet']],
        },
        'Dimensions':   1,
    },    

    'ZLeadingJetFinalBeamJet'         :   {
        'Requests'      :   {
            'Vars'      :   ['Pt_Sum', 'M', 'Mt', 'dR_Eta'],
            'Particles' :   [['ZLeadingJet', 'FinalBeamJet']],
        },
        'Dimensions':   1,
    },    

    'ZSubLeadingJetFinalBeamJet'         :   {
        'Requests'      :   {
            'Vars'      :   ['Pt_Sum', 'M', 'Mt',  'dR_Eta'],
            'Particles' :   [['ZSubLeadingJet', 'FinalBeamJet']],
        },
        'Dimensions':   1,
    },    

    'FinalBeamElectronLeadingMuon'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   [['FinalBeamElectron', 'LeadingMuon']],
        },
        'Dimensions':   1,
    },    

    'FinalBeamElectronSubLeadingMuon'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   [['FinalBeamElectron', 'SubLeadingMuon']],
        },
        'Dimensions':   1,
    },    

    'FinalBeamElectronFinalBeamJet'   
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi', 'M'],
            'Particles' :   [['FinalBeamElectron', 'FinalBeamJet']],
        },
        'Dimensions':   1,
    },    

    'FinalBeamElectronLeadingJet'   
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi', 'M'],
            'Particles' :   [['FinalBeamElectron', 'LeadingJet']],
        },
        'Dimensions':   1,
    },    


    'MuonMuon'      :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi', 'dRapidity', 'dR_Eta', 'dR_Rap', 'M'],
            'Particles' :   [['LeadingMuon', 'SubLeadingMuon']],
        },
        'Dimensions':   1,
    },    

    'LeadingMuonFinalBeamJet'
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   [['LeadingMuon', 'FinalBeamJet']],
        },
        'Dimensions':   1,
    },    

    'SubLeadingMuonFinalBeamJet'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   [['SubLeadingMuon', 'FinalBeamJet']],
        },
        'Dimensions':   1,
    },    

    'MissingETFinalElectron'    
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   [['MissingET', 'FinalBeamElectron']],
        },
        'Dimensions':   1,
    },    

    'MissingETFinalBeamJet'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   [['MissingET', 'FinalBeamJet']],
        },
        'Dimensions':   1,
    },    

    'MissingETWMuons'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   [['MissingET', 'WMuonSum']],
        },
        'Dimensions':   1,
    },    

    'MissingETLeadingMuon'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   [['MissingET', 'LeadingMuon']],
        },
        'Dimensions':   1,
    },    

    'MissingETSubLeadingMuon'   
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   [['MissingET', 'SubLeadingMuon']],
        },
        'Dimensions':   1,
    },    

    'MissingETThirdMuon'   
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   [['MissingET', 'ThirdMuon']],
        },
        'Dimensions':   1,
    },    

    'MissingETMuonSum'      
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   [['MissingET', 'MuonSum']],
        },
        'Dimensions':   1,
    },    

    'JetAllParticles'
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dR_Eta'],
            'Particles' :   [['LeadingJet', 'FinalBeamElectron'], ['LeadingJet', 'LeadingMuon'], ['LeadingJet', 'SubLeadingMuon'],
                            ['SubLeadingJet', 'FinalBeamElectron'], ['SubLeadingJet', 'LeadingMuon'], ['SubLeadingJet', 'SubLeadingMuon']],
        },
        'Dimensions':   1,
    },    

### 2D Hists ###

    '2DFinalBeamElectron' 
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['FinalBeamElectron'], ['FinalBeamElectron']]],
        },
        'Dimensions':   2,
    },

    '2DLeadingMuon'   
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['LeadingMuon'], ['LeadingMuon']]],
        },
        'Dimensions':   2,
    },

    '2DSubLeadingMuon'   
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['SubLeadingMuon'], ['SubLeadingMuon']]],
        },
        'Dimensions':   2,
    },

    '2DThirdMuon'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['ThirdMuon'], ['ThirdMuon']]],
        },
        'Dimensions':   2,
    },

    '2DFourthMuon'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['FourthMuon'], ['FourthMuon']]],
        },
        'Dimensions':   2,
    },

    '2DAllJets'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['LeadingJet', 'SubLeadingJet', 'ThirdJet', 'FourthJet'], ['LeadingJet', 'SubLeadingJet', 'ThirdJet', 'FourthJet']]],
        },
        'Dimensions':   2,
    },

    '2DFinalBeamJet'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['FinalBeamJet'], ['FinalBeamJet']]],
        },
        'Dimensions':   2,
    },

    '2DLeadingJet'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['LeadingJet'], ['LeadingJet']]],
        },
        'Dimensions':   2,
    },

    '2DSubLeadingJet'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['SubLeadingJet'], ['SubLeadingJet']]],
        },
        'Dimensions':   2,
    },

    '2DThirdJet'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['ThirdJet'], ['ThirdJet']]],
        },
        'Dimensions':   2,
    },

    '2DMissingET'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt'], ['Phi', 'Et']],
            'Particles' :   [[['MissingET'], ['MissingET']]],
        },
        'Dimensions':   2,
    },

    '2DWLeadingJet'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['WLeadingJet'], ['WLeadingJet']]],
        },
        'Dimensions':   2,
    },

    '2DWSubLeadingJet'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['WSubLeadingJet'], ['WSubLeadingJet']]],
        },
        'Dimensions':   2,
    },

    '2DWJets'       :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['WLeadingJet', 'WSubLeadingJet'], ['WLeadingJet', 'WSubLeadingJet']]],
        },
        'Dimensions':   2,
    },

    '2DWPlusMuon'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['WPlusMuon'], ['WPlusMuon']]],
        },
        'Dimensions':   2,
    },

    '2DWMinusMuon'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['WMinusMuon'], ['WMinusMuon']]],
        },
        'Dimensions':   2,
    },

    '2DZLeadingMuon'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['ZLeadingMuon'], ['ZLeadingMuon']]],
        },
        'Dimensions':   2,
    },

    '2DZSubLeadingMuon'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['ZSubLeadingMuon'], ['ZSubLeadingMuon']]],
        },
        'Dimensions':   2,
    },

    '2DZMuons'      :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['ZLeadingMuon', 'ZSubLeadingMuon'], ['ZLeadingMuon', 'ZSubLeadingMuon']]],
        },
        'Dimensions':   2,
    },

    '2DZLeadingJet'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['ZLeadingJet'], ['ZLeadingJet']]],
        },
        'Dimensions':   2,
    },

    '2DZSubLeadingJet'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['ZSubLeadingJet'], ['ZSubLeadingJet']]],
        },
        'Dimensions':   2,
    },

    '2DZJets'       :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['ZLeadingJet', 'ZLeadingJet'], ['ZSubLeadingJet', 'ZSubLeadingJet']]],
        },
        'Dimensions':   2,
    },

    '2DWPlusMuon-FinalBeamElectron'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Eta'], ['Pt', 'Pt']],
            'Particles' :   [[['WPlusMuon'], ['FinalBeamElectron']]],
        },
        'Dimensions':   2,
    },

    '2DWMinusMuonFinalBeamElectron'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Eta'], ['Pt', 'Pt']],
            'Particles' :   [[['WMinusMuon'], ['FinalBeamElectron']]],
        },
        'Dimensions':   2,
    },

    '2DWPlusMuonWMinusMuon'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Eta'], ['Pt', 'Pt']],
            'Particles' :   [[['WPlusMuon'], ['WMinusMuon']]],
        },
        'Dimensions':   2,
    },

    '2DWPlusMuonFinalBeamElectron'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['WPlusMuonFinalBeamElectron'], ['WPlusMuonFinalBeamElectron']]],
        },
        'Dimensions':   2,
    },

    '2DDiMuon'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [[['DiMuon'], ['DiMuon']]],
        },
        'Dimensions':   2,
    },

    '2DDiMuon-WPlusMuonFinalBeamElectron'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Eta'], ['Phi', 'Phi'], ['Pt', 'Pt'], ['M', 'M']],
            'Particles' :   [[['DiMuon'], ['WPlusMuonFinalBeamElectron']]],
        },
        'Dimensions':   2,
    },

    '2DFinalBeamElectron-WMinusMuon'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['qLepton', 'qLepton'], ['qeMethod', 'qeMethod']],
            'Particles' :   [[['FinalBeamElectron'], ['WMinusMuon']]],
        },
        'Dimensions':   2,
    },

    '2DMissingET-FinalBeamElectron'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Et', 'Eta'], ['Et', 'Phi'], ['Et', 'Pt'], ['Et', 'Et']],
            'Particles' :   [[['MissingET'], ['FinalBeamElectron']]],
        },
        'Dimensions':   2,
    },

    '2DFinalBeamJet-ZLeadingJet'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Eta'], ['Phi', 'Phi'], ['Pt', 'Pt'], ['Et', 'Et']],
            'Particles' :   [[['FinalBeamJet'], ['ZLeadingJet']]],
        },
        'Dimensions':   2,
    },

    '2DFinalBeamJet-ZSubLeadingJet'     
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Eta'], ['Phi', 'Phi'], ['Pt', 'Pt'], ['Et', 'Et']],
            'Particles' :   [[['FinalBeamJet'], ['ZSubLeadingJet']]],
        },
        'Dimensions':   2,
    },    
}

# Dictionary to request hist comparisons

'''
HistComparisonDict =  {
  'HistKey'           :   {
      'Hist1'             :   {
          'Name'              :   Hist1Name,
      },
      
      'Hist2'         :   {
          'Name'          :   Hist1Name,
      },

      'Var'           :   [HistVars]
  },
'''

HistComparisonDict =    {

    '1'             :   {
        'Hist1'         :   {
            'Name'          :   'FinalBeamElectron',
        },
        
        'Hist2'         :   {
            'Name'          :   'WPlusMuon',
        },

        'Var'           :   ['Eta', 'Pt']
    },

    '2'             :   {
        'Hist1'         :   {
            'Name'          :   'FinalBeamElectron',
        },
        
        'Hist2'         :   {
            'Name'          :   'WMinusMuon',
        },

        'Var'           :   ['Eta', 'Pt']
    },    

    '3'             :   {
        'Hist1'         :   {
            'Name'          :   'FinalBeamJet',
        },
        
        'Hist2'         :   {
            'Name'          :   'ZJets',
        },

        'Var'           :   ['Eta', 'Pt']
    },

    '4'             :   {
        'Hist1'         :   {
            'Name'          :   'FinalBeamJet',
        },
        
        'Hist2'         :   {
            'Name'          :   'ZLeadingJet',
        },

        'Var'           :   ['Eta', 'Pt']        
    },    

    '5'             :   {
        'Hist1'         :   {
            'Name'          :   'FinalBeamJet',
        },
        
        'Hist2'         :   {
            'Name'          :   'ZSubLeadingJet',
        },

        'Var'           :   ['Eta', 'Pt']    
    },

    '6'             :   {
        'Hist1'         :   {
            'Name'          :   'DiMuon',
        },
        
        'Hist2'         :   {
            'Name'          :   'WPlusMuonFinalBeamElectron',
        },

        'Var'           :   ['Eta', 'Phi', 'Pt']    
    },

    '7'             :   {
        'Hist1'         :   {
            'Name'          :   'FinalBeamElectron',
        },
        
        'Hist2'         :   {
            'Name'          :   'WMinusMuon',
        },

        'Var'           :   ['qeMethod', 'qLepton']    
    },

    '8'             :   {
        'Hist1'         :   {
            'Name'          :   'FinalBeamJet',
        },
        
        'Hist2'         :   {
            'Name'          :   'ZLeadingJet',
        },

        'Var'           :   ['Eta', 'Pt']    
    },

    '9'             :   {
        'Hist1'         :   {
            'Name'          :   'FinalBeamJet',
        },
        
        'Hist2'         :   {
            'Name'          :   'ZSubLeadingJet',
        },

        'Var'           :   ['Eta', 'Pt']    
    },

    '10'             :   {
        'Hist1'         :   {
            'Name'          :   'FinalBeamJet',
        },
        
        'Hist2'         :   {
            'Name'          :   'ZJets',
        },

        'Var'           :   ['Eta', 'Pt']    
    },

    '11'             :   {
        'Hist1'         :   {
            'Name'          :   'AllJets',
        },
        
        'Hist2'         :   {
            'Name'          :   'ZJets',
        },

        'Var'           :   ['Eta', 'Pt']    
    },    

    '12'             :   {
        'Hist1'         :   {
            'Name'          :   'ZLeadingJetFinalBeamJet',
        },
        
        'Hist2'         :   {
            'Name'          :   'ZJets',
        },

        'Var'           :   ['M', 'Mt', 'dR_Eta']    
    },

    '13'             :   {
        'Hist1'         :   {
            'Name'          :   'ZSubLeadingJetFinalBeamJet',
        },
        
        'Hist2'         :   {
            'Name'          :   'ZJets',
        },

        'Var'           :   ['M', 'Mt', 'dR_Eta']    
    },    
}
