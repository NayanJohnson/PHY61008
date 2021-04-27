EventLoopParams = {
    'Signal'            :   {
        'Xsec'              :   7.0e-05,
        'NEvents'           :   50000,        
    },

    'Background'        :   {
        'Xsec'              :   0.057,
        'NEvents'           :   28395,
    },
    'Level'             :   {
        'Loop'              :   {
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
                'Muons'             :   1,
                'Jets'              :   3
            },

            'NoCuts'            :   {
                'Electrons'         :   0,
                'Muons'             :   0,
                'Jets'              :   0,
            },
        },

        'Analysis'     :   {
            'Cuts'              :   {
                
                'LeadingJet'        :   {
                    'Pt'                :   (30, float('inf')),
                },

                'SubLeadingJet'     :   {
                    'Pt'                :   (20, float('inf')),
                },

                'ZJets'             :   {
                    'M'                 :   (50, float('inf')),
                },

                'MissingET'         :   {
                    'Et'                :   (0, float('inf')),
                },

                'FinalBeamElectron' :   {
                    'Eta'               :   (float('-inf'), float('inf')),
                },

                'FinalBeamJet' :   {
                    'Pt'                :   (10, float('inf')),
                }                
            },

            'NoCuts'            :   {
                
                'LeadingJet'        :   {
                    'Pt'                :   (0, float('inf')),
                },

                'SubLeadingJet'     :   {
                    'Pt'                :   (0, float('inf')),
                },

                'ZJets'             :   {
                    'M'                 :   (0, float('inf')),
                },

                'MissingET'         :   {
                    'Et'                :   (0, float('inf')),
                },
                
                'FinalBeamElectron' :   {
                    'Eta'               :   (float('-inf'), float('inf')),
                },

                'FinalBeamJet' :   {
                    'Pt'                :   (0, float('inf')),
                }  
            },
        },
    },

    'Z'         :   {
        'Decays'    :   ('Jets', None),
        'Mass'      :   91.19 #GeV
    },      

    'WPlus'     :   {
        'Decays'    :   (None, None),
        'Mass'      :   80.38 #GeV
    },      

    'WMinus'    :   {
        'Decays'    :   ('Muons', None),
        'Mass'      :   80.38 #GeV
    }   
}   




