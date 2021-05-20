from ROOT import TH1F, TH2F, TCanvas, TLegend, SetOwnership, TColor

import config, requests, itertools
import Particle_Funcs as ParticleFuncs
import Loop_Funcs as LoopFuncs

'''
Definitions of used objects:

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
    Particles   :   [( xparticle1, xparticle2 ...), (y1particle1, yparticle2, ...)],
    Hists       :   {name1 : hist1, ... },

'''

def GetScale(Xsec, NEvents):
    '''
        Given the path to the pythia log file and the number of events,
        will return the scaling factor calculated from the process 
        cross section. 
    '''
    
    # L_int(Data) = 1 [ab-1] = 1000000 [pb-1]
    # L_int(MC) = N/Xsec [pb-1]
    # Scale = L_int(Data) / L_int(MC)
    Scale = 1000000 / (NEvents/Xsec)

    return Scale

def MakeHists(HistDict):
    '''
        Will initialise histograms using HistDict[Category][Requests][Vars] list
        and add them to HistDict[Category][Hists].
    '''

    VarParams = requests.VarParams
    NbinsDefault = VarParams['Nbins']
    LowRangeBinScale = VarParams['LowRangeNbinsScale']
    HighRangeBinScale = VarParams['HighRangeNbinsScale']

    for name, attributes in HistDict.items():
        attributes['Hists'] = {}
        
        # 1D Hists
        if attributes['Dimensions'] == 1:
            for var in attributes['Requests']['Vars']:
                histName = name+'_'+var
                histTitle = histName+';'+var+';Frequency'

                histXlow = VarParams[var]['Range'][0]
                histXup = VarParams[var]['Range'][1]
                histXrange = histXup-histXlow

                if histXrange <= 10:
                    histXNbins = int(NbinsDefault * 1/2 * LowRangeBinScale)
                elif histXrange <= 100:
                    # Scales number of bins dependng on var range
                    histXNbins = int(NbinsDefault * LowRangeBinScale)
                else:
                    histXNbins = int(NbinsDefault * HighRangeBinScale)

                hist = TH1F(histName, histTitle, histXNbins, histXlow, histXup)


                hist.SetOption('HIST')
                # Adds the hist to the dict
                HistDict[name]['Hists'][var] = hist

        # 2D Hists
        elif attributes['Dimensions'] == 2: 
            for pair in attributes['Requests']['Vars']:
                histName = name+'_'+pair[0]+'_'+pair[1]

                if attributes['Requests']['Particles'][0][0] == attributes['Requests']['Particles'][0][1]:
                    histTitle = histName+';'+pair[0]+';'+pair[1]+';Frequency'
                else:
                    histTitle = histName+';'+attributes['Requests']['Particles'][0][0][0]+'_'+pair[0]+';'+attributes['Requests']['Particles'][0][1][0]+'_'+pair[1]+';Frequency'


                histXlow = VarParams[pair[0]]['Range'][0]
                histXup = VarParams[pair[0]]['Range'][1]
                histXrange = histXup-histXlow

                if histXrange <= 10:
                    histXNbins = int(NbinsDefault * 1/2 * LowRangeBinScale)
                elif histXrange <= 100:
                    # Scales number of bins dependng on var range
                    histXNbins = int(NbinsDefault * LowRangeBinScale)
                else:
                    histXNbins = int(NbinsDefault * HighRangeBinScale)

                histYlow = VarParams[pair[1]]['Range'][0]
                histYup = VarParams[pair[1]]['Range'][1]        
                histYrange = histYup-histYlow

                if histYrange <= 10:
                    histYNbins = int(NbinsDefault * 1/2 * LowRangeBinScale)
                elif histYrange <= 100:
                    # Scales number of bins dependng on var range
                    histYNbins = int(NbinsDefault * LowRangeBinScale)
                else:
                    histYNbins = int(NbinsDefault * HighRangeBinScale)                    

                hist = TH2F(histName, histTitle, histXNbins, histXlow, histXup, histYNbins, histYlow, histYup)
                
                hist.SetOption('HIST COLZ')
                # Adds the hist to the dict
                HistDict[name]['Hists'][pair[0]+'_'+pair[1]]    =   hist

    return HistDict

def FillHists(HistDict, ParticleDict):
    '''
        Given a HistDict, will fill the histograms.
    '''
    
    # List of variables that are stored in all particles.
    ParticleProperties = ['PID', 'E', 'Eta', 'Phi', 'Rapidity', 'Theta', 'Pt', 'Et']

    for category, attributes in HistDict.items():
        if attributes['Dimensions'] == 1:
            for xVar, hist in attributes['Hists'].items():

                # Count var can be read straight from attributes
                if xVar == 'Count': 
                    hist.Fill(attributes['Count'])

                else:
                    for xParticles in attributes['Particles']:

                        # Get the variable of the particle in question
                        xVal = ParticleFuncs.GetParticleVariable(ParticleDict, xParticles, xVar)

                        # If a value is returned
                        if xVal:
                            # If the function returns a list fill the hist for each
                            # element in list
                            if type(xVal) is list:
                                for val in xVal:
                                    hist.Fill(val)
                            else:
                                hist.Fill(xVal)

        elif attributes['Dimensions'] == 2:
            for key, hist in attributes['Hists'].items():
                
                # 2D hist key = 'xVar_yVar'
                xVar, yVar = key.split('_')[0], key.split('_')[1]

                # attributes['Particles'] = [(xParticles), (yParticles)]
                for Comparison in attributes['Particles']:

                    # Comparison = [(xParticles), (yParticles)]
                    xParticles, yParticles = Comparison[0], Comparison[1]

                    xVal = ParticleFuncs.GetParticleVariable(ParticleDict, xParticles, xVar)
                    yVal = ParticleFuncs.GetParticleVariable(ParticleDict, yParticles, yVar)

                    # If values are returned
                    if xVal and yVal:
                    
                        if type(xVal) == list and type(yVal) == list:                            
                            # each element in xVal yVal corresponds to the corresponding particles
                            # in xParticles, yParticles
                            for x, y in zip(xVal, yVal):
                                hist.Fill(x, y)
                        else:
                            hist.Fill(xVal, yVal)

def HistLims(hist, name, var, Scale=1, Norm=False, Change1D=True, Change2D=True):
    '''
        Rescales hist lims.
        Passed objects:
        hist        :   histogram
        Scale       :   float used to scale histrogram - default is 1.
        Norm        :   Should the hist be normalised?
    '''    
    XMin, XMax, YMin, YMax = False, False, False, False

    try:
        hist.Integral()
    except AttributeError:
        print(name, var)

    if Norm and hist.Integral() != 0:
        # Normalises the hist    
        hist.Scale(1./hist.Integral())
    else:
        hist.Scale(Scale)

    ThresholdMin = (hist.Integral()/200) * 1/100                # Skip if hist = False
    if hist:
        if Change1D:
            if hist.GetDimension() == 1:
                # Recalculating Max Min with higher threshold - this is possible as 
                # the hists have been rebinned to a large width
                # Get the index of the min/max bin and the read off the value of the 
                # low edge
                # Set FindLastBinAbove threshold to 5 since otherwise the 
                # hist goes on for way too long
                BinMaxX = hist.GetBinLowEdge(hist.FindLastBinAbove(ThresholdMin, 1))
                BinMinX = hist.GetBinLowEdge(hist.FindFirstBinAbove(0, 1))
                # Max/min = BinMax/min +- 5% +- 5 (prevents max=min for BinMax/Min=0)
                XMax = BinMaxX + 5
                XMin = BinMinX - 5

                hist.SetAxisRange(XMin, XMax, 'X')

        elif hist.GetDimension() == 2:
            if Change2D:

                xVar  = var.split('_')[-2]
                yVar  = var.split('_')[-1]

                # Recalculating Max Min with higher threshold - this is possible as 
                # the hists have been rebinned to a large width
                # Get the index of the min/max bin and the read off the value of the 
                # low edge
                # Set FindLastBinAbove threshold to 2 since the particles are now spread
                # between two vars so the bins will be less filled 
                # hist goes on for way too long
                # For 2D hist must first get axis before using TH1 methods
                BinMaxX = hist.GetXaxis().GetBinLowEdge(hist.FindLastBinAbove(ThresholdMin, 1))
                BinMinX = hist.GetXaxis().GetBinLowEdge(hist.FindFirstBinAbove(0, 1))
                BinMaxY = hist.GetYaxis().GetBinLowEdge(hist.FindLastBinAbove(ThresholdMin, 2))
                BinMinY = hist.GetYaxis().GetBinLowEdge(hist.FindFirstBinAbove(0, 2))                
                # Max/min = BinMax/min +- 5 (prevents max=min for BinMax/Min=0)
                XMax = BinMaxX + 5
                XMin = BinMinX - 5
                YMax = BinMaxY + 5
                YMin = BinMinY - 5        

                hist.SetAxisRange(XMin, XMax, 'X')
                hist.SetAxisRange(YMin, YMax, 'Y')

    return hist, [(XMin, XMax), (YMin, YMax)]

def CompareHist(HistProps, MediaDir, LimChange=True):
    '''
        Given a histogram dictionary and 
         
        Histogram properties dictionary should be in the following format:
        HistFiles = {
            1               :   {
                'Prefix'        21:  _Prefix,
        1    'LoopRun'    2   :  HistFile1_LoopRun,
1              'EventRu2n'     :   HistFile1_EventRun,
                'AnalysisRun'   :   HistFile1_AnalysisRun,
                'Name'          :   HistFile1_Name,

                'File'          :   TFile(HistFile1_Name+'.root')
            },

            2   :   {
                'Prefix'        :   HistFile2_Prefix,
                'LoopRun'       :   HistFile2_LoopRun,
                'EventRun'      :   HistFile2_EventRun,
                'AnalysisRun'   :   HistFile2_AnalysisRun,
                'Name'          :   HistFile2_Name,

                'File'          :   TFile(HistFile2_Name+'.root')
            },
        }

        HistProps = {
            'Hist1'     :   {
                'Hist'      :   Hist1,
                'HistName'  :   HistName,
                'HistVar'   :   HistVar,
                'FileDict'  :   HistFiles[1]
            },

            'Hist2'     :   {
                'Hist'      :   Hist2,
                'HistName'  :   HistName,
                'HistVar'   :   HistVar,
                'FileDict'  :   HistFiles[2]

            },
            
            'Norm'      :   Norm
        }
    '''
    
    Norm = HistProps['Norm']
    if Norm:
        Comparison = 'Norm'
    else:
        Comparison = 'Rel'

    Hist1Name = HistProps['Hist1']['HistName']
    Hist1Var = HistProps['Hist1']['HistVar']
    Hist1 = HistProps['Hist1']['FileDict']['File'].Get(Hist1Name+'_'+Hist1Var+';1')

    Hist1File_Prefix = HistProps['Hist1']['FileDict']['Prefix']
    Hist1File_LevelRun = HistProps['Hist1']['FileDict']['LevelRun']
    Hist1File_LoopRun = HistProps['Hist1']['FileDict']['LoopRun']
    Hist1File_EventRun = HistProps['Hist1']['FileDict']['EventRun']
    Hist1File_AnalysisRun = HistProps['Hist1']['FileDict']['AnalysisRun']

    Hist2Name = HistProps['Hist2']['HistName']
    Hist2Var = HistProps['Hist2']['HistVar']
    Hist2 = HistProps['Hist2']['FileDict']['File'].Get(Hist2Name+'_'+Hist2Var+';1')
    
    Hist2File_Prefix = HistProps['Hist2']['FileDict']['Prefix']
    Hist2File_LevelRun = HistProps['Hist2']['FileDict']['LevelRun']
    Hist2File_LoopRun = HistProps['Hist2']['FileDict']['LoopRun']
    Hist2File_EventRun = HistProps['Hist2']['FileDict']['EventRun']
    Hist2File_AnalysisRun = HistProps['Hist2']['FileDict']['AnalysisRun']

    # print(HistProps)
    Hist1, Lims1 = HistLims(Hist1, Hist1Name, Hist1Var, Norm=Norm)
    Hist2, Lims2 = HistLims(Hist2, Hist2Name, Hist2Var, Norm=Norm)

    # Clear canvas
    HistCan = TCanvas()
    HistCan.cd()

    if Lims1[0][0] and Lims2[0][0] and Lims1[0][1] and Lims2[0][1]:
        XMin = min(Lims1[0][0], Lims2[0][0])
        XMax = max(Lims1[0][1], Lims2[0][1])

        Hist1.SetAxisRange(XMin, XMax, 'X')
        Hist2.SetAxisRange(XMin, XMax, 'X')

        #2D hists
        if Hist1.GetDimension() == 2:
            if Lims1[1][0] and Lims2[1][0] and Lims1[1][1] and Lims2[1][1]:
                YMin = min(Lims1[1][0], Lims2[1][0])
                YMax = max(Lims1[1][1], Lims2[1][1])
                Hist1.SetAxisRange(YMin, YMax, 'Y')
                Hist2.SetAxisRange(YMin, YMax, 'Y')

    # max frequency
    Max1 = Hist1.GetMaximum() + Hist1.GetMaximum()/10
    Max2 = Hist2.GetMaximum() + Hist2.GetMaximum()/10
    # Take the larger value from the two hists
    Max = max(Max1, Max2)

    # Setting universal hist options
    for hist in (Hist1, Hist2):
        # SetBins actually introduces an offset into the graph
        hist.SetStats(False)
        hist.SetMaximum(Max)


    # Legend properties
    LegendX1 = .8
    LegendX_interval = 0.2
    LegendY1 = .95
    LegendY_interval = 0.1

    Legend1 = TLegend(LegendX1, LegendY1 , LegendX1+LegendX_interval, LegendY1-LegendY_interval)
    # Stops legend overwriting canvas
    SetOwnership(Legend1,False)
    Legend1.SetBorderSize(1)
    Legend1.SetShadowColor(2)
    Legend1.SetHeader(Hist1Name)
    # Entries
    Legend1.AddEntry('entries','Entries: '+str(int(Hist1.GetEntries())))
    Legend1.AddEntry(Hist1, 'Line Color', 'l')
    Legend1.SetTextSize(0.025)
    Legend1.SetTextColor(1)
    # Seperation is small, but will be maximised to the bounds of the TLegend
    # box
    Legend1.SetEntrySeparation(.1)

    Legend2 = TLegend(LegendX1, LegendY1-LegendY_interval , LegendX1+LegendX_interval, LegendY1-2*LegendY_interval)
    # Stops legend overwriting canvas    
    SetOwnership(Legend2,False)
    Legend2.SetBorderSize(1)
    Legend2.SetShadowColor(2)
    # Entries
    Legend2.AddEntry('entries','Entries: '+str(int(Hist2.GetEntries())))
    Legend2.AddEntry(Hist2, 'Line Color', 'l')
    Legend2.SetTextSize(0.025)       
    # Seperation is small, but will be maximised to the bounds of the TLegend
    # box
    Legend2.SetEntrySeparation(.1)

    HistTitle = Hist1Name+'_'+Hist2Name

    if Hist1File_Prefix == Hist2File_Prefix:
        Hist1PrefixLabel = ''
        Hist2PrefixLabel = ''
    else:
        Hist1PrefixLabel = Hist1File_Prefix+'_'
        Hist2PrefixLabel = Hist2File_Prefix+'_'        

    if Hist1Name == Hist2Name:
        Hist1NameLabel = ''
        Hist2NameLabel = ''
    else:
        Hist1NameLabel = Hist1Name+'_'
        Hist2NameLabel = Hist2Name+'_'

    if Hist1File_LevelRun == Hist2File_LevelRun:
        Hist1LevelLabel = ''
        Hist2LevelLabel = ''
    else:
        Hist1LevelLabel = Hist1File_LevelRun+'Level'
        Hist2LevelLabel = Hist2File_LevelRun+'Level'

    if Hist1File_LoopRun == Hist2File_LoopRun:
        Hist1LoopLabel = ''
        Hist2LoopLabel = ''
    else:
        Hist1LoopLabel = 'Loop'+Hist1File_LoopRun
        Hist2LoopLabel = 'Loop'+Hist2File_LoopRun

    if Hist1File_EventRun == Hist2File_EventRun:
        Hist1EventLabel = ''
        Hist2EventLabel = ''
    else:
        Hist1EventLabel = 'Event'+Hist1File_EventRun
        Hist2EventLabel = 'Event'+Hist2File_EventRun
    
    if Hist1File_AnalysisRun == Hist2File_AnalysisRun:
        Hist1AnalysisLabel = ''
        Hist2AnalysisLabel = ''
    else:
        Hist1AnalysisLabel = 'Analysis'+Hist1File_AnalysisRun
        Hist2AnalysisLabel = 'Analysis'+Hist2File_AnalysisRun

    Hist1.SetTitle(HistTitle)

    Legend1.SetHeader(Hist1PrefixLabel+Hist1NameLabel+Hist1LevelLabel+Hist1LoopLabel+Hist1EventLabel+Hist1AnalysisLabel)
    Legend2.SetHeader(Hist2PrefixLabel+Hist2NameLabel+Hist2LevelLabel+Hist2LoopLabel+Hist2EventLabel+Hist2AnalysisLabel)

    if Hist1.GetDimension() == 1:
        # Force both to be drawn as hist and on the same canvas
        Hist1.SetLineColor(4)        
        Hist1.Draw('HIST same')
        Hist2.SetLineColor(2)
        Hist2.Draw('HIST same')
    elif Hist1.GetDimension() == 2:
        TColor.SetPalette(59, 0)
        Hist1.Draw('COLZ same')
        
        TColor.SetPalette(60, 0)
        Hist2.Draw('COLZ same')

    Legend1.Draw('same')
    Legend2.Draw('same')

    HistCan.Update()
    with LoopFuncs.Quiet():
        if Hist1Name == Hist2Name:
            HistCan.SaveAs(MediaDir+Comparison+Hist1File_Prefix+Hist2File_Prefix+'/Loop'+Hist1File_LoopRun+'-'+Hist2File_LoopRun+'/Event'+Hist1File_EventRun+'-'+Hist2File_EventRun+'/Analysis'+Hist1File_AnalysisRun+'-'+Hist2File_AnalysisRun+'/'+Hist1File_LevelRun+'-'+Hist2File_LevelRun+'Level/'+Hist1Name+Hist1Var+'.png')
        else:
            HistCan.SaveAs(MediaDir+Comparison+Hist1File_Prefix+Hist2File_Prefix+'/Loop'+Hist1File_LoopRun+'-'+Hist2File_LoopRun+'/Event'+Hist1File_EventRun+'-'+Hist2File_EventRun+'/Analysis'+Hist1File_AnalysisRun+'-'+Hist2File_AnalysisRun+'/'+Hist1File_LevelRun+'-'+Hist2File_LevelRun+'Level/'+Hist1Name+Hist2Name+Hist1Var+'.png')

    HistCan.Clear()

    Hist1.Rebin(5)
    Hist2.Rebin(5)

    Sig_Back = Hist1.Clone()
    Sig_Back.Divide(Hist1,Hist2)

    Sig_Back.Draw()
    HistCan.Update()
    with LoopFuncs.Quiet():
        if Hist1Name == Hist2Name:
            HistCan.SaveAs(MediaDir+Comparison+Hist1File_Prefix+Hist2File_Prefix+'/Loop'+Hist1File_LoopRun+'-'+Hist2File_LoopRun+'/Event'+Hist1File_EventRun+'-'+Hist2File_EventRun+'/Analysis'+Hist1File_AnalysisRun+'-'+Hist2File_AnalysisRun+'/'+Hist1File_LevelRun+'-'+Hist2File_LevelRun+'Level/'+Hist1Name+Hist1Var+'_'+Hist1File_Prefix+'Over'+Hist2File_Prefix+'.png')
        else:
            HistCan.SaveAs(MediaDir+Comparison+Hist1File_Prefix+Hist2File_Prefix+'/Loop'+Hist1File_LoopRun+'-'+Hist2File_LoopRun+'/Event'+Hist1File_EventRun+'-'+Hist2File_EventRun+'/Analysis'+Hist1File_AnalysisRun+'-'+Hist2File_AnalysisRun+'/'+Hist1File_LevelRun+'-'+Hist2File_LevelRun+'Level/'+Hist1Name+Hist2Name+Hist1Var+'_'+Hist1File_Prefix+'Over'+Hist2File_Prefix+'.png')
