from ROOT import gSystem, TFile, TChain
import sys

# Initialising runs
NRuns = 5
RootDir = ''
outfileprefix = ''
Selection = ''

for arg in sys.argv:
    # Should filter the python script
    if arg.split('.')[-1] == 'py':
        continue 

    # Dir arguements in the form "DIR=RUNDIR-MEDIADIR"
    elif arg.split('=')[0].upper() == 'NRUNS':
        NRuns = int(arg.split('=')[1])

    # Dir arguements in the form "DIR=RUNDIR-MEDIADIR"
    elif arg.split('=')[0].upper() == 'ROOTDIR':
        RootDir = arg.split('=')[1]

    elif arg.split('=')[0].upper() == 'PREFIX':
        outfileprefix = arg.split('=')[1]

    # Looks for arguements passing the runs to compare
    elif arg.split('=')[0].upper() == 'SELECTION':
        Selection = ''.join(arg.split('=')[1:])

RunDirs = []
for run in range(NRuns):
    runstr = 'run_'+'{:02d}'.format(run+1)+'/'
    RunDirs.append(runstr)
RunTrees = [x+'tag_1_delphes_events.root' for x in RunDirs]

# Looping through the cross section of all runs and taking an average
XsecList = []
for run in RunDirs:
    with open(run+'tag_1_pythia.log', 'r') as file:
        lines = file.read().splitlines()
        # Xsec is the last element of the last line
        XsecList.append( float(lines[-1].split()[-1]) )
Xsec = sum(XsecList)/len(XsecList)

# Will recursively try to create each dir in RootDir path
if RootDir:
    for i in range(len(RootDir.split('/'))):
        gSystem.Exec('mkdir '+'/'.join(RootDir.split('/')[:i+1]))

chain = TChain('Delphes')
for tree in RunTrees:
    chain.Add(tree)

outfilename = RootDir+outfileprefix+'Pruned.root'
outfile = TFile(outfilename,'RECREATE')
PrunedTree = chain.CopyTree(Selection)

outfile.Write()
outfile.Close()


print('Mean xsec =', Xsec)
print('NEvents =', chain.GetEntries())
