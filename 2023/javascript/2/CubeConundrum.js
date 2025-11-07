function getData(path) {
    const fs = require("fs")
    const text = fs.readFileSync(path).toString("utf-8")
    return text.split("\n")
}


function parseGame(string) {
    const setStrings = string.split(":")[1]
    const sets = setStrings.split(";").map(parseSet)
    const minNumCubes = sets.reduce((currentMax, a) => currentMax.map((e, i) => e > a[i] ? e : a[i]), [0, 0, 0])    // "column-wise" max
    console.log(string, minNumCubes)
    // console.log(minNumCubes, isPossible(minNumCubes))
    return minNumCubes
}


function parseSet(string) {
    const regexExpressions = [/([0-9]+) red/, /([0-9]+) green/, /([0-9]+) blue/]
    const counter = cubeCounter(string)
    const numCubes = regexExpressions.map(counter)
    // console.log(string, numCubes)
    return numCubes
}


function cubeCounter(string) {
    function count(regex) {
        const cubeMatch = string.match(regex)
        return cubeMatch === null ? 0 :parseInt(cubeMatch[1])
    }
    return count
}


function isPossible(game) {
    maxNumCubes = [12, 13, 14]  // red, green, blue
    return game.every((numCubes, i) => numCubes <= maxNumCubes[i])
}


function partOne() {
    const gameStrings = getData("./2/input.txt")
    const games = gameStrings.map(parseGame)
    const possibleGamesIds = games.map((_, i) => i).filter(i => isPossible(games[i])).map(i => i+1)
    // console.log(games)
    // console.log(possibleGamesIds)
    
    console.log(possibleGamesIds.reduce((partialSum, a) => partialSum + a, 0))
}


function partTwo() {
    const gameStrings = getData("./2/input.txt")
    const games = gameStrings.map(parseGame)
    const gamePowers = games.map(minNumCubes => minNumCubes.reduce((partialProduct, a) => partialProduct * a, 1))
    
    console.log(gamePowers.reduce((partialSum, a) => partialSum + a, 0))
}


// partOne()
partTwo()
