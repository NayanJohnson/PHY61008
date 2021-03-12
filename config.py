# Dictionary that will contain all info needed to produce histograms.
# 'Request' dictionary is used to tell the script what variables to
# plot and what particles the histogram requires

# Var keywords:
# ['Count', 'Eta', 'Phi', 'Rapidity', 'Pt', 'Et', 'q', 
# 'dEta', 'dPhi', 'dRapidity', 'dR_Eta', 'dR_Rap', 'InvMass']

# Particle keywords:
ParticleKeywords = [
    'BeamElectron', 'FinalBeamElectron', 'LeadingMuon', 'SubLeadingMuon', 'MuonSum', 
    'AllMuons', 'WPlusMuon', 'WMinusMuon', 'MissingET', 'BeamQuark', 'BeamJet',
    'LeadingJet', 'SubLeadingJet', 'ThirdJet', 'FourthJet',
]

# 'AllJets' also accepted as keyword, but is not initialised as a particle


HistDict = {
    'Electrons'     :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['Count'],
            'Particles' :   [],
        },
    },
    
    'Muons'         :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['Count'],
            'Particles' :   [],
        },
    },
    
    'Jets'          :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['Count'],
            'Particles' :   [],
        },
    },
    
    'FinalBeamElectron' 
                    :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['FinalBeamElectron'],
        },
    },
    
    'LeadingMuon'   :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['LeadingMuon'],
        },
    },
    
    'SubLeadingMuon':   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['SubLeadingMuon'],
        },
    },
    
    'WPlusMuon'     :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['WPlusMuon'],
        },
    },
        
    'WMinusMuon'    :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['WMinusMuon'],
        },
    },
        
    'AllJets'       :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['AllJets'],
        },
    },
        
    'LeadingJet'    :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['LeadingJet'],
        },
    },
        
    'SubLeadingJet' :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['SubLeadingJet'],
        },
    },
        
    'ThirdJet'      :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['ThirdJet'],
        },
    },
        
    'FourthJet'     :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt'],
            'Particles' :   ['FourthJet'],
        },
    },
        
    'MissingET'     :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['Eta', 'Phi', 'Rapidity', 'Pt', 'Et'],
            'Particles' :   ['MissingET'],
        },
    },
        
    'q_Lepton'      :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['q'],
            'Particles' :   ['BeamElectron', 'FinalBeamElectron'],
        },
    },
        
    'q_Quark'       :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['q'],
            'Particles' :   ['BeamQuark', 'BeamJet'],
        },
    },

    'q_eMethod'     :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['q'],
            'Particles' :   ['BeamElectron', 'FinalBeamElectron'],
        },
    },

    'FinalBeamElectronLeadingMuon'  
                    :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['FinalBeamElectron', 'LeadingMuon'],
        },
    },

    'FinalBeamElectronSubLeadingMuon'  
                    :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['FinalBeamElectron', 'SubLeadingMuon'],
        },
    },

    'FinalBeamElectronLeadingJet'   
                    :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['FinalBeamElectron', 'LeadingJet'],
        },
    },

    'MuonMuon'      :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi', 'dRapidity', 'dR_Eta', 'dR_Rap', 'InvMass'],
            'Particles' :   ['LeadingMuon', 'SubLeadingMuon'],
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['LeadingMuon', 'LeadingJet'],
        },
    },

    'SubLeadingMuonLeadingJet'  
                    :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['SubLeadingMuon', 'LeadingJet'],
        },
    },
    
    'MissingETFinalElectron'    
                    :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['MissingET', 'FinalBeamElectron'],
        },
    },
    
    'MissingETLeadingJet'  
                    :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['MissingET', 'LeadingJet'],
        },
    },
    
    'MissingETLeadingMuon'  
                    :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['MissingET', 'LeadingMuon'],
        },
    },
    
    'MissingETSubLeadingMuon'   
                    :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['MissingET', 'SubLeadingMuon'],
        },
    },
    
    'MissingETMuonSum'      
                    :   {
        'Dimensions'    :   1,
        'Requests'      :   {
            'Vars'      :   ['dEta', 'dPhi'],
            'Particles' :   ['MissingET', 'MuonSum'],
        },
    },
    
    'Final'
}

VarParams = {
    'Count'     :   {
        'Nbins'     :   200,
        'Range'     :   (0, 10)
    },

    'Eta'       :   {
        'Nbins'     :   200,
        'Range'     :   (-10, 10)
    },

    'Phi'       :   {
        'Nbins'     :   200,
        'Range'     :   (-3.5, 3.5)
    },

    'Rapidity'  :   {
        'Nbins'     :   200,
        'Range'     :   (-10, 10)
    },
    
    'Pt'        :   {
        'Nbins'     :   1000,
        'Range'     :   (0, 1000)
    },
    
    'Et'        :   {
        'Nbins'     :   1500,
        'Range'     :   (0, 1500)
    },
    
    'q'         :   {
        'Nbins'     :   1000,
        'Range'     :   (0, 10000)
    }

    'dEta'      :   {
        'Nbins'     :   200,
        'Range'     :   (-10, 10)
    },
    
    'dPhi'      :   {
        'Nbins'     :   200,
        'Range'     :   (-3.5, 3.5)
    },
    
    'dRapidity' :   {
        'Nbins'     :   200,
        'Range'     :   (-20, 20)
    },
    
    'dR_Eta'    :   {
        'Nbins'     :   1000,
        'Range'     :   (0, 100)
    },
    
    'dR_Rap'    :   {
        'Nbins'     :   1000,
        'Range'     :   (0, 100)
    },
    
    'InvMass'   :   {
        'Nbins'     :   2000,
        'Range'     :   (0, 10000)
    },
}