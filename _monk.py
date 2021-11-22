from __future__ import annotations
from random import randint, random
from termcolor import colored
from _garden import Garden, GardenUtils

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
        # Order: Left, Right, Up, Down (if left >= right, prefer left, etc.)
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

    def __init__(self, mapSize_or_parent1: int | Monk, parent2: Monk | None = None, mutationChance: float = 0, crossPosition: int = 0) -> None:
        self.mapSize = 0
        self.mapEntranceCount = 0
        self.genes = [] # mapEntranceCount * Entrance genes, 4 * Rotation genes
        self.fitness = 0 # exploration result: number of steps + mapSize * mapSize - number of rotations
        # 0 is default, going negative would mean worse, so:     \_______________/ to guarantee positive values because "-" number of rotations
        # good fitness    = (mapSize * mapSize - pebbleCount) * weight + mapSize * mapSize - number of rotations
        # optimal fitness = (mapSize * mapSize - pebbleCount) * weight + mapSize * mapSize - 0

        self.exploreGardenStepPrint = False
        self.exploreDetailStepPrint = False

        # Determine how to generate this Monk's chromozome based on whether he has parents or not
        if isinstance(mapSize_or_parent1, int):
            # first generation (no parents): use random gene values
            self.mapSize = mapSize_or_parent1
            self.mapEntranceCount = self.mapSize * 4
            self._randomGenes_()

        elif (isinstance(mapSize_or_parent1, Monk) and isinstance(parent2, Monk)):
            parent1 = mapSize_or_parent1
            self.mapSize = parent1.mapSize # assuming both parents are compatible with this map size
            self.mapEntranceCount = self.mapSize * 4
            self._crossMutate_(parent1, parent2, mutationChance, crossPosition)

        return

    # ---------------------------

    def _findPassableDirection_(self, garden: list, x: int, y: int, prevDirection: str) -> str:
        leftBeforeRight: bool = self.genes[self.mapEntranceCount] >= self.genes[self.mapEntranceCount + 1] # L, R genes
        upBeforeDown: bool = self.genes[self.mapEntranceCount + 2] >= self.genes[self.mapEntranceCount + 3] # U, D genes
        encircled = False

        if (prevDirection == "up" or prevDirection == "down"):
            if (leftBeforeRight):
                if (x - 1 >= 0 and garden[y][x-1] == "0"):
                    return "left"
                elif (x + 1 < self.mapSize and garden[y][x+1] == "0"):
                    return "right"
                else:
                    encircled = True
            else:
                if (x + 1 < self.mapSize and garden[y][x+1] == "0"):
                    return "right"
                elif (x - 1 >= 0 and garden[y][x-1] == "0"):
                    return "left"
                else:
                    encircled = True

        elif (prevDirection == "left" or prevDirection == "right"):
            if (upBeforeDown):
                if (y - 1 >= 0 and garden[y-1][x] == "0"):
                    return "up"
                elif (y + 1 < self.mapSize and garden[y+1][x] == "0"):
                    return "down"
                else:
                    encircled = True
            else:
                if (y + 1 < self.mapSize and garden[y+1][x] == "0"):
                    return "down"
                elif (y - 1 >= 0 and garden[y-1][x] == "0"):
                    return "up"
                else:
                    encircled = True

        # special corner turn situation
        if (encircled and x in [0, self.mapSize - 1] and y in [0, self.mapSize - 1]):
            return "cornerturn"
        else:
            return "encircled"
        
    # returns False if encircled, True if success
    def _exploreSingle_(self, garden: list, x: int, y: int, direction: str, turn: int, steps: int, rotations: int) -> list:
        finished = False

        if (garden[y][x] != "0"):
            return [True, steps, rotations] # don't consider a blocked entrance an encirclement

        while (not finished):
            if (direction == "up"):
                for y in range(y, -1, -1):
                    if (self.exploreDetailStepPrint): 
                        print(direction + ": " + str(y) + " " + str(x))
                    if (garden[y][x] == "0"):
                        steps += 1
                        garden[y][x] = str(turn) # change number
                    else: # hit pebble or already explored
                        # go back, rotate
                        y += 1
                        direction = self._findPassableDirection_(garden, x, y, direction)
                        x += 1 if (direction == "right") else -1 if (direction == "left") else 0 # avoid self-collision by pre-moving
                        rotations += 1 if (direction in ["right", "left", "cornerturn"]) else 0
                        if (self.exploreDetailStepPrint):
                            print("\_ PEBBLE! Go " + direction)
                        break
            if (direction == "up"): # didn't break => loop finished, reached border, all ok
                finished = True

            if (direction == "down"):
                for y in range(y, self.mapSize, 1):
                    if (self.exploreDetailStepPrint): 
                        print(direction + ": " + str(y) + " " + str(x))
                    if (garden[y][x] == "0"):
                        steps += 1
                        garden[y][x] = str(turn) # change number
                    else: # hit pebble or already explored
                        # go back, rotate
                        y -= 1
                        direction = self._findPassableDirection_(garden, x, y, direction)
                        x += 1 if (direction == "right") else -1 if (direction == "left") else 0 # avoid self-collision by pre-moving
                        rotations += 1 if (direction in ["right", "left", "cornerturn"]) else 0
                        if (self.exploreDetailStepPrint):
                            print("\_ PEBBLE! Go " + direction)
                        break
            if (direction == "down"): # didn't break => loop finished, reached border, all ok
                finished = True

            if (direction == "left"):
                order = range(x, -1, -1)
                for x in order:
                    if (self.exploreDetailStepPrint): 
                        print(direction + ": " + str(y) + " " + str(x))
                    if (garden[y][x] == "0"):
                        steps += 1
                        garden[y][x] = str(turn) # change number
                    else: # hit pebble or already explored
                        # go back, rotate
                        x += 1
                        direction = self._findPassableDirection_(garden, x, y, direction)
                        y += 1 if (direction == "down") else -1 if (direction == "up") else 0 # avoid self-collision by pre-moving
                        rotations += 1 if (direction in ["down", "up", "cornerturn"]) else 0
                        if (self.exploreDetailStepPrint):
                            print("\_ PEBBLE! Go " + direction)
                        break
            if (direction == "left"): # didn't break => loop finished, reached border, all ok
                finished = True

            if (direction == "right"):
                for x in range(x, self.mapSize, 1):
                    if (self.exploreDetailStepPrint): 
                        print(direction + ": " + str(y) + " " + str(x))
                    if (garden[y][x] == "0"):
                        steps += 1
                        garden[y][x] = str(turn) # change number
                    else: # hit pebble or already explored
                        # go back, rotate
                        x -= 1
                        direction = self._findPassableDirection_(garden, x, y, direction)
                        y += 1 if (direction == "down") else -1 if (direction == "up") else 0 # avoid self-collision by pre-moving
                        rotations += 1 if (direction in ["down", "up", "cornerturn"]) else 0
                        if (self.exploreDetailStepPrint):
                            print("\_ PEBBLE! Go " + direction)
                        break
            if (direction == "right"): # didn't break => loop finished, reached border, all ok
                finished = True

            if (direction == "cornerturn"): # valid special case that immediately finishes
                finished = True
                steps += 1

            if (direction == "encircled"):
                return [False, steps, rotations]

        return [True, steps, rotations]

    def explore(self, _garden: Garden, weight: int = 2, gardenStepPrint = False, detailStepPrint = False, solutionPrint = False): 
        # assigns fitness, returns [success bool, Garden explored state]
        # save additional printing options for internal functions
        self.exploreGardenStepPrint = gardenStepPrint
        self.exploreDetailStepPrint = detailStepPrint

        turns = 0 # round counter (for printing)
        steps = 0 # step counter (for fitness)
        rotations = 0 # for additional fitness optimization
        success = True

        garden = GardenUtils.copy(_garden)
        for gene in self.genes[0 : len(self.genes) - 4]:
            if (self.exploreGardenStepPrint):
                garden.print()
            # upper border
            if (gene >= 0 and gene < self.mapSize):
                success, steps, rotations = self._exploreSingle_(garden = garden.garden, x = gene, y = 0, direction = "down", turn = turns + 1, steps = steps, rotations = rotations)

            # right border
            elif (gene >= self.mapSize and gene < self.mapSize * 2):
                gene -= self.mapSize
                success, steps, rotations = self._exploreSingle_(garden = garden.garden, x = self.mapSize - 1, y = gene, direction = "left", turn = turns + 1, steps = steps, rotations = rotations)

            # bottom border
            elif (gene >= self.mapSize * 2 and gene < self.mapSize * 3):
                gene -= self.mapSize * 2
                success, steps, rotations = self._exploreSingle_(garden = garden.garden, x = gene, y = self.mapSize - 1, direction = "up", turn = turns + 1, steps = steps, rotations = rotations)

            # left border
            elif (gene >= self.mapSize * 3 and gene < self.mapSize * 4):
                gene -= self.mapSize * 3
                success, steps, rotations = self._exploreSingle_(garden = garden.garden, x = 0, y = gene, direction = "right", turn = turns + 1, steps = steps, rotations = rotations)

            turns += 1 # round finished, add to counter

            if (not success): # monk failed, execution!
                break

        # Assign fitness - only step count for now without rotations
        fieldCount = self.mapSize * self.mapSize
        pebbleCount = garden.pebbleCount
        self.fitness = steps * weight + fieldCount - rotations

        # Solution printing
        if (solutionPrint):
            if (success):
                print("Monk succeeded after " + str(steps) + " steps, " + str(rotations) + " rotations, " + str(turns) + " rounds.")
                print("Fitness: " + str(self.fitness))
            else:
                print("Monk failed after " + str(steps) + " steps, " + str(rotations) + " rotations, encircled in " + str(turns) + "th round.")
                print("Fitness: " + str(self.fitness))

        return [success, garden]

    def printGenes(self, newLineEvery: int = 10, padding: int = 2): # color direction genes
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