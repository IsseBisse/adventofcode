function getData(path) {
    const fs = require("fs")
    const text = fs.readFileSync(path).toString("utf-8")
    return text.split("\r\n")
};


function getPaths(lines) {
    const xLineWithIndex = lines.map(line => line.split("").map((char, index) => [char, index]))
    const xPaths = xLineWithIndex.map(line => line.filter(([char, _]) => char !== "."))
    
    const yLineWithIndex = [...Array(lines[0].length).keys()].map(colIndex => lines.map((line, rowIndex) => [line[colIndex], rowIndex]))
    const yPaths = yLineWithIndex.map(line => line.filter(([char, _]) => char !== "."))

    return [xPaths, yPaths]
}


function linspace(endPoints) {
    endPoints.sort((a, b) => a-b)
    const length = endPoints[1] - endPoints[0] + 1
    const points = [...Array(length).keys()].map(offset => endPoints[0] + offset)
    return points
}


class Ray {
    constructor(id, x, y, xMovement, positiveDirection, xMax, yMax, previousStates) {
        this.id = id
        
        this.x = x
        this.y = y
        
        this.xMovement = xMovement
        this.positiveDirection = positiveDirection

        this.yMax = yMax
        this.xMax = xMax

        this.energizedPositions = new Set()
        this.previousStates = previousStates
    }

    getNextObsticle(xPaths, yPaths) {
        const paths = this.xMovement ? xPaths : yPaths
        const pathPosition = this.xMovement ? this.x : this.y
        const pathIndex = this.xMovement ? this.y : this.x
        const skipObsticle = this.xMovement ? "-" : "|"

        const currentPath = paths[pathIndex]
        const obsticlesInFront = this.positiveDirection ? currentPath.filter(([obsticle, index]) => index > pathPosition && obsticle !== skipObsticle) : currentPath.filter(([obsticle, index]) => index < pathPosition && obsticle !== skipObsticle).reverse()
       
        console.log(this.id)
        console.log(obsticlesInFront.map(item => `${item[0]}, ${item[1]}`))

        let nextObsticle
        if (obsticlesInFront.length === 0) {
            const maxPosition = this.xMovement ? this.xMax : this.yMax
            const position = this.positiveDirection ? maxPosition : -1 
            nextObsticle = ["O", position]

        } else {
            nextObsticle = obsticlesInFront[0]
        }

        return nextObsticle
    }

    moveToObsticle(obsticle, paths) {
        const [type, position] = obsticle
       
        if (type==="\\" && position===6) {
            console.log()
        }

        // Update energized (visited) positions
        let positions;
        if (this.xMovement) {
            positions = linspace([this.x, position]).map(x => [x, this.y])
            this.x = position
        } else {
            positions = linspace([this.y, position]).map(y => [this.x, y])
            this.y = position
        }
        positions.forEach(item => this.energizedPositions.add(item.join(",")))

        // Check for loops
        const currentStateString = [this.x, this.y, this.xMovement, this.positiveDirection].join(",")
        if (this.previousStates.has(currentStateString)) {
            return this.energizedPositions
        }
        this.previousStates.add(currentStateString)

        // Update direction of travel
        this.xMovement = !this.xMovement

        if (type === "/") {
            this.positiveDirection = !this.positiveDirection
        } else if (type === "|" || type === "-") {
            const newRay = new Ray(this.id+1, this.x, this.y, this.xMovement, !this.positiveDirection, this.xMax, this.yMax, this.previousStates)
            this.energizedPositions = new Set([...this.energizedPositions, ...newRay.move(paths)])
        }

        if (this.id===1) {
            console.log()
        }
    }

    move(paths) {
        const [xPaths, yPaths] = paths

        while((this.x >= 0 && this.x < this.xMax) && (this.y >= 0 && this.y < this.yMax)) {
            const nextObsticle = this.getNextObsticle(xPaths, yPaths)
            this.moveToObsticle(nextObsticle, paths)

            this.print()
            console.log("")
        }

        return this.energizedPositions
    }

    print() {
        console.log(`id: ${this.id}`)
        console.log(`[${this.x}, ${this.y}], xMov:${this.xMovement}, posMov:${this.positiveDirection}`)
        console.log(` ${[...Array(this.xMax).keys()].join("")}`)
        for (let y = 0; y < this.yMax; y++) {
            let chars = [y]
            for (let x = 0; x < this.xMax; x++) {
                if (this.energizedPositions.has([x, y].join(","))) {
                    chars.push("#")
                } else {
                    chars.push(".")
                }
            }

            console.log(chars.join(""))
        }
    }
}


function partOne() {
    const lines = getData("./16/smallInput.txt")
    const paths = getPaths(lines)
    const xMax = lines[0].length 
    const yMax = lines.length

    for (line of lines) {
        console.log(line)
    }

    const ray = new Ray(0, 0, 0, true, true, xMax, yMax, new Set())
    ray.move(paths)
    ray.print()
}


function partTwo() {
    
}


partOne()
partTwo()
