import colorama
from _garden import GardenUtils
from _monk import Monk

def main():
    colorama.init() # make termcolor work on windows

    garden = GardenUtils.load("map_samples/10/1")
    # garden.print()

    monk1 = Monk(10)
    monk1.printGenes()

    success, exploredGarden = monk1.explore(garden, gardenStepPrint = False, detailStepPrint = False, solutionPrint = True)
    exploredGarden.print()

    # monk2 = Monk(10)
    # monk2.printGenes()

    # monkNextGen = Monk(monk1, monk2)
    # monkNextGen.printGenes()

    return

if __name__ == "__main__":
    main()