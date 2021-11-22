import colorama
import os
from _garden import GardenUtils

def main():
    colorama.init() # make termcolor work on windows

    # user-defined
    path = "map_samples"
    countPerSize = 5
    sizes = [10, 15, 20] # each will get subdir in path

    # check/create directories
    if not os.path.exists(path):
        os.mkdir(path)
    for size in sizes:
        if not os.path.exists(path + "/" + str(size)):
            os.mkdir(path + "/" + str(size))

    # generation into files (files will be overwritten)
    # hint: use GardenUtils.load() to load a generated file
    for size in sizes:
        print("Generating " + str(countPerSize) + " " + str(size) + "x" + str(size) + " gardens:")
        for i in range(countPerSize):
            garden = GardenUtils.generate(size) # generating with default values
            GardenUtils.print(garden)
            GardenUtils.save(garden, path + "/" + str(size) + "/" + str(i + 1))

    return

if __name__ == "__main__":
    main()