from ROOT import TFile, TLorentzVector

import config, requests
import Particle_Funcs as ParticleFuncs
import Loop_Funcs as LoopFuncs


def EventLoop(TreeDict, Xsec, RootDir, outfileprefix, LevelRun, LoopRun, EventRun, AnalysisRun):
    '''
    '''

    outfilename = RootDir+'Loop'+LoopRun+'/Event'+EventRun+'/Analysis'+AnalysisRun+'/'+outfileprefix+LevelRun+'Level_Pruned.root'

    # Open output
    outfile = TFile(outfilename,'RECREATE')
    PrunedTree = TreeDict['Tree'].CloneTree(0)

    EventCuts = config.EventLoopParams['Level']['Event'][EventRun]
    AnalysisCuts = config.EventLoopParams['Level']['Analysis'][AnalysisRun] 

    Zdecays = config.EventLoopParams['Z']['Decays']
    WPlusdecays = config.EventLoopParams['WPlus']['Decays']
    WMinusdecays = config.EventLoopParams['WMinus']['Decays']

    HistDict = requests.HistDict

    EventCutNum = 0
    # Looping through events
    for EventNum in range(TreeDict['NEvents']):

        HistDict, ParticleDict, EventDict = LoopFuncs.GetParticles(TreeDict, LevelRun, LoopRun, HistDict, EventNum)
        
        # MissingET cuts
        if EventDict['MissingET'].Et() < AnalysisCuts['MissingET']['Et'][0] or AnalysisCuts['MissingET']['Et'][1] < EventDict['MissingET'].Et():
            continue

        # Event cuts
        if EventDict['Count']['Electrons'] < EventCuts['Electrons'] or EventDict['Count']['Muons'] < EventCuts['Muons'] or EventDict['Count']['Jets'] < EventCuts['Jets']:
            continue

        # MuonSum
        MuonSum = TLorentzVector() 
        for Particle in EventDict['PTSorted']['Muons']:
            muon = Particle[1]
            MuonSum += muon.P4()
        ParticleDict = ParticleFuncs.AddParticle('MuonSum', ParticleDict, MuonSum)

        EventCutNum += 1
        for Zdecay in Zdecays:
            if Zdecay == None:
                continue
            elif Zdecays[0] == Zdecays[1]:
                continue
            else:
                ParticleDict, EventDict = ParticleFuncs.InvMassCheck(Zdecay, 'Z', ParticleDict, EventDict, EventCuts)

        for WPlusdecay in WPlusdecays:
            if WPlusdecay == None:
                continue
            elif WPlusdecays[0] == WPlusdecays[1]:
                continue            
            elif WPlusdecay == 'Jets':
                ParticleDict, EventDict = ParticleFuncs.InvMassCheck(WPlusdecay, 'WPlus', ParticleDict, EventDict, EventCuts)
            else:
                particlesList = [ParticleDict['Leading'+WPlusdecay[0:-1]], ParticleDict['SubLeading'+WPlusdecay[0:-1]]]
                for Lepton in particlesList:
                    if Lepton['Check']:
                        if Lepton['Charge'] == 1:
                            ParticleDict = ParticleFuncs.AddParticle('WPlus'+WPlusdecay[0:-1], ParticleDict, Lepton['P4'])

        for WMinusdecay in WMinusdecays:
            if WMinusdecay == None:
                continue
            elif WMinusdecays[0] == WMinusdecays[1]:
                continue            
            elif WMinusdecay == 'Jets':
                ParticleDict, EventDict = ParticleFuncs.InvMassCheck(WMinusdecay, 'WMinus', ParticleDict, EventDict, EventCuts)
            else:
                particlesList = [ParticleDict['Leading'+WMinusdecay[0:-1]], ParticleDict['SubLeading'+WMinusdecay[0:-1]]]
                for Lepton in particlesList:
                    if Lepton['Check']:
                        if Lepton['Charge'] == -1:
                            ParticleDict = ParticleFuncs.AddParticle('WMinus'+WMinusdecay[0:-1], ParticleDict, Lepton['P4'])

        # FinalBeamElectron selection and cuts completed after boson particles removed from PTSorted List
        FinalBeamElectron_Sorted = list(EventDict['PTSorted']['Electrons'])
        # FinalBeamElectron cuts 
        for particle in EventDict['PTSorted']['Electrons']:
            if particle[1].P4().Eta() < AnalysisCuts['FinalBeamElectron']['Eta'][0] or AnalysisCuts['FinalBeamElectron']['Eta'][1] < particle[1].P4().Eta():
                FinalBeamElectron_Sorted.remove(particle)                

        # FinalBeamElectron selection
        if len(FinalBeamElectron_Sorted) != 0:
            ParticleDict = ParticleFuncs.AddParticle('FinalBeamElectron', ParticleDict, FinalBeamElectron_Sorted[-1][1].P4())
        else:
            continue

        if len(EventDict['PTSorted']['Jets']) != 0:
            ParticleDict = ParticleFuncs.AddParticle('FinalBeamJet', ParticleDict, EventDict['PTSorted']['Jets'][-1][1].P4())

        # Adds particle for W+ - W- muons and W+ - Electron 
        if ParticleDict['WPlusMuon']['Check'] and ParticleDict['WMinusMuon']['Check']:
            DiMuon = ParticleDict['WPlusMuon']['P4'] + ParticleDict['WMinusMuon']['P4']
            WPlusMuonFinalBeamElectron = ParticleDict['WPlusMuon']['P4'] + ParticleDict['FinalBeamElectron']['P4']
            ParticleDict = ParticleFuncs.AddParticle('DiMuon', ParticleDict, DiMuon)
            ParticleDict = ParticleFuncs.AddParticle('WPlusMuonFinalBeamElectron', ParticleDict, WPlusMuonFinalBeamElectron)

        TreeDict['Tree'].GetEntry(EventNum)
        PrunedTree.Fill()
    
    # Writing and closing file
    outfile.Write()
    outfile.Close()
    print('here')
    # PrunedTree.Delete()