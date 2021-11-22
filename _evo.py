from math import ceil, floor
from _garden import Garden
from _monk import Monk
class Evolution:
    def __init__(self, garden: Garden, 
                populationCount: int, fitnessStepOverRotWeight: int = 2, 
                mutationChance: float = 0, crossPosition: int = 0, idealisticGenes: bool = True,
                elitism: float = 1,
                gardenStepPrint = False, detailStepPrint = False, solutionPrint = False, elitismFitnessRecalcPrint = False) -> None:
        
        # used for every generation incl. first
        self.garden = garden
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
        self.generation = 1
        maxFitnessInPop = 0
        # also include a success detector just in case
        self.successCount = 0
        self.successAttribs = []
        if (elitismFitnessRecalcPrint): eflog = "EFR Before:"
        for i in range(populationCount):
            monk = Monk([garden.a, garden.b], mutationChance, crossPosition, idealisticGenes)
            success, exploredGarden = monk.explore(garden, fitnessStepOverRotWeight, gardenStepPrint, detailStepPrint, solutionPrint)
            if (success):
                self.successCount += 1
                self.successAttribs.append([self.generation, monk, exploredGarden, success])

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
        if (elitismFitnessRecalcPrint): print(eflog)

        self.population.sort()
        # for monk in self.population:
        #     print(monk.fitness)

        return

    def evolve(self):
        newPopulation = []
        self.generation += 1

        # Idea 1: Combine likely stronger (more likely with higher elitism) with likely average and likely weaker
        # No combinations between average and weaker or selves
        matcher = float(self.populationCount / 3)
        group1 = 0
        group2 = int(ceil(matcher))
        group3 = int(ceil(matcher * 2))
        for likelyStronger in range(group1, group2):
            parent1 = self.population[likelyStronger]

            for likelyAverage in range(group2, group3, int((group3 - group2) / 1.5)):
                parent2 = self.population[likelyAverage]
                newPopulation.append(Monk(parent1, parent2, self.mutationChance, self.crossPosition, self.idealisticGenes))

            for likelyWeaker in range(group3, self.populationCount, int((self.populationCount - group3) / 1.5)):
                parent3 = self.population[likelyWeaker]
                newPopulation.append(Monk(parent1, parent3, self.mutationChance, self.crossPosition, self.idealisticGenes))

        # the newer population is larger...
        oldlen = len(self.population)
        newlen = len(newPopulation)
        # print(oldlen)
        # print(newlen)

        # Idea 2: Too many children, some shall die to a deadly virus
        clamp = (newlen / 100) * oldlen
        if (clamp > 1.0):
            f = clamp
            while (f < newlen):
                newPopulation[floor(f)] = None # use None value because direct pop causes values to move
                f += clamp
            for monk in newPopulation:
                if (monk == None):
                    newPopulation.remove(monk)

        # Calculate fitness for the whole generation, even though there are likely more than needed, the weakest shall die
        maxFitnessInPop = 0
        if (self.elitismFitnessRecalcPrint): eflog = "EFR Before:"
        for monk in newPopulation:
            if isinstance(monk, Monk):
                success, exploredGarden = monk.explore(self.garden,self.fitnessWeight,self.gardenStepPrint,self.detailStepPrint, self.solutionPrint)
                if (success):
                    self.successCount += 1
                    self.successAttribs.append([self.generation, monk, exploredGarden, success])
                
                if (self.elitismFitnessRecalcPrint): eflog += str(monk.fitness) + " "
                
                if (monk.fitness > maxFitnessInPop):
                    maxFitnessInPop = monk.fitness

        # apply elitism value , sort the generated population
        if (self.elitismFitnessRecalcPrint): eflog += "\nEFR After:"
        for monk in newPopulation:
            if isinstance(monk, Monk):
                monk.fitness = monk.fitness % int((maxFitnessInPop + 1) * self.elitism) # (low elitism => more mixed fitness values => more random sort)
            if (self.elitismFitnessRecalcPrint): eflog += str(monk.fitness) + " "
        if (self.elitismFitnessRecalcPrint): print(eflog)

        newPopulation.sort()

        # remove weakest links to maintain population count
        newPopulation = newPopulation[0 : oldlen]

        # replace old generation
        self.population = newPopulation

    def successPrint(self, onlySuccessLevel: int = 1):
        lastgeneration = 0
        perLevelSuccessCounter = 0
        for occurence in self.successAttribs:

            # saved attributes
            generation: int = occurence[0]
            monk: Monk = occurence[1]
            garden: Garden = occurence[2]
            successLevel: int = occurence[3]

            if (successLevel == onlySuccessLevel):
                perLevelSuccessCounter += 1

                # counter per generation
                if (generation != lastgeneration):
                    lastgeneration = generation
                    i = 1
                else:
                    i += 1

                # printing
                print("Monk no. " + str(i) + " in generation " + str(generation) + ": ")
                garden.print()

        print("Succeeded " + str(self.successCount) + " times in total within " + str(self.generation) + " generations.")
        print("From that, success level " + str(onlySuccessLevel) + " has occured " + str(perLevelSuccessCounter) + " times.")

    # ---------------------------

    def tabuSearch():
        pass