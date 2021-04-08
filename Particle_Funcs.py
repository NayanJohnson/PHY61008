
from ROOT import TMath, TLorentzVector

import config, requests, itertools
import Loop_Funcs as LoopFuncs
import Hist_Funcs as HistFuncs

"""
Definitions of used objects:

ParticleDict[name] = {
    'Check'     :   check,
    'Name'      :   name,
    'PID'       :   PID,
    'P4'        :   P4,
    'E'         :   P4.E(),
    'Eta'       :   P4.Eta(),
    'Phi'       :   P4.Phi(),
    'Rapidity'  :   P4.Rapidity(),
    'Theta'     :   P4.Theta(),
    'Pt'        :   P4.Pt(),
    'Et'        :   P4.Et()
}

"""

def RequestParticles(HistDict, ParticleDict):
    '''
        Adds requested particles to the HistDict.
        Histogram dictionary should be in the following format:
        HistDict =        {
            category        :   {
                Requests        :   {
                    Vars            :   [],
                    Particles       :   []
                },

                Vars        :   [],
                Particles   :   [],
                Hists       :   {
                    Var1        :   Hist1,
                    Var2        :   Hist2
                }
            }
        }
        
        Particle dictionary should be in the following format:
        ParticleDict[name] = {
            'Check'     :   check,
            'Name'      :   name,
            'PID'       :   PID,
            'P4'        :   P4,
            'E'         :   P4.E(),
            'Eta'       :   P4.Eta(),
            'Phi'       :   P4.Phi(),
            'Rapidity'  :   P4.Rapidity(),
            'Theta'     :   P4.Theta(),
            'Pt'        :   P4.Pt(),
            'Et'        :   P4.Et()
        }
    '''

    # Itterating through histogram categories
    for category, properties in HistDict.items():
        
        # Itterating through particle requests
        for particle in properties['Requests']['Particles']:

            # Particle check
            if ParticleDict[particle]['Check']:
                properties['Particles'].append(ParticleDict[particle])               

    return HistDict

def GetParticleVariable(var, ParticleList, category=None):
    '''
        Returns the value or list of variables for the given category : var
        Category is only used for q calcs.
    '''

    # List of variables that are stored in all particles.
    ParticleProperties = ['PID', 'E', 'Eta', 'Phi', 'Rapidity', 'Theta', 'Pt', 'Et']

    # Variables that can be calculated from one or multiple
    # particles.
    if len(ParticleList) != 0:

        # Variables in ParticleProperties only require one particle so
        # the hist can be filled by all particles in the list.
        if var in ParticleProperties:
            # Only alow 1D hists to return a list
            ParticleVars = []
            for i in range(0, len(ParticleList)):
                ParticleVars.append(ParticleList[i][var])
            return ParticleVars

        elif var == 'InvMass':
            ParticleSum = TLorentzVector()
            for particle in ParticleList:
                ParticleSum = particle['P4'] + ParticleSum
            return ParticleSum.M()

        elif var == 'q':
            if category == 'qLepton' or category == 'qQuark':
                q = (ParticleList[0]['P4'] - ParticleList[1]['P4']).Mag()
            elif category == 'qeMethod':
                q = TMath.Sqrt(2*ParticleList[0]['E']*ParticleList[1]['E']*(1 - TMath.Cos(ParticleList[0]['Theta'])))
            return abs(q)

        elif var == 'dEta':
            dEta = ParticleList[0]['Eta'] - ParticleList[1]['Eta']
            return dEta
        
        elif var == 'dPhi':
            dPhi = ParticleList[0]['P4'].DeltaPhi(ParticleList[1]['P4'])
            return dPhi

        elif var == 'dRapidity':
            dRap = ParticleList[0]['Rapidity'] - ParticleList[1]['Rapidity']
            return dRap

        elif var == 'dR_Eta':
            dR_Eta = ParticleList[0]['P4'].DrEtaPhi(ParticleList[1]['P4'])
            return dR_Eta

        elif var == 'dR_Rap':
            dPhi = ParticleList[0]['P4'].DeltaPhi(ParticleList[1]['P4'])
            dRap = ParticleList[0]['Rapidity'] - ParticleList[1]['Rapidity']
            # DrRapidityPhi function doesnt seem to work
            dR_Rap = TMath.Sqrt( dPhi**2 + dRap**2 )
            return dR_Rap    
    return False

def AddParticle(name, ParticleDict, P4=False, PID=None):
        '''
            Given a name, PID, 4-momenta of a particle,
            will add a particle dict of various properties to an existing
            dict.
        '''

        # Checks if a particle is present
        if P4:
            ParticleDict[name] = {
                'Check'     :   False
            }

        else:
            ParticleDict[name] = {
                'Check'     :   True,
                'Name'      :   name,
                'PID'       :   PID,
                'P4'        :   P4,
                'E'         :   P4.E(),
                'Eta'       :   P4.Eta(),
                'Phi'       :   P4.Phi(),
                'Rapidity'  :   P4.Rapidity(),
                'Theta'     :   P4.Theta(),
                'Pt'        :   P4.Pt(),
                'Et'        :   P4.Et(),
            }
        
        return ParticleDict

def InvMassCheck(particles, Boson, ParticleDict, EventDict):
    '''
    '''

    if particles == 'Electrons' and EventDict['Count']['Electrons'] <= 2:
        return ParticleDict, EventDict

    elif particles == 'Muons' and EventDict['Count']['Muons'] <= 1:
        return ParticleDict, EventDict

    elif particles == 'Jets' and EventDict['Count']['Jets'] <= 2:
        return ParticleDict, EventDict

    BosonMass = config.EventLoopParams[Boson]['Mass']

    # Setting up list of possible Boson decay products
    # When indexing ParticleDict remove the 's' from particle
    # Size of particlesList depends of number of expected particles
    # of that type

    # Getting the sorted particles from list
    # List will be a list of tuples (Pt, particle)
    particlesList = EventDict['PTSorted'][particles[0:-1]]
    # Possible pairs of Z decay products
    Permutations = list( itertools.combinations(particlesList, 2))

    InvMassList = []
    # Calculating InvMass of different possible pairs
    for ParticlePair in Permutations:
        InvMassList.append( (ParticlePair[0][1].P4()+ParticlePair[1][1].P4()).Mag() )

    # Find the closest InvMass to the BosonMass
    PairInvMass = min(InvMassList, key=lambda x:abs(x-BosonMass))
    PairIndex = InvMassList.index(PairInvMass)
    if Permutations[PairIndex][0][0] < Permutations[PairIndex][1][0]:
        ParticleDict = AddParticle(Boson+'Leading'+particles[0:-1], ParticleDict, Permutations[PairIndex][1][1].P4())
        ParticleDict = AddParticle(Boson+'SubLeading'+particles[0:-1], ParticleDict, Permutations[PairIndex][0][1].P4())

    else:        
        ParticleDict = AddParticle(Boson+'Leading'+particles[0:-1], ParticleDict, Permutations[PairIndex][0][1].P4())
        ParticleDict = AddParticle(Boson+'SubLeading'+particles[0:-1], ParticleDict, Permutations[PairIndex][1][1].P4())

    # Removing boson particles from list of particle
    particlesList.remove(Permutations[PairIndex][0])
    particlesList.remove(Permutations[PairIndex][1])
    EventDict['PTSorted'][particles[0:-1]] = particlesList

    return ParticleDict, EventDict

