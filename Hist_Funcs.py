from ROOT import TH1F, TH2F, TPad, TCanvas, TLegend, TLine, SetOwnership, TColor, gStyle, gROOT, TRatioPlot
import config, requests
import Particle_Funcs as ParticleFuncs
import Loop_Funcs as LoopFuncs

'''
Definitions of used objects:

HistFiles = {
    1               :   {
        'Prefix'        :   HistFile1_Prefix,
        'LevelRun'      :   HistFile1_LevelRun,
        'LoopRun'       :   HistFile1_LoopRun,
        'EventRun'      :   HistFile1_EventRun,
        'AnalysisRun'   :   HistFile1_AnalysisRun,
        'Name'          :   HistFile1_Name,

        'File'          :   TFile(HistFile1_Name)
    },

    2   :   {
        'Prefix'        :   HistFile2_Prefix,
        'LevelRun'      :   HistFile2_LevelRun,
        'LoopRun'       :   HistFile2_LoopRun,
        'EventRun'      :   HistFile2_EventRun,
        'AnalysisRun'   :   HistFile2_AnalysisRun,
        'Name'          :   HistFile2_Name,

        'File'          :   TFile(HistFile2_Name)
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

# Setting some options for canvas drawing, they're probably not all necessary
gStyle.SetOptStat(0)
gStyle.SetTitleStyle(0)
gStyle.SetLegendBorderSize(0)
gStyle.SetOptTitle(0)
gROOT.ForceStyle()

def GetVarLabels(var):
    '''
    Given a variable, will output the corresponding axis label.
    '''
    VarLabel = ''
    if var == 'Count':
        VarLabel = 'Count per event'
    elif var == 'Eta':
        VarLabel = '#eta'
    elif var == 'Phi':
        VarLabel = '#phi [rad]'
    elif var == 'Rapidity':
        VarLabel = 'y'
    elif var == 'Pt':
        VarLabel = 'p_{T} [GeV]'
    elif var == 'Et':
        VarLabel = 'E_{T} [GeV]'
    elif var == 'E':
        VarLabel = 'E [GeV]'                    
    elif var == 'M':
        VarLabel = 'M [GeV]'                    
    elif var == 'Mt':
        VarLabel = 'M_{T} [GeV]'
    elif var == 'qLepton':
        VarLabel = 'q [GeV]'
    elif var == 'qeMethod':
        VarLabel = 'q [GeV]'
    elif var == 'dEta':
        VarLabel = '#Delta#eta'      
    elif var == 'dPhi':
        VarLabel = '#Delta#phi [rad]'
    elif var == 'dRapidity':
        VarLabel = '#Delta#text{y}' 
    elif var == 'dR_Eta':
        VarLabel = '#DeltaR'                 
    elif var == 'dR_Rap':
        VarLabel = '#DeltaR'     
    elif var == 'Eta_Sum':
        VarLabel = '#eta_{Sum}'
    elif var == 'Phi_Sum':
        VarLabel = '#phi_{Sum} [rad]'
    elif var == 'Rapidity_Sum':
        VarLabel = 'y_{Sum}'
    elif var == 'Pt_Sum':
        VarLabel = 'p_{T, Sum} [GeV]'
    elif var == 'Et_Sum':
        VarLabel = 'E_{T, Sum} [GeV]'
    elif var == 'E_Sum':
        VarLabel = 'E_{Sum} [GeV]'   
    return VarLabel

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
        # Initialising the dictionary to store the hists for each "name"
        attributes['Hists'] = {}
        
        # 1D Hists
        if attributes['Dimensions'] == 1:
            for var in attributes['Requests']['Vars']:
                VarLabel = GetVarLabels(var)
                histName = name+'_'+var
                histTitle = ''+';'+VarLabel+';Events'

                histXlow = VarParams[var]['Range'][0]
                histXup = VarParams[var]['Range'][1]
                histXrange = histXup-histXlow

                # Scales number of bins dependng on var range
                if histXrange <= 10:
                    histXNbins = int(NbinsDefault * 1/2 * LowRangeBinScale)
                elif histXrange <= 100:
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

                VarLabels = [GetVarLabels(pair[0]), GetVarLabels(pair[1])]
                if attributes['Requests']['Particles'][0][0] == attributes['Requests']['Particles'][0][1]:
                    histTitle = ''+';'+VarLabels[0]+';'+VarLabels[1]+';Frequency'
                else:
                    histTitle = ''+';'+attributes['Requests']['Particles'][0][0][0]+' '+VarLabels[0]+';'+attributes['Requests']['Particles'][0][1][0]+' '+VarLabels[1]+';Frequency'


                histXlow = VarParams[pair[0]]['Range'][0]
                histXup = VarParams[pair[0]]['Range'][1]
                histXrange = histXup-histXlow

                # Scales number of bins dependng on var range
                if histXrange <= 10:
                    histXNbins = int(NbinsDefault * 1/2 * LowRangeBinScale)
                elif histXrange <= 100:
                    histXNbins = int(NbinsDefault * LowRangeBinScale)
                else:
                    histXNbins = int(NbinsDefault * HighRangeBinScale)

                histYlow = VarParams[pair[1]]['Range'][0]
                histYup = VarParams[pair[1]]['Range'][1]        
                histYrange = histYup-histYlow

                # Scales number of bins dependng on var range
                if histYrange <= 10:
                    histYNbins = int(NbinsDefault * 1/2 * LowRangeBinScale)
                elif histYrange <= 100:
                    histYNbins = int(NbinsDefault * LowRangeBinScale)
                else:
                    histYNbins = int(NbinsDefault * HighRangeBinScale)                    

                hist = TH2F(histName, histTitle, histXNbins, histXlow, histXup, histYNbins, histYlow, histYup)

                hist.SetOption('HIST COLZ')

                hist.GetZaxis().SetTitleSize(0.04)
                hist.GetZaxis().SetLabelSize(0.03)
                hist.GetZaxis().SetTickLength(0.02)

                # Adds the hist to the dict
                HistDict[name]['Hists'][pair[0]+'_'+pair[1]]    =   hist

        hist.GetXaxis().SetTitleSize(0.04)
        hist.GetYaxis().SetTitleSize(0.04)

        hist.GetXaxis().SetTickLength(0.02)
        hist.GetYaxis().SetTickLength(0.02)

        hist.SetStats(False)
        
    return HistDict

def FillHists(HistDict, ParticleDict):
    '''
    Given a HistDict, will fill the histograms using ParticleDict.
    '''
    
    # List of variables that are stored in the particle's dict. 
    ParticleProperties = ['PID', 'E', 'Eta', 'Phi', 'Rapidity', 'Theta', 'Pt', 'Et']

    for category, attributes in HistDict.items():
        if attributes['Dimensions'] == 1:
            for xVar, hist in attributes['Hists'].items():

                # Count var can be read straight from attributes
                if xVar == 'Count': 
                    hist.Fill(attributes['Count'])

                else:
                    # Loop through all particles stored with the hist
                    # attributes['Particles'] = [[List1], [List2]...]
                    for xParticles in attributes['Particles']:

                        # Get the variable of the particles in question
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

                # attributes['Particles'] = [[(xParticles1), (yParticles1)], [(xParticles2), (yParticles2)], ...]
                for Comparison in attributes['Particles']:

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

def HistLims(hist, name, var, Scale=1, Norm=False, Change1D=True, Change2D=True, Diff2D=True):
    '''
    Rescales hist lims.
    Norm : Whether to normalise the histograms
    ChangeND : Whether to alter the ND histogram lims
    Diff2D : Whether the 2D axis are allowed different limits
    '''    
    XMin, XMax, YMin, YMax = False, False, False, False

    try:
        hist.Integral()
    except AttributeError:
        print(name, var)

    # Normalises the hist or not    
    if Norm and hist.Integral() != 0:
        hist.Scale(1./hist.Integral())
    else:
        hist.Scale(Scale)


    if hist.GetDimension() == 1:
        if Change1D:
            ThresholdMin = (hist.Integral()/200) * 1/25
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
            
            ThresholdMin = (hist.Integral()/200) * 1/100
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
            if not Diff2D:
                Max = max(XMax, YMax)
                Min = min(XMin, YMin)
                XMax, YMax, Xmin, YMin = Max, Max, Min, Min
            hist.SetAxisRange(XMin, XMax, 'X')
            hist.SetAxisRange(YMin, YMax, 'Y')

    return hist, [(XMin, XMax), (YMin, YMax)]

def CompareHist(HistProps, MediaDir, LimChange=True):
    '''
    Given a histogram dictionary and 2 histogram files (stored in HistFiles and HistProps),
    will output comparison histograms.
    '''
    
    # Whether to normalise the hists or not
    Norm = HistProps['Norm']
    if Norm:
        Comparison = 'Norm'
    else:
        Comparison = 'Rel'

    # Initialising hist vars from the dictionaries
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

    # Getting the limits of each hist
    Hist1, Lims1 = HistLims(Hist1, Hist1Name, Hist1Var, Norm=Norm)
    Hist2, Lims2 = HistLims(Hist2, Hist2Name, Hist2Var, Norm=Norm)

    # Setting the limits of both hists to be equal
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
        hist.SetStats(False)
        hist.SetMaximum(Max)

    # Initialise canvas
    HistCan = TCanvas()
    HistCan.cd()

    # Legend properties
    LegendX1 = .7
    LegendX_interval = 0.2
    LegendY1 = .875
    LegendY_interval = 0.075
    TextSize = .028

    Legend1 = TLegend(LegendX1, LegendY1 , LegendX1+LegendX_interval, LegendY1-LegendY_interval)
    # Stops legend overwriting canvas
    SetOwnership(Legend1,False)
    # Legend1.SetBorderSize(1)
    Legend1.SetShadowColor(2)

    # Entries
    Legend1.AddEntry(Hist1,'Entries: '+str(int(Hist1.GetEntries())), 'l')
    # Legend1.AddEntry(Hist1, 'Line Color', 'l')
    Legend1.SetTextSize(TextSize)
    Legend1.SetTextColor(1)
    # Seperation is small, but will be maximised to the bounds of the TLegend
    # box
    Legend1.SetEntrySeparation(.1)

    Legend2 = TLegend(LegendX1, LegendY1-LegendY_interval , LegendX1+LegendX_interval, LegendY1-2*LegendY_interval)
    # Stops legend overwriting canvas    
    SetOwnership(Legend2,False)
    # Legend2.SetBorderSize(1)
    Legend2.SetShadowColor(2)

    # Entries
    Legend2.AddEntry(Hist2,'Entries: '+str(int(Hist2.GetEntries())), 'l')
    # Legend2.AddEntry(Hist2, 'Line Color', 'l')
    Legend2.SetTextSize(TextSize)       
    # Seperation is small, but will be maximised to the bounds of the TLegend
    # box
    Legend2.SetEntrySeparation(.1)

    # The header of each legend
    if Hist1File_Prefix != Hist2File_Prefix:
        Legend1.SetHeader(Hist1File_Prefix)
        Legend2.SetHeader(Hist2File_Prefix)
    elif Hist1Name != Hist2Name:
        Legend1.SetHeader(Hist1Name)
        Legend2.SetHeader(Hist2Name)

    # Constructing titles and labels depending on the comparison
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
    # Prevents log outputs
    with LoopFuncs.Quiet():
        # Saves the canvas
        if Hist1Name == Hist2Name:
            HistCan.SaveAs(MediaDir+Comparison+Hist1File_Prefix+Hist2File_Prefix+'/Loop'+Hist1File_LoopRun+'-'+Hist2File_LoopRun+'/Event'+Hist1File_EventRun+'-'+Hist2File_EventRun+'/Analysis'+Hist1File_AnalysisRun+'-'+Hist2File_AnalysisRun+'/'+Hist1File_LevelRun+'-'+Hist2File_LevelRun+'Level/'+Hist1Name+Hist1Var+'.png')
        else:
            HistCan.SaveAs(MediaDir+Comparison+Hist1File_Prefix+Hist2File_Prefix+'/Loop'+Hist1File_LoopRun+'-'+Hist2File_LoopRun+'/Event'+Hist1File_EventRun+'-'+Hist2File_EventRun+'/Analysis'+Hist1File_AnalysisRun+'-'+Hist2File_AnalysisRun+'/'+Hist1File_LevelRun+'-'+Hist2File_LevelRun+'Level/'+Hist1Name+Hist2Name+Hist1Var+'.png')
        # Attempts to clean up memory
        HistCan.Delete()

def SigBack(HistProps, MediaDir, LimChange=True):
    '''
    Given a histogram dictionary and 2 histogram files (stored in HistFiles and HistProps),
    will output comparison signal/background histograms.
    '''
    # Whether to normalise the hists or not    
    Norm = HistProps['Norm']
    if Norm:
        Comparison = 'Norm'
    else:
        Comparison = 'Rel'

    # Initialising hist vars from the dictionaries
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

    # Getting the limits of each hist
    Hist1, Lims1 = HistLims(Hist1, Hist1Name, Hist1Var, Norm=Norm)
    Hist2, Lims2 = HistLims(Hist2, Hist2Name, Hist2Var, Norm=Norm)

    # Setting the limits of both hists to be equal
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

    Hist1.Rebin(3)
    Hist2.Rebin(3)

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

        hist.GetXaxis().SetLabelFont(63) #font in pixels
        hist.GetXaxis().SetLabelSize(16) #in pixels
        hist.GetYaxis().SetLabelFont(63) #font in pixels
        hist.GetYaxis().SetLabelSize(16) #in pixels

    c1 = TCanvas("c1","example")
    # pad1 = TPad("pad1","pad1",0,0.3,1,1)
    # pad1.SetBottomMargin(0)
    # pad1.Draw()
    # pad1.cd()
    Hist1.SetLineColor(4)        
    # Hist1.Draw('HIST same')
    Hist2.SetLineColor(2)
    # Hist2.Draw('HIST same')

    c1.cd()

    # This will generate an upper (comparison) and lower (ratio) plot
    rp = TRatioPlot( Hist1 , Hist2 ) 
    # c1.SetTicks( 0 , 1 )
    rp.SetH1DrawOpt('HIST')
    rp.SetH2DrawOpt('HIST')
    rp.GetLowYaxis().SetTickLength(0.02)
    rp.GetLowYaxis().SetNdivisions(5) 
    rp.GetXaxis().SetLimits(XMin, XMax)
    rp.Draw('noconfint nogrid') 
    rp.GetLowerRefYaxis().SetLabelFont(63)
    rp.GetLowerRefYaxis().SetLabelSize(16)
    rp.GetLowerRefYaxis().SetTitle('Signal/Background')
    gStyle.SetOptStat(0)
    gStyle.SetTitleStyle(0)
    gStyle.SetLegendBorderSize(0)
    gStyle.SetOptTitle(0)
    gROOT.ForceStyle()

    # Legend properties
    LegendX1 = .7
    LegendX_interval = 0.15
    LegendY1 = .875
    LegendY_interval = 0.075
    TextSize = .028

    Legend1 = TLegend(LegendX1, LegendY1 , LegendX1+LegendX_interval, LegendY1-LegendY_interval)
    # Stops legend overwriting canvas
    SetOwnership(Legend1,False)
    # Legend1.SetBorderSize(1)
    Legend1.SetShadowColor(2)

    # Entries
    Legend1.AddEntry(Hist1,'Entries: '+str(int(Hist1.GetEntries())), 'l')
    # Legend1.AddEntry(Hist1, 'Line Color', 'l')
    Legend1.SetTextSize(TextSize)
    Legend1.SetTextColor(1)
    # Seperation is small, but will be maximised to the bounds of the TLegend
    # box
    Legend1.SetEntrySeparation(.1)

    Legend2 = TLegend(LegendX1, LegendY1-LegendY_interval , LegendX1+LegendX_interval, LegendY1-2*LegendY_interval)
    # Stops legend overwriting canvas    
    SetOwnership(Legend2,False)
    # Legend2.SetBorderSize(1)
    Legend2.SetShadowColor(2)

    # Entries
    Legend2.AddEntry(Hist2,'Entries: '+str(int(Hist2.GetEntries())), 'l')
    # Legend2.AddEntry(Hist2, 'Line Color', 'l')
    Legend2.SetTextSize(TextSize)       
    # Seperation is small, but will be maximised to the bounds of the TLegend
    # box
    Legend2.SetEntrySeparation(.1)

    # The header of each legend
    if Hist1File_Prefix != Hist2File_Prefix:
        Legend1.SetHeader(Hist1File_Prefix)
        Legend2.SetHeader(Hist2File_Prefix)
    elif Hist1Name != Hist2Name:
        Legend1.SetHeader(Hist1Name)
        Legend2.SetHeader(Hist2Name)

    # Constructing titles and labels depending on the comparison
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

    Legend1.Draw('same')
    Legend2.Draw('same')
    c1.Update() 

    # Prevents log outputs
    with LoopFuncs.Quiet():
        # Saves the canvas        
        if Hist1Name == Hist2Name:
            c1.SaveAs(MediaDir+Comparison+Hist1File_Prefix+Hist2File_Prefix+'/Loop'+Hist1File_LoopRun+'-'+Hist2File_LoopRun+'/Event'+Hist1File_EventRun+'-'+Hist2File_EventRun+'/Analysis'+Hist1File_AnalysisRun+'-'+Hist2File_AnalysisRun+'/'+Hist1File_LevelRun+'-'+Hist2File_LevelRun+'Level/'+Hist1Name+Hist1Var+'_'+Hist1File_Prefix+'Over'+Hist2File_Prefix+'.png')
        else:
            c1.SaveAs(MediaDir+Comparison+Hist1File_Prefix+Hist2File_Prefix+'/Loop'+Hist1File_LoopRun+'-'+Hist2File_LoopRun+'/Event'+Hist1File_EventRun+'-'+Hist2File_EventRun+'/Analysis'+Hist1File_AnalysisRun+'-'+Hist2File_AnalysisRun+'/'+Hist1File_LevelRun+'-'+Hist2File_LevelRun+'Level/'+Hist1Name+Hist2Name+Hist1Var+'_'+Hist1File_Prefix+'Over'+Hist2File_Prefix+'.png')

