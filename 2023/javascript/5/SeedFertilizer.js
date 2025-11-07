function getData(path) {
    const fs = require("fs")
    const text = fs.readFileSync(path).toString("utf-8")
    return text
};


class ConversionRange {
    constructor(destinationStart, sourceStart, length) {
        this.destinationStart = destinationStart
        this.sourceStart = sourceStart
        this.length = length
    }

    isInRange(sourceNumber) {
        return (sourceNumber >= this.sourceStart && sourceNumber < (this.sourceStart + this.length)) 
    }

    convert(sourceNumber) {
        const offset = sourceNumber - this.sourceStart
        return this.destinationStart + offset
    }
}


class CategoryMap {
    constructor(rangeNumbers) {
        this.conversionRanges = rangeNumbers.map(range => new ConversionRange(...range))
    }

    convert(sourceNumber) {
        const selectedRange = this.conversionRanges.filter(range => range.isInRange(sourceNumber))

        if (selectedRange.length > 0) {
            return selectedRange[0].convert(sourceNumber)
        } else {
            return sourceNumber
        }
    }
}


function parseMap(mapString) {
    const ranges = mapString.split("\r\n").slice(1)
    const rangeNumbers = ranges.map(string => string.split(" ").map(numberString => parseInt(numberString)))
    return rangeNumbers
}


function parseInstructions(text, reverse=false) {
    const [seeds, ...maps] = text.split("\r\n\r\n")
    const seedNumbers = seeds.split(": ")[1].split(" ").map(string => parseInt(string))

    const mapRanges = maps.map(parseMap)
    let categoryMaps
    if (reverse) {
        const reversedMapRanges = mapRanges.map(range => range.map(numbers => [numbers[1], numbers[0], numbers[2]])).reverse()
        categoryMaps = reversedMapRanges.map(cMap => new CategoryMap(cMap))
    } else {
        categoryMaps = mapRanges.map(cMap => new CategoryMap(cMap))
    }
    return [seedNumbers, categoryMaps]
}


function partOne() {
    const text = getData("./5/input.txt")
    const [seeds, categoryMaps] = parseInstructions(text)

    const locations = seeds.map(seed => categoryMaps.reduce((number, cMap) => cMap.convert(number), seed))

    console.log(Math.min(...locations))
}


class SeedRange {
    constructor(start, length) {
        this.start = start
        this.length = length
    }

    isInRange(number) {
        return (number >= this.start && number < (this.start + this.length))
    }

}


function partTwo() {
    const text = getData("./5/input.txt")
    const [seeds, categoryMaps] = parseInstructions(text, reverse=true)

    let seedPairs = []
    for (let i = 0; i < seeds.length; i += 2) {
        seedPairs.push(seeds.slice(i, i+2))
    }

    const seedRanges = seedPairs.map(pair => new SeedRange(...pair))
    let reverseSeed = 0
    let reverseSeedFound = false
    while (!reverseSeedFound) {
        const seed = categoryMaps.reduce((number, cMap) => cMap.convert(number), reverseSeed)
        const validRange =  seedRanges.filter(range => range.isInRange(seed))

        if (validRange.length > 0) {
            reverseSeedFound = true
        }

        reverseSeed += 1
    }

    console.log(reverseSeed-1)
}


// partOne()
partTwo()
