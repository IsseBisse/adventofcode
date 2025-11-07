function getData(path) {
    const fs = require("fs")
    const text = fs.readFileSync(path).toString("utf-8")
    return text.split("\r\n")
};


function parseInstruction(line) {
    const [direction, length, color] = line.split(" ")
    return [direction, parseInt(length), color.slice(2, -1)]
}

class Pixel extends Array {
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


directionToCoords = {
    "R": new Pixel(1, 0),
    "L": new Pixel(-1, 0),
    "U": new Pixel(0, 1),
    "D": new Pixel(0, -1)
}
function digTrench(instructions) {
    const edgePixels = new Map()

    instructions.reduce((current, instruction) => {
        const [direction, distance, _] = instruction
        const directionPixel = directionToCoords[direction]
        
        const newLine = [...Array(distance).keys()].map(steps => {
            const newPixel = current.add(directionPixel.scale(steps+1))
            edgePixels.set(newPixel.toString(), newPixel)
        })
        
        return current.add(directionPixel.scale(distance))        
    }, 
    new Pixel(0, 0))

    return edgePixels
}


// function floodFill(pixel, filledPixels) {
//     if (filledPixels.has(pixel.toString())) {
//         return
//     }
//     filledPixels.set(pixel.toString(), pixel)
//     console.log(pixel)

//     for (const [_, directionPixel] of Object.entries(directionToCoords)) {
//         floodFill(pixel.add(directionPixel), filledPixels)
//     }
//     return
// }


function floodFill(startPixel, filledPixels) {
    let pixelsToCheck = [startPixel]
    
    while (pixelsToCheck.length > 0) {
        const pixel = pixelsToCheck.pop() 

        if (!filledPixels.has(pixel.toString())) {
            filledPixels.set(pixel.toString())

            for (const [_, directionPixel] of Object.entries(directionToCoords)) {
                pixelsToCheck.push(pixel.add(directionPixel))
            }
        }
    }
    
    return filledPixels
}


function findStartPixel(edgePixels) {
    const edgePixelArray = [...edgePixels.values()]
    const startPixel = edgePixelArray[0].add(edgePixelArray[edgePixelArray.length-2])
    return startPixel
}


function partOne() {
    const lines = getData("./18/input.txt") 
    const instructions = lines.map(parseInstruction)
    const edgePixels = digTrench(instructions)

    const startPixel = findStartPixel(edgePixels)
    floodFill(startPixel, edgePixels)
    console.log(edgePixels.size)
}


function partTwo() {
    
}


partOne()
partTwo()
