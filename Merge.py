from ROOT import gSystem, TFile, TChain, TObject
import sys

# Initialising runs
NRuns = 1
RootDir = ''
outfilename = ''
Selection = ''

# Parsing arguments
for arg in sys.argv:
    # Should filter the python script
    if arg.split('.')[-1] == 'py':
        continue 

    # Number of run folders to merge
    # Recognised as "nruns=N"
    elif arg.split('=')[0].upper() == 'NRUNS':
        NRuns = int(arg.split('=')[1])

    # Root directory containing the run folders
    # Recognised as "rootdir=DIR"
    elif arg.split('=')[0].upper() == 'ROOTDIR':
        RootDir = arg.split('=')[1]

    # The name of the output merged file
    # Recognised as "outfile=FILENAME"
    elif arg.split('=')[0].upper() == 'OUTFILE':
        outfilename = arg.split('=')[1]

    # The selection string to pass to TTree.CopyTree("") function
    # Will act on the whole data set 
    # Recognised as "selection=SELECTION"

    # Using "=" as a delimiter should not effect the returned selection string 
    # since [1:] is used
    elif arg.split('=')[0].upper() == 'SELECTION':
        Selection = ''.join(arg.split('=')[1:])

# Makes a string for the filename of each run
# The runs are indexed as "run_N/tag_1_delphes_events.root" where 
# N is represented using 2 or more digits 

for run in range(NRuns):
    runstr = 'run_'+'{:02d}'.format(run+1)+'/'
    RunDirs.append(runstr)
RunTrees = [x+'tag_1_delphes_events.root' for x in RunDirs]

# Looping through the cross section of all runs and taking an average
# The cross section used for each run is taken from the end of the 
# pythia log file

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

NEvents = []
# Groups trees into 5 runs to manage memory use 
n = 5
GroupedTrees = [RunTrees[x:x+n] for x in range(0,len(RunTrees),n)]
GroupNEvents = []
# Make a directory for the grouped outfiles in the RootDir
gSystem.Exec('mkdir '+RootDir+'Groups/')

for i in range(len(GroupedTrees)):
    GroupChain = TChain('Delphes')

    # Make a chain made up of each tree in the group
    for tree in GroupedTrees[i]:
        GroupChain.Add(tree)

    # Make new file for each group
    GroupOutfile = TFile(RootDir+'Groups/'+str(i)+'.root','RECREATE')
    # Add the number of events of the pruned group to the list
    NEvents.append(GroupChain.GetEntries())

    # Prune the chain using the selection
    GroupPrunedTree = GroupChain.CopyTree(Selection)

    # Write and reset
    GroupOutfile.Write()
    GroupOutfile.Close()
    GroupChain.Reset()
    print('Group ', i)


# Load groups to one chain and save as one .root file
outfilename = RootDir+outfilename
MergedChain = TChain('Delphes')
for i in range(len(GroupedTrees)):
    print(RootDir+'Groups/'+str(i)+'.root')
    MergedChain.Add(RootDir+'Groups/'+str(i)+'.root')

outfile = TFile(RootDir+outfilename+'.root','RECREATE')

# I think (I've forgotten since I wrote it) that this line is to load the correct chain to memory (I hate memory management in PyROOT)
PrunedTree = MergedChain.CopyTree('') 


outfile.Write()
outfile.Close()
MergedChain.Reset()

# Sum the list to find total Nevents after pruning
NEvents_Total = sum(NEvents)

# Output average xsec and total Nevents
print('Mean xsec =', Xsec)
print('NEvents =', NEvents_Total)
