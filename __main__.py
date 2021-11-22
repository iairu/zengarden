import colorama
from _garden import GardenUtils

def main():
    colorama.init() # make termcolor work on windows

    garden = GardenUtils.load("map_samples/10/1")
    GardenUtils.print(garden)

    return

if __name__ == "__main__":
    main()