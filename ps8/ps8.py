# 6.00 Problem Set 8
#
# Name:
# Collaborators:
# Time:



import numpy
import random
import pylab
from ps7 import *

#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):

    """
    Representation of a virus which can have drug resistance.
    """      

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        """

        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        

        """
        # TODO
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb

    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.    

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        # TODO
        return self.resistances[drug]

    def isResistantToAll(self, drugs):
        """
        Get the state of this virus particle's resistance to all drugs in the list.     

        drugs: The list of drugs (list of strings)
        returns: True if this virus instance is resistant to all the the drugs in the list, False
        otherwise.
        """
        for drug in drugs:
            if not self.isResistantTo(drug):
                return False
        return True

    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        # TODO
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                raise NoChildException()
        
        child_resistances = {}
        prob = random.random()
        if prob <= self.maxBirthProb * (1 - popDensity):

            for drug in self.resistances.keys():
                resistanceProb = random.random()
                if resistanceProb < self.mutProb:
                    child_resistances[drug] = not self.resistances[drug]
                else:
                    child_resistances[drug] = self.resistances[drug]
                    
            child = ResistantVirus(self.maxBirthProb, self.clearProb, child_resistances,
                                   self.mutProb)
            return child
        else:
            raise NoChildException()

class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        # TODO
        SimplePatient.__init__(self, viruses, maxPop)
        self.drugs_taken = []

    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        # TODO
        # should not allow one drug being added to the list multiple times
        if newDrug not in self.drugs_taken:
            self.drugs_taken.append(newDrug)

    def getPrescriptions(self):

        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """

        # TODO
        return self.drugs_taken
        

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        # TODO
        resist_pop = 0
        for virus in self.viruses:
            if virus.isResistantToAll(drugResist):
                resist_pop += 1
        return resist_pop				

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        # TODO
        surviving_particles = []
        for particle in  self.viruses:
            if not particle.doesClear():
                surviving_particles.append(particle)
        
        current_density = float(len(surviving_particles)) / self.maxPop
        
        reproduction = []
        for particle in surviving_particles:
            try:
                child = particle.reproduce(current_density, self.drugs_taken)
                reproduction.append(child)
            except NoChildException:
               pass
		
        self.viruses = surviving_particles[:]
        if reproduction:
            self.viruses.extend(reproduction)

        return self.getTotalPop()

		
#
# PROBLEM 2
#

def simulationWithDrug(numViruses = 100, maxBirthProb = 0.1, clearProb = 0.05, 
                        resistances = {'guttagonol':False}, mutProb = 0.005,
                        maxPop = 1000, numStepsBeforeDrugApplied = 150, numTotalSteps = 300):

    """
    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """
    # TODO
    virus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
    viruses = []
    for _ in range(numViruses):
        viruses.append(virus)

    infected = Patient(viruses, maxPop)
    num_all_viruses = []
    num_resist_viruses = []

    for i in range(numTotalSteps):
        if i == numStepsBeforeDrugApplied:
            infected.addPrescription('guttagonol')
        size = infected.update()
        num_all_viruses.append(size)
        num_resist_viruses.append(infected.getResistPop(['guttagonol']))
    
    return (num_all_viruses, num_resist_viruses)
	
def run_n_SimulationWithDrug(n):

    """
	Run simulationWithoutDrug n-times and produce a single plot
    that is representative of the average case
    """
    num_all_viruses_container = []
    num_resist_viruses_container = []
	
    for _ in range(n):
        num_all_viruses, num_resist_viruses = simulationWithDrug()
        num_all_viruses_container.append(num_all_viruses)
        num_resist_viruses_container.append(num_resist_viruses)
		
	# using numpy arrays to calculate mean of the n-simulations
    avg_all_vir = numpy.mean(num_all_viruses_container, axis = 0)
    avg_res_vir = numpy.mean(num_resist_viruses_container, axis = 0)

    time_step = range(len(avg_all_vir))
    pylab.figure()
    pylab.plot(time_step, avg_all_vir, label = 'Total')
    pylab.plot(time_step,avg_res_vir, label = 'Resistant virus')
    pylab.title('Resistant virus simulation')
    pylab.xlabel('Time / Steps')
    pylab.ylabel('Virus population')
    pylab.legend(loc = 'best')
    pylab.show()

# run_n_SimulationWithDrug(30)

#
# PROBLEM 3
#        

def simulationDelayedTreatment(numTrials, numTSteps = 300):

    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """

    # TODO
    delays = [0, 75, 150, 300]
    final_results = {}
	
    for delay in delays:
        final_virus_count = []
        for _ in range(numTrials):
            num_all_viruses, num_resist_viruses = simulationWithDrug(numStepsBeforeDrugApplied = delay, numTotalSteps = numTSteps)
            final_virus_count.append(num_all_viruses[-1])
        
        final_results[delay] = final_virus_count
	
    plotNum = 1
    for delay in delays:
        pylab.subplot(2, 2, plotNum)
        pylab.title("delay: " + str(delay))
        pylab.xlabel("final virus counts")
        pylab.ylabel("# trials")
        pylab.hist(final_results[delay], bins=12, range=(0, 600))
        plotNum += 1

    pylab.show()    

# simulationDelayedTreatment(300)

#
# PROBLEM 4
#
def simTwoDrugsTreatment(numViruses = 100, maxBirthProb = 0.1, clearProb = 0.05, 
                        resistances = {'guttagonol':False, 'grimpex':False}, mutProb = 0.005,
                        maxPop = 1000, numStepsBeforeDrugApplied = 150, secondDrugDelay = 150,
                        numTotalSteps = 600, drugs = ['guttagonol', 'grimpex'], ver = 1):
    """
	Simulate treatment with two drugs applied
	ver = 1: returns tuple with lists of population of all viruses and those resistant to all drugs
	ver = 2: returns tuple with lists of population of all viruses, those resistant to all drugs,
	and those resistant to particular drug
	"""
    virus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
    viruses = []
    for _ in range(numViruses):
        viruses.append(virus)

    infected = Patient(viruses, maxPop)
    num_all_viruses = []
    num_resist_viruses = []
    num_resist_drug_one = []
    num_resist_drug_two = []

    for i in range(numTotalSteps):
        if i == numStepsBeforeDrugApplied:
            infected.addPrescription(drugs[0])
        if i == numStepsBeforeDrugApplied + secondDrugDelay:
            infected.addPrescription(drugs[1])
        size = infected.update()
        num_all_viruses.append(size)
        num_resist_viruses.append(infected.getResistPop(drugs))
        num_resist_drug_one.append(infected.getResistPop([drugs[0]]))
        num_resist_drug_two.append(infected.getResistPop([drugs[1]]))
		
    if ver == 1:
        return (num_all_viruses, num_resist_viruses)
    elif ver == 2:
        return (num_all_viruses, num_resist_viruses, num_resist_drug_one, num_resist_drug_two)

def run_n_SimulationWithTwoDrugs(n, firstDrugApp = 150, secondDrugApp = 300):

    """
	Run simulationWithoutDrug n-times and produce a single plot
    that is representative of the average case
    """
    num_all_viruses_container = []
    num_resist_viruses_container = []
	
    for _ in range(n):
        num_all_viruses, num_resist_viruses = simTwoDrugsTreatment(numStepsBeforeDrugApplied = firstDrugApp,
		                                                           secondDrugDelay = secondDrugApp)
        num_all_viruses_container.append(num_all_viruses)
        num_resist_viruses_container.append(num_resist_viruses)
		
	# using numpy arrays to calculate mean of the n-simulations at each time step
    avg_all_vir = numpy.mean(num_all_viruses_container, axis = 0)
    avg_res_vir = numpy.mean(num_resist_viruses_container, axis = 0)

    time_step = range(len(avg_all_vir))
    pylab.figure()
    pylab.plot(time_step, avg_all_vir, label = 'Total')
    pylab.plot(time_step,avg_res_vir, label = 'Resistant virus')
    pylab.title('Resistant virus simulation \n' + 'first drug applied after ' + str(firstDrugApp) + ' time/steps \n'
	            'second drug applied after ' + str(firstDrugApp + secondDrugApp) + ' time/steps')
    pylab.xlabel('Time / Steps')
    pylab.ylabel('Virus population')
    pylab.legend(loc = 'best')
    pylab.show()

# run_n_SimulationWithTwoDrugs(30)


def simulationTwoDrugsDelayedTreatment():

    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """

    # TODO
    # simTwoDrugsTreatment(), run_n_SimulationWithTwoDrugs()

#
# PROBLEM 5
#    

def simulationTwoDrugsVirusPopulations(n = 10, firstDrugApp = 150, secondDrugApp = 100, v = 2):

    """

    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        

    """
    #TODO
    num_all_viruses_container = []
    num_resist_viruses_container = []
    num_resist_drug_one_container = []
    num_resist_drug_two_container = []
	
    for _ in range(n):
        sim = simTwoDrugsTreatment(numStepsBeforeDrugApplied = firstDrugApp,
		                           secondDrugDelay = secondDrugApp, ver = v)
        num_all_viruses, num_resist_viruses, num_resist_drug_one, num_resist_drug_two = sim
        num_all_viruses_container.append(num_all_viruses)
        num_resist_viruses_container.append(num_resist_viruses)
        num_resist_drug_one_container.append(num_resist_drug_one)
        num_resist_drug_two_container.append(num_resist_drug_two)
		
	# using numpy arrays to calculate mean of the n-simulations at each time step
    avg_all_vir = numpy.mean(num_all_viruses_container, axis = 0)
    avg_res_vir = numpy.mean(num_resist_viruses_container, axis = 0)
    avg_res_drug_one = numpy.mean(num_resist_drug_one_container, axis = 0)
    avg_res_drug_two = numpy.mean(num_resist_drug_two_container, axis = 0)
	
    return (avg_all_vir, avg_res_vir, avg_res_drug_one, avg_res_drug_two)

# print simulationTwoDrugsVirusPopulations(2)
	
def makePlotTwoDrugsVirPop():
    """
	Creates the plots of virus particles population in realation to its resistance to drugs
	simulations.keys() - number of simulation runs
	simulations.values() - time after which drugs were applied (time_of_drug1, delay_of_drug2)
	"""

    simulations = {1:(150, 300), 2:(150, 0)}
    sim_outcome = {}
	
    for i in simulations.keys():
        sim_outcome[i] = simulationTwoDrugsVirusPopulations(firstDrugApp = simulations[i][0], secondDrugApp = simulations[i][1])
	
    plotNum = 1
    for i in simulations.keys():
        avg_all_vir = sim_outcome[i][0]
        avg_res_vir = sim_outcome[i][1]
        avg_res_drug_one = sim_outcome[i][2]
        avg_res_drug_two = sim_outcome[i][3]
        time_step = range(len(avg_all_vir))
		
        pylab.subplot(2, 1, plotNum)
        pylab.title('First drug applied after: ' + str(simulations[i][0]) + '\n'
                     'Second drug applied after: ' + str(simulations[i][0]+simulations[i][1]))
        pylab.plot(time_step, avg_all_vir, label = 'Total')
        pylab.plot(time_step, avg_res_vir, label = 'Resistant virus to all drugs')
        pylab.plot(time_step, avg_res_drug_one, label = 'Resistant virus to drug one')
        pylab.plot(time_step, avg_res_drug_two, label = 'Resistant virus to drug two')			 
        pylab.xlabel("Time / Steps")
        pylab.ylabel("Virus popultion")
        pylab.legend(loc = 'best')
        pylab.plot()
        plotNum += 1

    pylab.show()
	
# makePlotTwoDrugsVirPop()
