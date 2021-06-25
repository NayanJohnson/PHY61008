
from ROOT import TMath, TLorentzVector

import config, requests, itertools
import Loop_Funcs as LoopFuncs
import Hist_Funcs as HistFuncs

'''
Definitions of used objects:

ParticleDict[name] = {
    'Check'     :   check,
    'Name'      :   name,
    'Charge'    :   Charge,
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
def AddParticle(name, ParticleDict, P4=False, Charge=None):
        '''
        Adds particles to the ParticleDict
        '''

        # If no P4 is given (particle is not detected):
        if not P4:
            ParticleDict[name] = {
                'Check'     :   False
            }

        else:
            ParticleDict[name] = {
                'Check'     :   True,
                'Name'      :   name,
                'Charge'    :   Charge,
                'P4'        :   P4,
                'E'         :   P4.E(),
                'Eta'       :   P4.Eta(),
                'Phi'       :   P4.Phi(),
                'Rapidity'  :   P4.Rapidity(),
                'Theta'     :   P4.Theta(),
                'Pt'        :   P4.Pt(),
                'Et'        :   P4.Et(),
                'Mt'        :   P4.Mt(),
            }
        
        return ParticleDict


def RequestParticles(HistDict, ParticleDict):
    '''
    Adds requested particles to the HistDict.
    '''

    # Itterating through histogram categories
    for category, attributes in HistDict.items():
        
        if attributes['Dimensions'] == 1:
            # Itterating through particle requests
            for ParticleList_Index in range(len(attributes['Requests']['Particles'])):
                attributes['Particles'].append([])
                for particle in attributes['Requests']['Particles'][ParticleList_Index]:
                    attributes['Particles'][ParticleList_Index].append(ParticleDict[particle])

        elif attributes['Dimensions'] == 2:

            # Itterating through particle requests
            for Comparison_Index in range(len(attributes['Requests']['Particles'])):
                attributes['Particles'].append([[], []])
                # For x and y particles
                for i in (0, 1):
                    ParticleSet = attributes['Requests']['Particles'][Comparison_Index][i]
                    for particle in ParticleSet:
                        attributes['Particles'][Comparison_Index][i].append(ParticleDict[particle])  

    return HistDict

def GetParticleVariable(ParticleDict, ParticleList, var):
    '''
    Returns the value or list of variables for the given category : var
    Category is only used for q calcs.
    '''

    # List of variables that are stored in all particles.
    ParticleProperties = ['Charge', 'E', 'Eta', 'Phi', 'Rapidity', 'Theta', 'E', 'Pt', 'Et']
    SummedProperties = ['M', 'Mt', 'Eta_Sum', 'Phi_Sum', 'Rapidity_Sum', 'Pt_Sum', 'Et_Sum', 'E_Sum']


    # If all particles are present
    if all(particle['Check'] for particle in ParticleList):

        # Variables in ParticleProperties only require one particle and are stored in the particle entry
        # For these variables the hist is filled for each particle in the requests list
        if var in ParticleProperties:
            # Only alow 1D hists to return a list
            ParticleVars = []
            for i in range(0, len(ParticleList)):
                ParticleVars.append(ParticleList[i][var])
            return ParticleVars

        # Momentum transfer calculation using the beam electron and the passed particle
        elif var == 'qLepton':
            BeamParticle = ParticleDict['BeamElectron']
            if BeamParticle['Check']:
                q = (BeamParticle['P4'] - ParticleList[0]['P4']).Mag()
                return abs(q)
        
        # Momentum transfer calculation using the beam quark and the passed particle
        elif var == 'qQuark':
            BeamParticle = ParticleDict['BeamQuark']
            if BeamParticle['Check']:
                q = (BeamParticle['P4'] - ParticleList[0]['P4']).Mag()
                return abs(q)

        # Momentum transfer calculation using the beam electron and the passed particle, 
        # but uses the angles and energy rather than the P4
        elif var == 'qeMethod':
            BeamParticle = ParticleDict['BeamElectron']
            if BeamParticle['Check']:
                q = TMath.Sqrt(2*BeamParticle['E']*ParticleList[0]['E']*(1 - TMath.Cos(BeamParticle['Theta'])))
                return abs(q)

        # Variables in SummedProperties are calculated from the sum
        # of all particles in the request list
        elif var in SummedProperties:

            # Summing the P4 of the particles
            ParticleSum = TLorentzVector()
            for particle in ParticleList:
                ParticleSum = particle['P4'] + ParticleSum
            if var == 'M':
                return ParticleSum.M()
            elif var == 'Mt':
                return ParticleSum.Mt()
            elif var == 'Eta_Sum':
                return ParticleSum.Eta()
            elif var == 'Phi_Sum':
                return ParticleSum.Phi()
            elif var == 'Rapidity_Sum':
                return ParticleSum.Rapidity()
            elif var == 'Pt_Sum':
                return ParticleSum.Pt()
            elif var == 'Et_Sum':
                return ParticleSum.Et()
            elif var == 'E_Sum':
                return ParticleSum.E()

        # Varibles with a 'd' are the difference between two particles
        # These variables only use the first two particles in the request list
        elif var == 'dEta':
            dEta = ParticleList[0]['Eta'] - ParticleList[1]['Eta']
            return dEta
        
        elif var == 'dPhi':
            dPhi = ParticleList[0]['P4'].DeltaPhi(ParticleList[1]['P4'])
            return dPhi

        elif var == 'dRapidity':
            dRap = ParticleList[0]['Rapidity'] - ParticleList[1]['Rapidity']
            return dRap

        # Seperation of the two particles, calculated using Eta
        elif var == 'dR_Eta':
            dR_Eta = ParticleList[0]['P4'].DrEtaPhi(ParticleList[1]['P4'])
            return dR_Eta

        # Seperation of the two particles, calculated using Rapidity
        elif var == 'dR_Rap':
            dPhi = ParticleList[0]['P4'].DeltaPhi(ParticleList[1]['P4'])
            dRap = ParticleList[0]['Rapidity'] - ParticleList[1]['Rapidity']
            # DrRapidityPhi function doesnt seem to work
            dR_Rap = TMath.Sqrt( dPhi**2 + dRap**2 )
            return dR_Rap    

    return False


def InvMassCheck(Decay, Boson, ParticleDict, EventDict, EventCuts):
    '''
    Given a particular boson decay and the ParticleDict, will
    return the pair of particles that have an invariant mass
    closest to the boson rest mass. 
    Only the leading N particles are compared.
    (N is the number of expected particles defined in EventCuts[Decay])
    '''

    if EventDict['Count'][Decay] < EventCuts[Decay]:
        return ParticleDict, EventDict, True

    BosonMass = config.EventLoopParams[Boson]['Mass']

    # Getting the leading N sorted particles from EventDict
    # List will be a list of tuples (Pt, particle)
    particlesList = []
    for i in range(EventCuts[Decay]):
        particlesList.append(EventDict['PTSorted'][Decay][-1-i])

    # Possible pairs of particles
    Permutations = list( itertools.combinations(particlesList, 2))

    InvMassList = []
    # Calculating M of different possible pairs
    for ParticlePair in Permutations:
        InvMassList.append( (ParticlePair[0][1].P4()+ParticlePair[1][1].P4()).Mag() )

    # Find the closest M to BosonMass
    PairInvMass = min(InvMassList, key=lambda x:abs(x-BosonMass))
    PairIndex = InvMassList.index(PairInvMass)

    # Tagging the leading and subleading particle in the pair
    if Permutations[PairIndex][0][0] < Permutations[PairIndex][1][0]:
        ParticleDict = AddParticle(Boson+'Leading'+Decay[0:-1], ParticleDict, Permutations[PairIndex][1][1].P4())
        ParticleDict = AddParticle(Boson+'SubLeading'+Decay[0:-1], ParticleDict, Permutations[PairIndex][0][1].P4())

    else:        
        ParticleDict = AddParticle(Boson+'Leading'+Decay[0:-1], ParticleDict, Permutations[PairIndex][0][1].P4())
        ParticleDict = AddParticle(Boson+'SubLeading'+Decay[0:-1], ParticleDict, Permutations[PairIndex][1][1].P4())

    # Removing boson particles from PTSorted list
    EventDict['PTSorted'][Type].remove(Permutations[PairIndex][0])
    EventDict['PTSorted'][Type].remove(Permutations[PairIndex][1])

    return ParticleDict, EventDict

