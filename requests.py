# Dictionary that will contain all info needed to produce histograms.
# 'Request' dictionary is used to tell the script what variables to
# plot and what particles the histogram requires

VarKeywords = [
    'Count', 'Eta', 'Phi', 'Rapidity', 'Pt', 'Et', 'q', 
    'dEta', 'dPhi', 'dRapidity', 'dR_Eta', 'dR_Rap', 'InvMass'
]

# Tuples of two variables will be treated as 2 dimensions in a 2D histogram


# Particle keywords:
Particles = ['Electron', 'Jet', 'Muon']

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

VarParams = {
    'Nbins'     :   200,
    'LowRangeNbinsScale'    
                :   1,
    'HighRangeNbinsScale'   
                :   1.25,
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
    
    'Pt'        :   {
        'Range'     :   [0, 500]
    },
    
    'Et'        :   {
        'Range'     :   [0, 1500]
    },
    
    'q'         :   {
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
        'Range'     :   [0, 100]
    },
    
    'dR_Rap'    :   {
        'Range'     :   [0, 100]
    },
    
    'InvMass'   :   {
        'Range'     :   [0, 1000]
    },
}

# No entries here can have _ as this is how variables are seperated in the code
# When fully filled:
# HistDict =        {
#   Catagory        :   {
#       Requests        :   {
#           Vars            :   [],
#           Particles       :   []
#       },

#       Vars        :   [],
#       Particles   :   [],
#       Hists       :   {
#           Var1        :   Hist1,
#           Var2        :   Hist2
#       }
#   }
# }
HistDict =  {
    'Electrons'     :   {
        'Requests'      :   {
            'Vars'      :   ['Count'],
            'Particles' :   [],
        },
        'Dimensions':   1,
    },
    
    'Muons'         :   {
        'Requests'      :   {
            'Vars'      :   ['Count'],
            'Particles' :   [],
        },
        'Dimensions':   1,
    },
    
    'Jets'          :   {
        'Requests'      :   {
            'Vars'      :   ['Count'],
            'Particles' :   [],
        },
        'Dimensions':   1,
    },
    
    'FinalBeamElectron' 
                    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['FinalBeamElectron'],
        },
        'Dimensions':   1,
    },
    
    'LeadingMuon'   :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['LeadingMuon'],
        },
        'Dimensions':   1,
    },
    
    'SubLeadingMuon':   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['SubLeadingMuon'],
        },
        'Dimensions':   1,
    },
    
    'ThirdMuon'     :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['ThirdMuon'],
        },
        'Dimensions':   1,
    },    
    
    'FourthMuon'    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['ThirdMuon'],
        },
        'Dimensions':   1,
    },              

    'DiMuon'    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Pt'],
            'Particles' :   ['DiMuon'],
        },
        'Dimensions':   1,
    },

    'WPlusMuonFinalBeamElectron'    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Pt'],
            'Particles' :   ['WPlusMuonFinalBeamElectron'],
        },
        'Dimensions':   1,
    },

    'AllJets'       :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['LeadingJet', 'SubLeadingJet', 'ThirdJet', 'FourthJet'],
        },
        'Dimensions':   1,
    },    

    'FinalBeamJet'    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['FinalBeamJet'],
        },
        'Dimensions':   1,
    },    

    'LeadingJet'    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['LeadingJet'],
        },
        'Dimensions':   1,
    },    

    'SubLeadingJet' :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['SubLeadingJet'],
        },
        'Dimensions':   1,
    },    

    'ThirdJet'      :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['ThirdJet'],
        },
        'Dimensions':   1,
    },    

    'MissingET'     :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', 'Et'],
            'Particles' :   ['MissingET'],          
        },
        'Dimensions':   1,
    },    

    'WLeadingJet'   :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['WLeadingJet'],
        },
        'Dimensions':   1,
    },    

    'WSubLeadingJet':   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['WSubLeadingJet'],
        },
        'Dimensions':   1,
    },    

    'WJets':   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['WLeadingJet', 'WSubLeadingJet'],
        },
        'Dimensions':   1,
    },    

    'WPlusMuon'     :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['WPlusMuon'],
        },
        'Dimensions':   1,
    },    

    'WMinusMuon'     :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['WMinusMuon'],
        },
        'Dimensions':   1,
    },    

    'ZLeadingMuon'  :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['ZLeadingMuon'],
        },
        'Dimensions':   1,
    },    

    'ZSubLeadingMuon'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['ZSubLeadingMuon'],
        },
        'Dimensions':   1,
    },    

    'ZMuons'        :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', 'InvMass'],
            'Particles' :   ['ZLeadingMuon', 'ZSubLeadingMuon'],
        },
        'Dimensions':   1,
    },    

    'ZLeadingJet'   :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['ZLeadingJet'],
        },
        'Dimensions':   1,
    },    

    'ZSubLeadingJet'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['ZSubLeadingJet'],
        },
        'Dimensions':   1,
    },    

    'ZJets'         :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', 'InvMass'],
            'Particles' :   ['ZLeadingJet', 'ZSubLeadingJet'],
        },
        'Dimensions':   1,
    },    

    'qLepton'      :   {
        'Requests'      :   {
            'Vars'      :   ['q'],
            'Particles' :   ['BeamElectron', 'FinalBeamElectron'],
        },
        'Dimensions':   1,
    },    

    'qQuark'       :   {
        'Requests'      :   {
            'Vars'      :   ['q'],
            'Particles' :   ['BeamQuark', 'FinalBeamJet'],
        },
        'Dimensions':   1,
    },    

    'qeMethod'     :   {
        'Requests'      :   {
            'Vars'      :   ['q'],
            'Particles' :   ['BeamElectron', 'FinalBeamElectron'],
        },
        'Dimensions':   1,
    },    

    'FinalBeamElectronLeadingMuon'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['FinalBeamElectron', 'LeadingMuon'],
        },
        'Dimensions':   1,
    },    

    'FinalBeamElectronSubLeadingMuon'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['FinalBeamElectron', 'SubLeadingMuon'],
        },
        'Dimensions':   1,
    },    

    'FinalBeamElectronLeadingJet'   
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi', 'InvMass'],
            'Particles' :   ['FinalBeamElectron', 'LeadingJet'],
        },
        'Dimensions':   1,
    },    

    'MuonMuon'      :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi', 'dRapidity', 'dR_Eta', 'dR_Rap', 'InvMass'],
            'Particles' :   ['LeadingMuon', 'SubLeadingMuon'],
        },
        'Dimensions':   1,
    },    

    'LeadingMuonLeadingJet'
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['LeadingMuon', 'LeadingJet'],
        },
        'Dimensions':   1,
    },    

    'SubLeadingMuonLeadingJet'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['SubLeadingMuon', 'LeadingJet'],
        },
        'Dimensions':   1,
    },    

    'MissingETFinalElectron'    
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['MissingET', 'FinalBeamElectron'],
        },
        'Dimensions':   1,
    },    

    'MissingETLeadingJet'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['MissingET', 'LeadingJet'],
        },
        'Dimensions':   1,
    },    

    'MissingETWMuons'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['MissingET', 'WMuonSum'],
        },
        'Dimensions':   1,
    },    

    'MissingETLeadingMuon'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['MissingET', 'LeadingMuon'],
        },
        'Dimensions':   1,
    },    

    'MissingETSubLeadingMuon'   
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['MissingET', 'SubLeadingMuon'],
        },
        'Dimensions':   1,
    },    

    'MissingETThirdMuon'   
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['MissingET', 'ThirdMuon'],
        },
        'Dimensions':   1,
    },    

    'MissingETMuonSum'      
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['MissingET', 'MuonSum'],
        },
        'Dimensions':   1,
    },    

    '2DFinalBeamElectron' 
                    :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['FinalBeamElectron'], ['FinalBeamElectron']],
        },
        'Dimensions':   2,
    },

    '2DLeadingMuon'   :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['LeadingMuon'], ['LeadingMuon']],
        },
        'Dimensions':   2,
    },

    '2DSubLeadingMuon'   :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['SubLeadingMuon'], ['SubLeadingMuon']],
        },
        'Dimensions':   2,
    },

    '2DThirdMuon'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['ThirdMuon'], ['ThirdMuon']],
        },
        'Dimensions':   2,
    },

    '2DFourthMuon'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['FourthMuon'], ['FourthMuon']],
        },
        'Dimensions':   2,
    },

    '2DAllJets'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['LeadingJet', 'SubLeadingJet', 'ThirdJet', 'FourthJet'], ['LeadingJet', 'SubLeadingJet', 'ThirdJet', 'FourthJet']],
        },
        'Dimensions':   2,
    },

    '2DFinalBeamJet'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['FinalBeamJet'], ['FinalBeamJet']],
        },
        'Dimensions':   2,
    },

    '2DLeadingJet'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['LeadingJet'], ['LeadingJet']],
        },
        'Dimensions':   2,
    },

    '2DSubLeadingJet'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['SubLeadingJet'], ['SubLeadingJet']],
        },
        'Dimensions':   2,
    },

    '2DThirdJet'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['ThirdJet'], ['ThirdJet']],
        },
        'Dimensions':   2,
    },

    '2DMissingET'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['MissingET'], ['MissingET']],
        },
        'Dimensions':   2,
    },

    '2DWLeadingJet'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['WLeadingJet'], ['WLeadingJet']],
        },
        'Dimensions':   2,
    },

    '2DWSubLeadingJet'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['WSubLeadingJet'], ['WSubLeadingJet']],
        },
        'Dimensions':   2,
    },

    '2DWJets'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['WLeadingJet', 'WSubLeadingJet'], ['WLeadingJet', 'WSubLeadingJet']],
        },
        'Dimensions':   2,
    },

    '2DWPlusMuon'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['WPlusMuon'], ['WPlusMuon']],
        },
        'Dimensions':   2,
    },

    '2DWMinusMuon'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['WMinusMuon'], ['WMinusMuon']],
        },
        'Dimensions':   2,
    },

    '2DZLeadingMuon'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['ZLeadingMuon'], ['ZLeadingMuon']],
        },
        'Dimensions':   2,
    },

    '2DZSubLeadingMuon'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['ZSubLeadingMuon'], ['ZSubLeadingMuon']],
        },
        'Dimensions':   2,
    },

    '2DZMuons'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['ZLeadingMuon', 'ZSubLeadingMuon'], ['ZLeadingMuon', 'ZSubLeadingMuon']],
        },
        'Dimensions':   2,
    },

    '2DZLeadingJet'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['ZLeadingJet'], ['ZLeadingJet']],
        },
        'Dimensions':   2,
    },

    '2DZSubLeadingJet'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['ZSubLeadingJet'], ['ZSubLeadingJet']],
        },
        'Dimensions':   2,
    },

    '2DZJets'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Pt']],
            'Particles' :   [['ZSubLeadingJet', 'ZSubLeadingJet'], ['ZSubLeadingJet', 'ZSubLeadingJet']],
        },
        'Dimensions':   2,
    },

    '2DWPlusMuonFinalBeamElectron'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Eta'], ['Pt', 'Pt']],
            'Particles' :   [['WPlusMuon'], ['FinalBeamElectron']],
        },
        'Dimensions':   2,
    },

    '2DWMinusMuonFinalBeamElectron'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Eta'], ['Pt', 'Pt']],
            'Particles' :   [['WMinusMuon'], ['FinalBeamElectron']],
        },
        'Dimensions':   2,
    },

    '2DWPlusMuonWMinusMuon'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Eta'], ['Pt', 'Pt']],
            'Particles' :   [['WPlusMuon'], ['WMinusMuon']],
        },
        'Dimensions':   2,
    },

    '2DDiMuon-WPlusMuonFinalBeamElectron'     :   {
        'Requests'      :   {
            'Vars'      :   [['Eta', 'Eta'], ['Phi', 'Phi'], ['Pt', 'Pt']],
            'Particles' :   [['DiMuon'], ['WPlusMuonFinalBeamElectron']],
        },
        'Dimensions':   2,
    },

}

# Dictionary to request hist comparisons
# Format:
# HistComparisonDict =  {
#   'HistKey'           :   {
#       'Hist1'             :   {
#           'Name'              :   Hist1Name,
#           'File'              :   Hist1FileIndex
#       },
#       
#       'Hist2'         :   {
#           'Name'          :   Hist1Name,
#           'File'          :   Hist2FileIndex
#       },
#
#       'Var'           :   HistVars
#   },

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
    }
}
