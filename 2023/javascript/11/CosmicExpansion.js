function getData(path) {
    const fs = require("fs")
    const text = fs.readFileSync(path).toString("utf-8")
    return text.split("\r\n")
};


function charInserter(char) {
    function insertChar(string, index) {
        return string.slice(0, index) + char + string.slice(index) 
    }

    return insertChar
}


function rowInserter(row) {
    function insertRow(array, index) {
        return [...array.slice(0, index), row, ...array.slice(index)]
    }

    return insertRow
}


function expand(universe, insertedChar=".") {
    const expandColIndicies = [...Array(universe[0].length).keys()].filter(colIndex => {
        const col = universe.map(row => row[colIndex])
        return !col.includes("#")
    }).reverse()
    const insertChar = charInserter(insertedChar)
    const colExpandedUniverse = universe.map(row => expandColIndicies.reduce((string, index) => insertChar(string, index), row)) 

    const expandRowIndicies = [...universe.keys()].filter(index => !universe[index].includes("#"))
    const insertedRow = Array.from(Array(universe[0].length)).map(_ => insertedChar).join("")
    const insertRow = rowInserter(insertedRow)
    // Reverse to not mess up indicies
    const expandedUniverse = expandRowIndicies.reverse().reduce((universe, index) => insertRow(universe, index), colExpandedUniverse)
    
    return expandedUniverse
}


function getGalaxies(universe, skipSize=2) {
    let galaxies = []
    let rowSkips = 0
    for ([rowIndex, row] of universe.entries()) {
        let colSkips = 0
        if (row.split("").every(char => char === "x")) {
            rowSkips += 1
            continue
        }

        for ([colIndex, char] of row.split("").entries()) {
            if (char === "#") {
                galaxies.push([rowIndex+rowSkips*(skipSize-2), colIndex+colSkips*(skipSize-2)])
            } else if (char === "x") {
                colSkips += 1
            }
        } 
    } 

    return galaxies
}


function distance(first, second) {
    return Math.abs(first[0] - second[0]) + Math.abs(first[1] - second[1])
}


function partOne() {
    const universe = getData("./11/input.txt")
    const expandedUniverse = expand(universe)
    const galaxies = getGalaxies(expandedUniverse)
    const galaxyDistances = galaxies.map(first => galaxies.map(second => distance(first, second)))

    const totalGalaxyDistance = galaxyDistances.map(row => row.reduce((partialSum, a) => partialSum + a, 0))
    const totalDistance = totalGalaxyDistance.reduce((partialSum, a) => partialSum + a, 0) / 2

    console.log(totalDistance)

//     for (row of expandedUniverse) {
//         console.log(row)
//     }
}


function partTwo() {
    const universe = getData("./11/input.txt")
    const expandedUniverse = expand(universe, insertedChar="x")
    const galaxies = getGalaxies(expandedUniverse, skipSize=1000000)
    const galaxyDistances = galaxies.map(first => galaxies.map(second => distance(first, second)))
    const totalGalaxyDistance = galaxyDistances.map(row => row.reduce((partialSum, a) => partialSum + a, 0))
    const totalDistance = totalGalaxyDistance.reduce((partialSum, a) => partialSum + a, 0) / 2

    console.log(totalDistance)

//     for (row of expandedUniverse) {
//         console.log(row)
//     }
}


// partOne()
partTwo()
