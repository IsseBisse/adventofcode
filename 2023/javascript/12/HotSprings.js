const exp = require("constants")

function getData(path) {
    const fs = require("fs")
    const text = fs.readFileSync(path).toString("utf-8")
    return text.split("\r\n")
};


function parseRow(row) {
    const [spring, groupString] = row.split(" ")
    const group = groupString.split(",").map(string => parseInt(string))

    return [spring, group]
}


function groupSpring(spring) {
    const matches = [...spring.matchAll(/(?:^|\.)(#+)(?=$|\.)/g)]
    if (matches === null) {
        return []
    }
    const groups = matches.map(match => match[1].length)
    return groups
}


function getPossibleConfigurations(spring, expectedGroups) {
    let combinations = []

    const springSplit = spring.split("?")
    const knownSpring = springSplit[0] + (springSplit.length > 1 ? "?" : "")
    const knownSpringGroups = groupSpring(knownSpring)
    for (const [index, knownGroup] of knownSpringGroups.entries()) {
        // If groups don't match we don't need to go deeper into the recursion
        if (knownGroup !== expectedGroups[index]) {
            return combinations
        } 
    }

    if (spring.includes("?")) {
        springOperational = spring.replace("?", ".")
        combinations = combinations.concat(getPossibleConfigurations(springOperational, expectedGroups))
        
        springBroken = spring.replace("?", "#")
        combinations = combinations.concat(getPossibleConfigurations(springBroken, expectedGroups))
    } else {
        combinations.push(spring)
    }

    return combinations
}


function partOne() {
    const rows = getData("./12/input.txt").map(parseRow)
    // const rows = [["?#?#?#?#?#?#?#?", [1,3,1,6]]]
    // const springs = rows.map(row => row[0])
    const groups = rows.map(row => row[1])

    const springConfigurations = rows.map(([spring, groups]) => getPossibleConfigurations(spring, groups))
    const validSpringConfigurations = springConfigurations.map((configuration, i) => {
        return configuration.filter(spring => groupSpring(spring).join(",") === groups[i].join(","))
    })

    console.log(validSpringConfigurations.map(config => config.length).reduce((partialSum, a) => partialSum + a, 0))
}


NUM_REPEATS = 5
function extend(row) {
    [spring, groups] = row
    
    extendedSpring = Array(NUM_REPEATS).fill(spring).join("?")
    extendedGroups = Array(NUM_REPEATS).fill(groups).flat()

    return [extendedSpring, extendedGroups]
}


function partTwo() {
    const rows = getData("./12/smallInput2.txt").map(parseRow)
    const extendedRows = rows.map(row => extend(row))
    const groups = extendedRows.map(row => row[1])

    const springConfigurations = extendedRows.map(([spring, groups]) => getPossibleConfigurations(spring, groups))
    const validSpringConfigurations = springConfigurations.map((configuration, i) => {
        return configuration.filter(spring => groupSpring(spring).join(",") === groups[i].join(","))
    })

    console.log(validSpringConfigurations.map(config => config.length).reduce((partialSum, a) => partialSum + a, 0))
}


// partOne()
start = performance.now()
partTwo()
console.log(performance.now() - start)
