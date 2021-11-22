import colorama
from _garden import GardenUtils
from _monk import Monk
from _evo import Evolution

def main():
    colorama.init() # make termcolor work on windows

    size = [12, 10]
    maxGarden = 5
    # size = [15, 15]
    # size = [20, 5]

    for i in range(maxGarden):
        evolutionCount = 10
        garden = GardenUtils.load("map_samples/" + str(size[0]) + "x" + str(size[1]) + "/" + str(i + 1))
        garden.print()
        evo = Evolution(garden = garden,
                        populationCount = 50,
                        fitnessStepOverRotWeight = 2,
                        mutationChance = 0,
                        crossPosition = 0,
                        idealisticGenes = True,
                        elitism = 0.1,
                        gardenStepPrint = False,
                        detailStepPrint = False,
                        solutionPrint = False,
                        elitismFitnessRecalcPrint = False)

        for i in range(evolutionCount):
            evo.evolve()

        evo.successPrint(2) # change to 1 to print gardens of non-stuck monks that however still contain fields which haven't been visited

    return

if __name__ == "__main__":
    main()