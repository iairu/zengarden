from random import randint, random
from termcolor import colored

class Garden:
    def _getCount_(self, fieldContent: str):
        count = 0
        for row in self.garden:
            for elm in row:
                if (elm == fieldContent):
                    count += 1
        return count

    def __init__(self, a: int, b: int, garden: list, pebbleCount: int = -1):
        self.a = a
        self.b = b
        self.garden = garden
        self.pebbleCount = self._getCount_("X") if (pebbleCount < 0) else pebbleCount
        

    def print(self):
        # Available text colors:
        colors = ["red", "green", "yellow", "blue", "magenta", "cyan", "white"]
        colorlen = len(colors)
        # Available text highlights:
        # highlights = ["on_red", "on_green", "on_yellow", "on_blue", "on_magenta", "on_cyan", "on_white"]
        # Available attributes:
        # attributes = ["bold", "dark", "underline", "blink", "reverse", "concealed"]

        out = ""
        for rowId, rowElms in enumerate(self.garden):
            for elm in rowElms:
                if (elm == "X"):
                    out += colored(elm, "white", "on_white") 
                else:
                    out += colored(elm, colors[int(elm) % colorlen])
                out += " "
            out += "\n"
        print(out)
        return

class GardenUtils:
    def _generatePebblePositions_(a, pebblesChance: float = 0.33, maxPebbles: int = 3):
        # pebble generation
        pebbles = []

        # pebblesChance: determine whether this round will even have any pebbles
        generatePebbles = random() <= pebblesChance

        # round will have pebbles:
        if (generatePebbles):
            # select 1 up to maxPebbles count of pebbles
            pebbleCount = randint(1, maxPebbles)
            # give each pebble a unique position
            for pebble in range(pebbleCount):
                pebblePos = randint(0, a - 1) # generate random position
                while (pebblePos in pebbles): # guarantee unique position by finding next empty
                    pebblePos = (pebblePos + 1) % a
                pebbles.append(pebblePos)

        return pebbles

    # ---------------------------

    def generate(a: int, b: int, pebblesInRowChance: float = 0.33, maxPebblesPerRow: int = 3):
        garden = [["0"]*a for y in range(b)] 
        # array of strings = garden
        for row in range(b): # string of chars = row
            pebblePositions = GardenUtils._generatePebblePositions_(a, pebblesInRowChance, maxPebblesPerRow)
            for col in pebblePositions: # char
                garden[row][col] = "X"

        return Garden(a, b, garden)

    def copy(_garden: Garden):
        gardenCopy = []
        for row in _garden.garden:
            rowCopy = []
            for elm in row:
                rowCopy.append(str(elm));
            gardenCopy.append(rowCopy)
        
        return Garden(_garden.a, _garden.b, gardenCopy, _garden.pebbleCount)

    # ---------------------------

    def save(_garden: Garden, path: str):
        garden = _garden.garden
        out = ""
        for rowId, rowElms in enumerate(garden):
            for elm in rowElms:
                out += elm + " "
            out += "\n"
        
        with open(path, "w", encoding = "utf-8") as f:
            f.write(out)
        return

    def load(path: str):
        with open(path, "r", encoding = "utf-8") as f:
            lines = f.readlines()

        garden = []
        a = 0
        b = len(lines)
        for line in lines:
            row = []
            buffer = ""
            for char in line:
                if (char == " "):
                    row.append(buffer)
                    buffer = ""
                elif (char == "\n" or char == "\r"):
                    continue
                else:
                    buffer += char
            a = len(row)
            garden.append(row)

        return Garden(a, b, garden)
