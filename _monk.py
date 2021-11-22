from __future__ import annotations
from random import randint, random
from termcolor import colored

directionCount = 4

class Monk:

    def _randomGenes_(self, idealistic: bool = True):
        # Entrance genes
        # A position on the border from which monk will enter the garden is determined in order of these genes
        for option in range(self.mapEntranceCount):
            # generate a random entrance point
            entrance = randint(0, self.mapEntranceCount - 1)

            if (idealistic): 
                # make each entrance point unique = more ideal, because there is no point entering twice from the same spot
                # this won't remove collisions with exits but will give the monk a much better distribution of entrance points (will remove entrance collisions)
                while (entrance in self.genes):
                    entrance = (entrance + 1) % self.mapEntranceCount # look for next unused entrance
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

    # parent1 is prefered because its direction genes will be used
    def _crossMutate_(self, parent1: Monk, parent2: Monk, mutationChance: float = 0, crossPosition: int = 0):
        genesLen = len(parent1.genes) # expectation that both parents have equivalent length genes
        
        # minimal position from which genes will be replaced with other parent
        # excluding 0 and n because otherwise the child would be equivalent to a single parent
        # between <1 (second gene) ; n - 2 (gene before last)>
        # if a random number isn't used then user's input is anchored (just in case) to match the above
        crossPosition = ((crossPosition - 1) % (genesLen - 2)) + 1 if (crossPosition != 0) else randint(1, genesLen - 2)

        # from crossPosition onwards use parent1's genes
        newGenes = parent2.genes[0 : crossPosition]
        for gene in parent1.genes[crossPosition : genesLen]:
            newGenes.append(gene)

        # mutation (single gene)
        if (random() >= mutationChance):
            pos = randint(0,genesLen - 1)
            # mutation within compatible values (different for directions), no correction for duplicates
            newGenes[pos] = randint(0, self.mapEntranceCount) if (pos < genesLen - directionCount) else randint(0, directionCount)
            
        # new monk's birth
        self.genes = newGenes
        return

    # ---------------------------

    def __init__(self, mapEntranceCount_or_parent1: int | Monk, parent2: Monk | None = None, mutationChance: float = 0, crossPosition: int = 0) -> None:
        self.mapEntranceCount = 0
        self.genes = [] # mapEntranceCount * Entrance genes, 4 * Rotation genes
        self.fitness = 0 # exploration result

        # Determine how to generate this Monk's chromozome based on whether he has parents or not
        if isinstance(mapEntranceCount_or_parent1, int):
            # first generation (no parents): use random gene values
            self.mapEntranceCount = mapEntranceCount_or_parent1
            self._randomGenes_()

        elif (isinstance(mapEntranceCount_or_parent1, Monk) and isinstance(parent2, Monk)):
            parent1 = mapEntranceCount_or_parent1
            self.mapEntranceCount = parent1.mapEntranceCount # assuming both parents are compatible with this map size
            self._crossMutate_(parent1, parent2, mutationChance, crossPosition)

        return

    # ---------------------------

    def setFitness(self, fitness: int):
        self.fitness = fitness
        return

    def printGenes(self, padding: int = 2, newLineEvery: int = 10): # color direction genes
        directionGenesStart = len(self.genes) - directionCount
        out = ""
        for i, gene in enumerate(self.genes):
            genestr = str(gene)
            while (len(genestr) <= padding):
                genestr += " "

            if (i < directionGenesStart):
                out += genestr
            else:
                out += colored(genestr, "red")
            
            out += " "
            
            if ((i+1) % newLineEvery == 0):
                out += "\n"

        print(out)