from random import randint
from termcolor import colored

directionCount = 4

class Monk:

    def _randomGenes_(self, mapEntranceCount: int, idealistic: bool = True):
        # Entrance genes
        # A position on the border from which monk will enter the garden is determined in order of these genes
        for option in range(mapEntranceCount):
            # generate a random entrance point
            entrance = randint(0, mapEntranceCount - 1)

            if (idealistic): 
                # make each entrance point unique = more ideal, because there is no point entering twice from the same spot
                # this won't remove collisions with exits but will give the monk a much better distribution of entrance points (will remove entrance collisions)
                while (entrance in self.genes):
                    entrance = (entrance + 1) % mapEntranceCount # look for next unused entrance
            self.genes.append(entrance)

        # Rotation genes
        # If the monk hits a rock or already visited place, these genes will determine the order in which he will attempt a different direction
        # Order: North, East, South, West from the end, where each number represents the order of trying the given direction
        # example         .... 3 0 1 2: try south, then east, then north, then west
        # mutated/non-idealistic example .... 3 0 3 2: try south, then west, then north, (then west) (no east will get tried and last west trial wont get reached because already tried)
        cache = []
        for option in range(directionCount):
            rotation = randint(0, 3)

            if (idealistic): 
                # make each entrance point unique = more ideal, because there is no point entering twice from the same spot
                # this won't remove collisions with exits but will give the monk a much better distribution of entrance points (will remove entrance collisions)
                while (rotation in cache):
                    rotation = (rotation + 1) % directionCount # look for next unused rotation
                cache.append(rotation)
            self.genes.append(rotation)
        return

    def __init__(self, mapEntranceCount_or_parent1, parent2 = None) -> None:
        self.genes = [] # mapEntranceCount * Entrance genes, 4 * Rotation genes
        self.fx = 0 # fitness result

        # Determine how to generate this Monk's chromozome based on whether he has parents or not
        if (mapEntranceCount_or_parent1 is not Monk):
            # first generation (no parents): use random gene values
            self._randomGenes_(mapEntranceCount_or_parent1)

        elif (mapEntranceCount_or_parent1 is Monk and parent2 is Monk):
            # todo: any other generation: cross + mutatechance*mutate
            pass

        return

    def printGenes(self): # color direction genes
        directionGenesStart = len(self.genes) - directionCount
        out = ""
        for i, gene in enumerate(self.genes):
            if (i < directionGenesStart):
                out += str(gene)
            else:
                out += colored(str(gene), "red")
            out += " "

        print(out)