import colorama
import os
from _garden import GardenUtils

def main():
    colorama.init() # make termcolor work on windows

    # user-defined
    path = "map_samples"
    countPerSize = 5
    sizes = [[12, 10], [15, 15], [20, 5]] # each will get subdir in path

    # check/create directories
    if not os.path.exists(path):
        os.mkdir(path)
    for size in sizes:
        if not os.path.exists(path + "/" + str(size[0]) + "x" + str(size[1])):
            os.mkdir(path + "/" + str(size[0]) + "x" + str(size[1]))

    # generation into files (files will be overwritten)
    # hint: use GardenUtils.load() to load a generated file
    for size in sizes:
        print("Generating " + str(countPerSize) + " " + str(size[0]) + "x" + str(size[1]) + " gardens:")
        for i in range(countPerSize):
            garden = GardenUtils.generate(size[0], size[1]) # generating with default values
            garden.print()
            GardenUtils.save(garden, path + "/" + str(size[0]) + "x" + str(size[1]) + "/" + str(i + 1))

    return

if __name__ == "__main__":
    main()