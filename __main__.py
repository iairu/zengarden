import colorama
from _garden import GardenUtils
from _monk import Monk
from _evo import Evolution

def main():
    colorama.init() # make termcolor work on windows

    # sizes = [[12, 10], [15, 15], [20, 5]]
    sizes = [[20, 5]]
    maxGarden = 5 # files per samples folder 1 to 5
    # evolutionCounts = [10, 100, 200, 500, 700, 1000]
    evolutionCounts = [25]
    evolutionRetries = 3

    for size in sizes:
        for i in range(maxGarden):
            gardenHolder = GardenUtils.load("map_samples/" + str(size[0]) + "x" + str(size[1]) + "/" + str(i + 1))
            gardenHolder.print()
            for r in range(evolutionRetries): # retry with fresh first generation
                for evolutionCount in evolutionCounts: # try different counts of evolution
                    garden = GardenUtils.copy(gardenHolder)
                    evo = Evolution(garden = garden,
                                    populationCount = 10,
                                    fitnessStepOverRotWeight = 10,
                                    mutationChance = 0.2,
                                    crossPosition = garden.a,
                                    idealisticGenes = True,
                                    elitism = 0.7,
                                    gardenStepPrint = False,
                                    detailStepPrint = False,
                                    solutionPrint = False,
                                    elitismFitnessRecalcPrint = False)

                    print("[|", end = "")
                    for j in range(evolutionCount):
                        print("|", end = "")
                        evo.evolve()

                    print("]")

                    evo.successPrint(1) # change to 1 to print gardens of non-stuck monks that however still contain fields which haven't been visited

    return

if __name__ == "__main__":
    main()