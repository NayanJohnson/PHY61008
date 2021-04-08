EventLoopParams = {
    'Level'              :   {
        'Loop'     :   {
            'Cuts'              :   {
                'e_Eta'             :   (float('-inf'), float('inf')),
                'e_Pt'              :   0,
                'mu_Eta'            :   (float('-inf'), float('inf')),
                'mu_Pt'             :   0,  
                'jet_Eta'           :   (float('-inf'), float('inf')),
                'jet_Pt'            :   0,                       
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
                'Electrons'         :   0,
                'Muons'             :   0,
                'Jets'              :   0
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
                    'Eta'               :   (float('-inf'), float('inf')),
                }
            },

            'NoCuts'            :   {
                'BeamElectron'      :   {
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
        'Decays' :   (None, None),
        'Mass'      :   80.379 #GeV
    },      

    'WMinus'    :   {
        'Decays' :   (None, None),
        'Mass'      :   80.379 #GeV
    }   
}   


