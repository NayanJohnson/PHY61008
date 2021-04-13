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
                'Jets'              :   1
            },

            'NoCuts'            :   {
                'Electrons'         :   0,
                'Muons'             :   0,
                'Jets'              :   0,
            },
        },

        'Analysis'     :   {
            'Cuts'              :   {
                'MissingET'         :   {
                    'Et'            :   (15, float('inf')),
                },

                'FinalBeamElectron' :   {
                    'Eta'               :   (-1, float('inf')),
                }
            },

            'NoCuts'            :   {
                'MissingET'         :   {
                    'Et'            :   (0, float('inf')),
                },
                #
                'FinalBeamElectron' :   {
                    'Eta'               :   (float('-inf'), float('inf')),
                }
            },
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




