function getData(path) {
    const fs = require("fs")
    const text = fs.readFileSync(path).toString("utf-8")
    return text.split("\r\n")
};


function getLayout(lines) {
    const linesWithCoords = lines.map((line, y) => line.split("").map((char, x) => [char, new Vector(x, y)]))
    const obsticles = linesWithCoords.map(line => line.filter(([char, _]) => char !== ".")).flat()

    let layout = new Map
    obsticles.forEach(([type, coords]) => layout.set(coords.toString(), type))
    return layout
}


class Vector extends Array {
    add(other) {
        return this.map((element, i) => element + other[i])
    }

    scale(scalar) {
        return this.map(element => element*scalar)
    }

    toString() {
        return this.join(",")
    }
}


function dash(direction) {
    if (Math.abs(direction[0]) === 1) {
        return [direction]
    } else {
        return [new Vector(-1, 0), new Vector(1, 0)]
    }
}
function pipe(direction) {
    if (Math.abs(direction[0]) === 1) {
        return [new Vector(0, -1), new Vector(0, 1)]
    } else {
        return [direction]
    }
}
function slash(direction) {
    if (Math.abs(direction[0]) === 1) {
        return [new Vector(0, -direction[0])]  
    } else {
        return [new Vector(-direction[1], 0)]
    } 
}
function backslash(direction) {
    if (Math.abs(direction[0]) === 1) {
        return [new Vector(0, direction[0])]  
    } else {
        return [new Vector(direction[1], 0)]  
    }
}
obsticleToFunctions = {
    "-": dash,
    "|": pipe,
    "/": slash,
    "\\": backslash
}


class Point {
    constructor(coords, direction) {
        this.coords = coords
        this.direction = direction
    }

    toString() {
        return `${this.coords.toString()},${this.direction.toString()}`
    }

    move(layout) {
        this.coords = this.coords.add(this.direction)

        if (layout.has(this.coords.toString())) {
            const obsticle = layout.get(this.coords.toString())
            const newDirections = obsticleToFunctions[obsticle](this.direction)
            const newPoints = newDirections.map(newDir => new Point(this.coords, newDir))
            return newPoints
        }

        return this
    }

    isInsideLayout(layoutDim) {
        if (this.coords.some(value => value < 0)) {
            return false
        }
        if (this.coords.some((value, index) => value >= layoutDim[index])) {
            return false
        }
        return true
    }
}


function print(points, previousStates, lines, overwriteLines=false) {
    const previousCoords = [...previousStates.keys()].map(state => state.split(",").slice(0, 2).join(","))
    const pointCoords = points.map(point => point.coords.toString())

    for (const [y, row] of lines.entries()) {
        let rowChars = []
        for (const [x, char] of row.split("").entries()) {
            if (pointCoords.includes([x, y].join(","))) {
                rowChars.push("O")
            } else if ((char === "." || overwriteLines) && previousCoords.includes([x, y].join(","))) {
                rowChars.push("x")
            } else {
                rowChars.push(char)
            }
        }
        console.log(rowChars.join(""))
    }
    console.log("")
}


function getStates(layout, lines, startPoint) {
    const layoutDim = new Vector(lines[0].length, lines.length)

    let points = [startPoint]
    let previousStates = new Set()
    while (points.length > 0) {
        previousStates = new Set([...previousStates, ...points.map(point => point.toString())])        
        points = points.map(point => point.move(layout)).flat()
            .filter(point => point)
            .filter(point => !previousStates.has(point.toString()))
            .filter(point => point.isInsideLayout(layoutDim))
            
            // print(points, previousStates, lines)
        }
        previousStates = new Set([...previousStates, ...points.map(point => point.toString())])
        
    // print(points, previousStates, lines, overwriteLines=true)
    return previousStates
}


function statesToCoords(states) {
    return new Set([...states.keys()].map(state => state.split(",").slice(0, 2).join(",")))
}


function partOne() {
    const lines = getData("./16/input.txt")
    const layout = getLayout(lines)

    const startPoint = new Point(new Vector(-1, 0), new Vector(1, 0))

    const previousStates = getStates(layout, lines, startPoint)
    
    const previousCoords = statesToCoords(previousStates) 
    console.log(previousCoords.size-1)
}


function partTwo() {
    const lines = getData("./16/input.txt")
    const layout = getLayout(lines)
    const layoutDim = new Vector(lines[0].length, lines.length)

    let startPoints = []
    const xCoords = [...Array(layoutDim[0]).keys()]
    startPoints = startPoints.concat(xCoords.map(x => new Point(new Vector(x, -1), new Vector(0, 1))))
    startPoints = startPoints.concat(xCoords.map(x => new Point(new Vector(x, layoutDim[1]), new Vector(0, -1))))
    
    const yCoords = [...Array(layoutDim[1]).keys()]
    startPoints = startPoints.concat(yCoords.map(y => new Point(new Vector(-1, y), new Vector(1, 0))))
    startPoints = startPoints.concat(yCoords.map(y => new Point(new Vector(1, y), new Vector(-1, 0))))

    const maxPreviousCoord = startPoints.map(startPoint => getStates(layout, lines, startPoint))
        .map(states => statesToCoords(states))
        .map(coords => coords.size-1)
        .reduce((previousValue, value) => value > previousValue ? value : previousValue, 0)
    console.log(maxPreviousCoord)
}


// partOne()
partTwo()
