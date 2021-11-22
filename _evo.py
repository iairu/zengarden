from _garden import Garden
from _monk import Monk
class Evolution:
    def __init__(self, garden: Garden, 
                populationCount: int, fitnessStepOverRotWeight: int = 2, 
                mutationChance: float = 0, crossPosition: int = 0, idealisticGenes: bool = True,
                elitism: float = 1,
                gardenStepPrint = False, detailStepPrint = False, solutionPrint = False, elitismFitnessRecalcPrint = False) -> None:
        
        # used for every generation incl. first
        self.populationCount = populationCount
        self.fitnessWeight = fitnessStepOverRotWeight
        self.mutationChance = mutationChance
        self.idealisticGenes = idealisticGenes
        self.elitism = elitism

        # used for every generation excl. first (pairing)
        self.crossPosition = crossPosition

        # print options
        self.gardenStepPrint = gardenStepPrint
        self.detailStepPrint = detailStepPrint
        self.solutionPrint = solutionPrint
        self.elitismFitnessRecalcPrint = elitismFitnessRecalcPrint

        # generate first generation with random genes
        self.population = []
        maxFitnessInPop = 0
        if (elitismFitnessRecalcPrint): eflog = "EFR Before:"
        for i in range(populationCount):
            monk = Monk([garden.a, garden.b], mutationChance, crossPosition, idealisticGenes)
            monk.explore(garden, fitnessStepOverRotWeight, gardenStepPrint, detailStepPrint, solutionPrint)
            if (elitismFitnessRecalcPrint): eflog += str(monk.fitness) + " "

            if (monk.fitness > maxFitnessInPop):
                maxFitnessInPop = monk.fitness
            self.population.append(monk)

        # apply elitism value , sort the generated population
        if (elitismFitnessRecalcPrint): eflog += "\nEFR After:"
        for i in range(populationCount):
            monk = self.population[i]
            if isinstance(monk, Monk):
                monk.fitness = monk.fitness % int((maxFitnessInPop + 1) * elitism) # (low elitism => more mixed fitness values => more random sort)
            if (elitismFitnessRecalcPrint): eflog += str(monk.fitness) + " "
        if (elitismFitnessRecalcPrint):
            print(eflog)

        self.population.sort()
        for monk in self.population:
            print(monk.fitness)

        return
    
    # ---------------------------

    def tabuSearch():
        pass