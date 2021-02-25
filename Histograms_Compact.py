import Analysis_Funcs as funcs

myTree = Analysis_Funcs.LoadROOT("tag_1_delphes_events.root")

from ROOT import TFile, TH1F

outfile=TFile("GenParticles.root","RECREATE")

Nbins = 200


CountMin = 0
CountMax = 5

# Name = TH1F(Name, Title, NBins, xmin, xmax)

# Number of outgoing electrons (not including beam electrons)
Electron_Count = funcs.Histograms('Electron', HistVariables=['Count'], HistLimits=[(0, 10)])

# Number of outgoing muons (not including boson decay muons)
Muon_Count = funcs.Histograms('Muon', HistVariables=['Count'], HistLimits=[(0, 10)])

# Number of outgoing jets
Jet_Count = funcs.Histograms('Jet', HistVariables=['Count'], HistLimits=[(0, 10)])

FinalElectron = funcs.Histogram('FinalElectron')
LeadingMuon = funcs.Histogram('LeadingMuon')
SubLeadingMuon = funcs.Histogram('SubLeadingMuon')

WPlusMuon = funcs.Histogram('WPlusMuon')
WMinusMuon = funcs.Histogram('WMinusMuon')

LeadingJet = funcs.Histogram('LeadingJet')
SubLeadingJet = funcs.Histogram('SubLeadingJet')

ComparisonVars = ['dEta', 'dPhi', 'dRapidity', 'dR_Eta', 'dR_Rap']
ComparisonLims = [(-20, 20), (-3.5, 3.5), (-20, 20), (0, 10), (0, 10)]
MuonMuon = funcs.Histograms('Muon', HistVariables=ComparisonVars.append('InvMass'), HistLimits=ComparisonLims.append((0, 200)))
ElectronLeadingMuon = funcs.Histograms('ElectronLeadingMuon', HistVariables=ComparisonVars, HistLimits=ComparisonLims)
ElectronSubLeadingMuon = funcs.Histograms('ElectronSubLeadingMuon', HistVariables=ComparisonVars, HistLimits=ComparisonLims)
