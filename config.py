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
    'BeamElectron', 'FinalBeamElectron', 'LeadingMuon', 'SubLeadingMuon', 'MuonSum', 
    'AllMuons', 'WPlusMuon', 'WMinusMuon', 'MissingET', 'BeamQuark', 'BeamJet',
    'LeadingJet', 'SubLeadingJet', 'ThirdJet', 'FourthJet',
]

# 'AllJets' also accepted as keyword, but is not initialised as a particle


HistDict = {
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
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', ('Pt', 'Eta')],
            'Particles' :   ['FinalBeamElectron'],
        },
    },
    
    'LeadingMuon'   :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['LeadingMuon'],
        },
    },
    
    'SubLeadingMuon':   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['SubLeadingMuon'],
        },
    },
    
    'WPlusMuon'     :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['WPlusMuon'],
        },
    },
        
    'WMinusMuon'    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['WMinusMuon'],
        },
    },
        
    'AllJets'       :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['AllJets'],
        },
    },
        
    'LeadingJet'    :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['LeadingJet'],
        },
    },
        
    'SubLeadingJet' :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['SubLeadingJet'],
        },
    },
        
    'ThirdJet'      :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['ThirdJet'],
        },
    },
        
    'FourthJet'     :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['FourthJet'],
        },
    },
        
    'MissingET'     :   {
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', 'Et'],
            'Particles' :   ['MissingET'],
        },
    },
        
    'q_Lepton'      :   {
        'Requests'      :   {
            'Vars'      :   ['q'],
            'Particles' :   ['BeamElectron', 'FinalBeamElectron'],
        },
    },
        
    'q_Quark'       :   {
        'Requests'      :   {
            'Vars'      :   ['q'],
            'Particles' :   ['BeamQuark', 'BeamJet'],
        },
    },

    'q_eMethod'     :   {
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

# Initial Parameters for the

VarParams = {
    'Nbins'     :   10000,
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
        'Range'     :   (-10, 10)
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