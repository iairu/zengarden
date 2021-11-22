from random import randint, random
from termcolor import colored

def _generatePebblePositions_(side, pebblesChance: float = 0.33, maxPebbles: int = 3):
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
            pebblePos = randint(0, side - 1) # generate random position
            while (pebblePos in pebbles): # guarantee unique position by finding next empty
                pebblePos = (pebblePos + 1) % side
            pebbles.append(pebblePos)

    return pebbles

class GardenUtils:
    def generate(side: int, pebblesInRowChance: float = 0.33, maxPebblesPerRow: int = 3):
        garden = [["0"]*side for y in range(side)] 
        # array of strings = garden
        for row in range(side): # string of chars = row
            pebblePositions = _generatePebblePositions_(side, pebblesInRowChance, maxPebblesPerRow)
            for col in pebblePositions: # char
                garden[row][col] = "X"
        return garden

    def save(garden: list, path: str):
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
            garden.append(row)

        return garden

    def print(garden: list):
        # Available text colors:
        colors = ["red", "green", "yellow", "blue", "magenta", "cyan", "white"]
        colorlen = len(colors)
        # Available text highlights:
        # highlights = ["on_red", "on_green", "on_yellow", "on_blue", "on_magenta", "on_cyan", "on_white"]
        # Available attributes:
        # attributes = ["bold", "dark", "underline", "blink", "reverse", "concealed"]

        out = ""
        for rowId, rowElms in enumerate(garden):
            for elm in rowElms:
                if (elm == "X"):
                    out += colored(elm, "white", "on_white") 
                else:
                    out += colored(elm, colors[int(elm) % colorlen])
                out += " "
            out += "\n"
        print(out)
        return