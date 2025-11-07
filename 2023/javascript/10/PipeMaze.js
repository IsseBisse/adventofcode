function getData(path) {
    const fs = require("fs")
    const text = fs.readFileSync(path).toString("utf-8")
    return text.split("\n")
};


function vectorAdd(a, b) {
    return a.map((e, i) => e + b[i])
}


function isInsideMap(coord, dim) {
    if (coord[0] < dim[0][0] || coord[0] > dim[0][1]) {
        return false
    }
    if (coord[1] < dim[1][0] || coord[1] > dim[1][1]) {
        return false
    }
    return true
}


const nextDirection = {
    "|": {"0,1": [0, 1], "0,-1": [0, -1]},
    "-": {"1,0": [1, 0], "-1,0": [-1, 0]},
    "L": {"-1,0": [0, -1], "0,1": [1, 0]},
    "J": {"1,0": [0, -1], "0,1": [-1, 0]},
    "7": {"1,0": [0, 1], "0,-1": [-1, 0]},
    "F": {"-1,0": [0,1], "0,-1": [1,0]},
    ".": {}
}


function isValidDirection(char, direction) {
    const directionString = direction.join(",")
    return directionString in nextDirection[char]
}


function getChar(coord, rows) {
    return rows[coord[1]][coord[0]]
}


function findValidDirection(startCoord, rows) {
    const steps = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    const mapDim = [[0, rows[0].length], [0, rows.length]]
    const notOutOfBounds = steps.filter(step => isInsideMap(vectorAdd(startCoord, step), mapDim))

    const validSteps = notOutOfBounds.filter(step => isValidDirection(getChar(vectorAdd(startCoord, step), rows), step))
    return validSteps[0]
}


function getMaze(rows) {
    const startRow = rows.findIndex(row => row.indexOf("S") > -1)
    const startCol = rows[startRow].indexOf("S")
    const startCoord = [startCol, startRow]

    let route = [[startCoord, "S"]]
    
    let currentDirection = findValidDirection(startCoord, rows)
    let currentCoord = vectorAdd(startCoord, currentDirection)
    let currentChar = getChar(currentCoord, rows)
    while (currentChar !== "S") {
        route.push([currentCoord, currentChar])

        currentDirection = nextDirection[currentChar][currentDirection.join(",")]
        currentCoord = vectorAdd(currentCoord, currentDirection)
        currentChar = getChar(currentCoord, rows)
    }

    return route
}   


function partOne() {
    const rows = getData("./10/input.txt")
    const route = getMaze(rows)
    console.log(Math.floor(route.length / 2))
}


// function expand(coords, maze) {

// }


// function findEnclosedCoords(route, maze) {
//     const [colMax, rowMax] = [maze[0].length, maze.length]
//     const unknownCoords = Array.from(Array(rowMax).keys()).map(rowCoord => {
//         return Array.from(Array(colMax).keys()).map(colCoord => [colCoord, rowCoord])
//     }).flat()
//     let unknownGroundCoords = unknownCoords.filter(coord => getChar(coord, maze) === ".")

//     let enclosedCoords = []
//     while (unknownGroundCoords.length > 0) {
//         const coord = unknownGroundCoords.pop()
//         const [isEnclosed, expandedCoords] = expand(coord, maze)

//         if (isEnclosed) {
//             enclosedCoords = enclosedCoords.concat(expandedCoords)
//         } 
//         // TODO: Remove enclosed coords from unknown
//         // unknownGroundCoords = unknownGroundCoords.filter(coord => coord ) 
//     }

//     console.log(unknownCoords)
// }


function calcPolygonArea(vertices) {
    var total = 0;

    for (var i = 0, l = vertices.length; i < l; i++) {
      var addX = vertices[i][0];
      var addY = vertices[i == vertices.length - 1 ? 0 : i + 1][1];
      var subX = vertices[i == vertices.length - 1 ? 0 : i + 1][0];
      var subY = vertices[i][1];

      total += (addX * addY * 0.5);
      total -= (subX * subY * 0.5);
    }

    return Math.abs(total);
}


function partTwo() {
    const rows = getData("./10/input.txt")
    const route = getMaze(rows)
    const vertices = route.map(coord => coord[0])
    // Polygon area - area of narrow tube (i.e. 1 per two tube pieces) = enclosed area
    const enclosedArea = calcPolygonArea(vertices) - vertices.length / 2 + 1
    console.log(enclosedArea)
}


// partOne()
partTwo()
