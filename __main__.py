import colorama
from _garden import GardenUtils
from _monk import Monk

def main():
    colorama.init() # make termcolor work on windows

    garden = GardenUtils.load("map_samples/10/1")
    GardenUtils.print(garden)

    entrances = 10*4

    monk1 = Monk(entrances)
    monk1.printGenes()

    monk2 = Monk(entrances)
    monk2.printGenes()

    monkNextGen = Monk(monk1, monk2)
    monkNextGen.printGenes()

    return

if __name__ == "__main__":
    main()