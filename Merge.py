from ROOT import gSystem, TFile, TChain, TObject
import sys

# Initialising runs
NRuns = 1
RootDir = ''
outfilename = ''
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

    elif arg.split('=')[0].upper() == 'OUTFILE':
        outfilename = arg.split('=')[1]

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


# Groups trees into 5 runs to manage memory use 
n = 5
GroupedTrees = [RunTrees[x:x+n] for x in range(0,len(RunTrees),n)]
GroupNEvents = []
for i in range(len(GroupedTrees)):
    GroupChain = TChain('Delphes')

    for tree in GroupedTrees[i]:
        GroupChain.Add(tree)

    # Make new file for each group
    GroupOutfile = TFile(RootDir+'Group'+str(i)+'.root','RECREATE')

    GroupPrunedTree = GroupChain.CopyTree(Selection)


    GroupOutfile.Write()
    GroupOutfile.Close()
    GroupChain.Reset()
    print('Group ', i)


# Load merged runs and save as one .root file
outfilename = RootDir+outfilename
MergedChain = TChain('Delphes')
for i in range(len(GroupedTrees)):
    print(RootDir+'Group'+str(i)+'.root')
    MergedChain.Add(RootDir+'Group'+str(i)+'.root')

# Make new file for each group
outfile = TFile(RootDir+outfilename+'.root','RECREATE')

PrunedTree = MergedChain.CopyTree('')

NEvents = MergedChain.GetEntries()

outfile.Write()
outfile.Close()
MergedChain.Reset()

print('Mean xsec =', Xsec)
print('NEvents =', NEvents)
