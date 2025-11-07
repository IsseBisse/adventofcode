function getData(path) {
    const fs = require("fs")
    const text = fs.readFileSync(path).toString("utf-8")
    return text.split("\r\n")
};


function zip(arrays) {
    return arrays[0].map((_, i) => arrays.map(array => array[i]))
}


function parseInput(rows) {
    const times = rows[0].match(/[0-9]+/g).map(string => parseInt(string))
    const distances = rows[1].match(/[0-9]+/g).map(string => parseInt(string))
    return zip([times, distances])
}


function pq(p, q) {
    under_root = (p/2)**2 - q
    if (under_root < 0) {
        return null
    }

    return [-p/2 + Math.sqrt(under_root), -p/2 - Math.sqrt(under_root)]
}


function getNumWinningStrategies(time, distance) {
    const [t1, t2] = pq(time, distance+1)   // min/max times are negative
    const minChargeTime = -t1
    const maxChargeTime = -t2
    const numWinningStrategies = Math.floor(maxChargeTime)-Math.ceil(minChargeTime) + 1

    return numWinningStrategies    
}


function partOne() {
    const races = parseInput(getData("./6/input.txt"))
    const numWinningStrategies = races.map(race => getNumWinningStrategies(...race))

    console.log(numWinningStrategies.reduce((partialProduct, a) => partialProduct*a, 1))
}


function partTwo() {
    // const races = [[71530, 940200]]
    const races = [[55826490, 246144110121111]]
    const numWinningStrategies = races.map(race => getNumWinningStrategies(...race))
    
    console.log(numWinningStrategies.reduce((partialProduct, a) => partialProduct*a, 1))
}


partOne()
partTwo()
