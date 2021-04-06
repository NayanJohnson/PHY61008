EventLoopParams = {
    'Level'              :   {
        'Loop'     :   {
            'Cuts'              :   {
                'e_Eta'             :   (-4.3, 4.9),
                'e_Pt'              :   5,
                'mu_Eta'            :   (-4, 4),
                'mu_Pt'             :   5,  
                'jet_Eta'           :   (-4.4, 5),
                'jet_Pt'            :   3,                   
            },

            'NoCuts'            :   {
                'e_Eta'             :   (float('-inf'), float('inf')),
                'e_Pt'              :   0,
                'mu_Eta'            :   (float('-inf'), float('inf')),
                'mu_Pt'             :   0,  
                'jet_Eta'           :   (float('-inf'), float('inf')),
                'jet_Pt'            :   0,                   
            }
        },

        'Event'        :   {
            'Cuts'              :   {
                'Electrons'         :   1,
                'Muons'             :   2,
                'Jets'              :   1,
            },

            'NoCuts'            :   {
                'Electrons'         :   0,
                'Muons'             :   0,
                'Jets'              :   0,
            },
        },

        'Background'     :   {
            'Cuts'              :   {
                'BeamElectron'      :   {
                    'Eta'               :   (-1, float('inf')),
                }
            },

            'NoCuts'            :   {
                    'Eta'               :   (float('-inf'), float('inf')),
                }
            },

    },

    'Z'         :   {
        'Decays' :   (None, None),
        'Mass'      :   91.1876 #GeV
    },      

    'WPlus'     :   {
        'Decays' :   ('Muons', None),
        'Mass'      :   80.379 #GeV
    },      

    'WMinus'    :   {
        'Decays' :   ('Muons', None),
        'Mass'      :   80.379 #GeV
    }   
}   

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
    'MuonSum', 'AllMuons', 
    'LeadingMuon', 'SubLeadingMuon', 'ThirdMuon', 'FourthMuon',
    'LeadingJet', 'SubLeadingJet', 'ThirdJet', 'FourthJet',
    'MissingET', 
    'WPlusElectron', 'WPlusMuon', 'WMinusElectron', 'WMinusMuon',
    'WLeadingJet', 'WSubLeadingJet',
    'ZLeadingElectron', 'ZSubLeadingElectron', 'ZThirdElectron', 'ZFourthElectron',
    'ZLeadingMuon', 'ZSubLeadingMuon', 'ZThirdMuon', 'ZFourthMuon',
    'ZLeadingJet', 'ZSubLeadingJet', 
]

# 'AllJets' also accepted as keyword, but is not initialised as a particle

# Initial parameters for specific var histograms
# Format:
# VarParams =       {
#   Var         :   {
#       Range       :   (min, max)
#   }
# }

VarParams = {
    'Nbins'     :   200,
    'LowRangeNbinsScale'    
                :   1,
    'HighRangeNbinsScale'   
                :   1.25,
    'Count'     :   {
        'Range'     :   (0, 10)
    },

    'Eta'       :   {
        'Range'     :   (-10, 10)
    },

    'Phi'       :   {
        'Range'     :   (-3.5, 3.5)
    },

    'Rapidity'  :   {
        'Range'     :   (-10, 10)
    },
    
    'Pt'        :   {
        'Range'     :   (0, 500)
    },
    
    'Et'        :   {
        'Range'     :   (0, 1500)
    },
    
    'q'         :   {
        'Range'     :   (0, 1000)
    },

    'dEta'      :   {
        'Range'     :   (-20, 20)
    },
    
    'dPhi'      :   {
        'Range'     :   (-3.5, 3.5)
    },
    
    'dRapidity' :   {
        'Range'     :   (-20, 20)
    },
    
    'dR_Eta'    :   {
        'Range'     :   (0, 100)
    },
    
    'dR_Rap'    :   {
        'Range'     :   (0, 100)
    },
    
    'InvMass'   :   {
        'Range'     :   (0, 1000)
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
    },
    
    'Muons'         :   {
        'Requests'      :   {
            'Vars'      :   ['Count'],
            'Particles' :   [],
        },
    },
    
    'Jets'          :   {
        'Requests'      :   {
            'Vars'      :   ['Count'],
            'Particles' :   [],
        },
    },
    
    'FinalBeamElectron' 
                    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['FinalBeamElectron'],
        },
    },
    
    'LeadingMuon'   :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['LeadingMuon'],
        },
    },
    
    'SubLeadingMuon':   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['SubLeadingMuon'],
        },
    },
    
    'ThirdMuon'     :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['ThirdMuon'],
        },
    },    
    
    'FourthMuon'    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['ThirdMuon'],
        },
    },            
        
    'AllJets'       :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['LeadingJet', 'SubLeadingJet', 'ThirdJet', 'FourthJet'],
        },
    },

    'FinalBeamJet'    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['FinalBeamJet'],
        },
    },

    'LeadingJet'    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['LeadingJet'],
        },
    },
        
    'SubLeadingJet' :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['SubLeadingJet'],
        },
    },
        
    'ThirdJet'      :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['ThirdJet'],
        },
    },
        
    'MissingET'     :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', 'Et', ('Eta', 'Pt')],
            'Particles' :   ['MissingET'],
        },
    },

    'WLeadingJet'   :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['WLeadingJet'],
        },
    },

    'WSubLeadingJet':   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['WSubLeadingJet'],
        },
    },    

    'WJets':   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['WLeadingJet', 'WSubLeadingJet'],
        },
    },       

    'WPlusMuon'     :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['WPlusMuon'],
        },
    },

    'WMinusMuon'     :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['WMinusMuon'],
        },
    },

    'ZLeadingMuon'  :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['ZLeadingMuon'],
        },
    },

    'ZSubLeadingMuon'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['ZSubLeadingMuon'],
        },
    },   

    'ZMuons'        :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt'), 'InvMass'],
            'Particles' :   ['ZLeadingMuon', 'ZSubLeadingMuon'],
        },
    }, 

    'ZLeadingJet'   :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['ZLeadingJet'],
        },
    },

    'ZSubLeadingJet'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['ZSubLeadingJet'],
        },
    },   

    'ZJets'         :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt'), 'InvMass'],
            'Particles' :   ['ZLeadingJet', 'ZSubLeadingJet'],
        },
    },     

    'qLepton'      :   {
        'Requests'      :   {
            'Vars'      :   ['q'],
            'Particles' :   ['BeamElectron', 'FinalBeamElectron'],
        },
    },
        
    'qQuark'       :   {
        'Requests'      :   {
            'Vars'      :   ['q'],
            'Particles' :   ['BeamQuark', 'FinalBeamJet'],
        },
    },

    'qeMethod'     :   {
        'Requests'      :   {
            'Vars'      :   ['q'],
            'Particles' :   ['BeamElectron', 'FinalBeamElectron'],
        },
    },

    'FinalBeamElectronLeadingMuon'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['FinalBeamElectron', 'LeadingMuon'],
        },
    },

    'FinalBeamElectronSubLeadingMuon'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['FinalBeamElectron', 'SubLeadingMuon'],
        },
    },

    'FinalBeamElectronLeadingJet'   
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi', 'InvMass'],
            'Particles' :   ['FinalBeamElectron', 'LeadingJet'],
        },
    },

    'MuonMuon'      :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi', 'dRapidity', 'dR_Eta', 'dR_Rap', 'InvMass'],
            'Particles' :   ['LeadingMuon', 'SubLeadingMuon']
        },
    
    'LeadingMuonLeadingJet'
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['LeadingMuon', 'LeadingJet'],
        },
    },

    'SubLeadingMuonLeadingJet'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['SubLeadingMuon', 'LeadingJet'],
        },
    },
    
    'MissingETFinalElectron'    
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['MissingET', 'FinalBeamElectron'],
        },
    },
    
    'MissingETLeadingJet'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['MissingET', 'LeadingJet'],
        },
    },

    'MissingETWMuons'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['MissingET', 'WPlusMuon', 'WMinusMuon'],
        },
    },

    'MissingETLeadingMuon'  
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['MissingET', 'LeadingMuon'],
        },
    },
    
    'MissingETSubLeadingMuon'   
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['MissingET', 'SubLeadingMuon'],
        },
    },

    'MissingETThirdMuon'   
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['MissingET', 'ThirdMuon'],
        },
    },
    
    'MissingETMuonSum'      
                    :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['MissingET', 'MuonSum'],
        },
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
    }
}
