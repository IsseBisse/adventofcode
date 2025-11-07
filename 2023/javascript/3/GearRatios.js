const { match } = require("assert")

function getData(path) {
    const fs = require("fs")
    const text = fs.readFileSync(path).toString("utf-8").replace("\r", "")
    return text.split("\n")
};


class SchematicNumber {
    constructor(number, rowIndex, columnIndicies) {
        this.number = number 
        this.row = rowIndex
        this.col = columnIndicies
        this.cogCoordinates = null
    }

    getAdjacentDimensions(schematic) {
        const rowMax = schematic.length - 1
        const colMax = schematic[0].length - 1

        const rowDim = [this.row>0 ? this.row-1 : 0, this.row<rowMax ? this.row+1 : rowMax]
        const colDim = [this.col[0]>0 ? this.col[0]-1 : 0, this.col[1]<colMax ? this.col[1]+1 : colMax]

        return [rowDim, colDim]
    }

    getAdjacentSchematic(schematic) {
        const [rowDim, colDim] = this.getAdjacentDimensions(schematic)
        const adjacentSchematic = schematic.slice(rowDim[0], rowDim[1]+1).map(row => row.slice(colDim[0], colDim[1] + 1))
        return adjacentSchematic 
    }

    hasAdjecentSymbol(schematic) {
        const adjacentSchematic = this.getAdjacentSchematic(schematic)
        const adjacentSchematicString = adjacentSchematic.join("")

        return adjacentSchematicString.match(/[^0-9.]/) !== null
    }

    setCogCoordinates(schematic) {
        const [rowDim, colDim] = this.getAdjacentDimensions(schematic)
        for (let row = rowDim[0]; row <= rowDim[1]; row++) {
            for (let col = colDim[0]; col <= colDim[1]; col++) {
                if (schematic[row][col] === "*") {
                    this.cogCoordinates = [row, col]
                }
            }
        }
    }
    
}


function getNumbers(string, row) {
    const matches = [...string.matchAll(/[0-9]+/g)]
    const indicies = matches.map(match => new SchematicNumber(parseInt(match[0]), row, [match.index, match.index+match[0].length-1])) 
    return indicies
}


function partOne() {
    const schematic = getData("./3/input.txt")
    const numbers = schematic.map((e, i) => getNumbers(e, i)).flat()
    const validNumbers = numbers.filter(number => number.hasAdjecentSymbol(schematic))

    console.log(validNumbers.reduce((partialSum, number) => partialSum + number.number, 0))
}


function isMatching(first, second) {
    if (first === second) {
        return false
    }
    
    if (first.cogCoordinates === null || second.cogCoordinates === null) {
        return false
    }

    return (first.cogCoordinates[0]===second.cogCoordinates[0] && first.cogCoordinates[1]===second.cogCoordinates[1])
}


function calculateGearRatio(first, numbers) {
    const matchingNumbers = numbers.filter(second => isMatching(first, second))

    if (matchingNumbers.length > 0) {
        return matchingNumbers[0].number * first.number
    }

    return 0
}


function partTwo() {
    const schematic = getData("./3/input.txt")
    const numbers = schematic.map((e, i) => getNumbers(e, i)).flat()
    numbers.map(number => number.setCogCoordinates(schematic))

    const gearRatios = numbers.map(first => calculateGearRatio(first, numbers))
    console.log(gearRatios.reduce((partialSum, a) => partialSum + a, 0) / 2)
}


// partOne()
partTwo()
