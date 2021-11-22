import colorama
from _garden import GardenUtils
from _monk import Monk
from _evo import Evolution

def main():
    colorama.init() # make termcolor work on windows

    size = [20, 5]
    garden = GardenUtils.load("map_samples/" + str(size[0]) + "x" + str(size[1]) + "/1")
    garden.print()
    Evolution(  garden = garden,
                populationCount = 10,
                fitnessStepOverRotWeight = 2,
                mutationChance = 0,
                crossPosition = 0,
                idealisticGenes = True,
                elitism = 0.1,
                gardenStepPrint = False,
                detailStepPrint = False,
                solutionPrint = True,
                elitismFitnessRecalcPrint = True)


    # monk1 = Monk(size)
    # monk1.printGenes()

    # success, exploredGarden = monk1.explore(garden, gardenStepPrint = False, detailStepPrint = False, solutionPrint = True)
    # exploredGarden.print()

    # monk2 = Monk(10)
    # monk2.printGenes()

    # monkNextGen = Monk(monk1, monk2)
    # monkNextGen.printGenes()

    return

if __name__ == "__main__":
    main()