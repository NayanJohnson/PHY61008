# This file contains info specific to the process 
# ie this is the file that changes with branch

EventLoopParams = {
    #MET>15
    # Dataset xsec and NEvents
    'Signal'            :   {
        'Xsec'              :   0.00036,
        'NEvents'           :   41298,        
    },

    'Background'        :   {
        'Xsec'              :   2.9,
        'NEvents'           :   559,
    },

    # Cuts for the various levels
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
                
                'LeadingJet'        :   {
                    'Pt'                :   (0, float('inf')),
                },

                'SubLeadingJet'     :   {
                    'Pt'                :   (0, float('inf')),
                },

                'ZJets'             :   {
                    'M'                 :   (0, float('inf')),
                },

                'ZLeading_FinalBeam_Jets' 
                                    :   {
                    'dR_Eta'            :   (0, float('inf')),
                    'M'                 :   (0, float('inf')),
                    'Mt'                :   (0, float('inf')),
                    'Pt'                :   (0, float('inf')),                    
                },    

                'ZSubLeading_FinalBeam_Jets' 
                                    :   {
                    'dR_Eta'            :   (0, float('inf')),
                    'M'                 :   (0, float('inf')),
                    'Mt'                :   (0, float('inf')),
                    'Pt'                :   (0, float('inf')),                    
                },       

                'MissingET'         :   {
                    'Et'                :   (0, float('inf')),
                },

                'FinalBeamElectron' :   {
                    'Eta'               :   (float('-inf'), float('inf')),
                },

                'FinalBeamJet'      :   {
                    'Pt'                :   (0, float('inf')),
                },                                
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

                'ZLeading_FinalBeam_Jets' 
                                    :   {
                    'dR_Eta'            :   (0, float('inf')),
                    'M'                 :   (0, float('inf')),
                    'Mt'                :   (0, float('inf')),
                    'Pt'                :   (0, float('inf')),                    
                },       

                'ZSubLeading_FinalBeam_Jets' 
                                    :   {
                    'dR_Eta'            :   (0, float('inf')),
                    'M'                 :   (0, float('inf')),
                    'Mt'                :   (0, float('inf')),
                    'Pt'                :   (0, float('inf')),                    
                },       

                'MissingET'         :   {
                    'Et'                :   (0, float('inf')),
                },

                'FinalBeamElectron' :   {
                    'Eta'               :   (float('-inf'), float('inf')),
                },

                'FinalBeamJet'      :   {
                    'Pt'                :   (0, float('inf')),
                },      
            },
        },
    },

    # Boson masses and expected decays  
    'Z'         :   {
        'Decays'    :   (None, None),
        'Mass'      :   91.19 #GeV
    },      

    'WPlus'     :   {
        'Decays'    :   ('Muons', None),
        'Mass'      :   80.38 #GeV
    },      

    'WMinus'    :   {
        'Decays'    :   ('Muons', None),
        'Mass'      :   80.38 #GeV
    }   
}   




