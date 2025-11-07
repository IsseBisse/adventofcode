from dataclasses import dataclass
import re


def getData(path):
    with open(path) as file:
        text = file.read()

    return text.split("\n")

@dataclass
class Number:
    number: int
    row: int
    colStart: int
    colEnd: int


def partsFinder(schematic):
    rowMax = len(schematic)
    colMax = len(schematic[0])

    def hasAdjacentSymbol(number):
        rowDim = [max(number.row-1, 0), min(number.row+1, rowMax)]
        colDim = [max(number.colStart-1, 0), min(number.colEnd+1, colMax)]
        
        adjacentRows = [string[colDim[0]:colDim[1]] for string in schematic[rowDim[0]:rowDim[1]+1]]
        adjacentString = "".join(adjacentRows)
        return len(re.findall("[^0-9.]", adjacentString)) > 0

    return hasAdjacentSymbol


def parseRow(string, row):
    numbers = [Number(int(match.group()), row, match.span()[0], match.span()[1]) for match in re.finditer(r"[0-9]+", string)]
    return numbers


def partOne():
    schematic = getData("./3/input.txt")
    matches = [parseRow(string, idx) for idx, string in enumerate(schematic)]
    partsNumbers = [item for row in matches for item in row]     # Flatten

    finder = partsFinder(schematic)
    validPartsNumbers = [number.number for number in partsNumbers if finder(number)]

    with open("validPartsNumbers.txt", "w") as file:
        for number in validPartsNumbers:
            file.write(f"{number}\n")

    print(sum(validPartsNumbers))


if __name__ == "__main__":
    partOne()
    # partTwo()