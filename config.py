# Dictionary that will contain all info needed to produce histograms.
# 'Request' dictionary is used to tell the script what variables to
# plot and what particles the histogram requires

VarKeywords = [
    'Count', 'Eta', 'Phi', 'Rapidity', 'Pt', 'Et', 'q', 
    'dEta', 'dPhi', 'dRapidity', 'dR_Eta', 'dR_Rap', 'InvMass'
]

# Touples of two variables will be treated as 2 dimensions in a 2D histogram


# Particle keywords:
ParticleKeywords = [
    'BeamElectron', 'LeadingElectron', 'FinalBeamElectron', 
    'LeadingMuon', 'SubLeadingMuon', 'ThirdMuon', 'MuonSum', 'AllMuons', 
    'WPlusMuon', 'WMinusMuon', 'ZLeadingMuon', 'ZSubLeadingMuon', 
    'MissingET', 'BeamQuark', 
    'BeamJet', 'LeadingJet', 'SubLeadingJet', 'ThirdJet', 'FourthJet',
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
    # Initial Nbins is large so that the bins can later be rescaled
    'Nbins'     :   5000,
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
        'Range'     :   (0, 1000)
    },
    
    'Et'        :   {
        'Range'     :   (0, 1500)
    },
    
    'q'         :   {
        'Range'     :   (0, 10000)
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
        'Range'     :   (0, 10000)
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
    
    'WPlusMuon'     :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['WPlusMuon'],
        },
    },
        
    'WMinusMuon'    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['WMinusMuon'],
        },
    },
        
    'AllJets'       :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['AllJets'],
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
        
    'FourthJet'     :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Eta', 'Pt')],
            'Particles' :   ['FourthJet'],
        },
    },
        
    'MissingET'     :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', 'Et', ('Eta', 'Pt')],
            'Particles' :   ['MissingET'],
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
            'Particles' :   ['BeamQuark', 'BeamJet'],
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
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['FinalBeamElectron', 'LeadingJet'],
        },
    },

    'MuonMuon'      :   {
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi', 'dRapidity', 'dR_Eta', 'dR_Rap', 'InvMass'],
            'Particles' :   ['LeadingMuon', 'SubLeadingMuon'],
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
            'File'          :   1
        },
        
        'Hist2'         :   {
            'Name'          :   'WPlusMuon',
            'File'          :   1
        },

        'Var'           :   ['Eta', 'Pt']
    },

    '2'             :   {
        'Hist1'         :   {
            'Name'          :   'FinalBeamElectron',
            'File'          :   1
        },
        
        'Hist2'         :   {
            'Name'          :   'WMinusMuon',
            'File'          :   1
        },

        'Var'           :   ['Eta', 'Pt']
    }
}