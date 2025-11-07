function getData(path) {
    const fs = require("fs")
    const text = fs.readFileSync(path).toString("utf-8")
    return text.split("\n")
};


function diff(sequence) {
    return sequence.map((value, index, array) => {
        const next = (index+1) < array.length ? array[index+1] : 0
        return next - value
    }).slice(0, -1)
}


function getNext(sequence) {
    const diffSequence = diff(sequence)
    // console.log(diffSequence)
    if (diffSequence.every(value => value === 0))  {
        return sequence.slice(-1)[0]
    }

    return sequence.slice(-1)[0] + getNext(diffSequence)
}


function partOne() {
    const sequences = getData("./9/input.txt").map(row => row.split(" ").map(string => parseInt(string)))
    const differences = sequences.map(diff)

    const next = sequences.map(getNext)    
    console.log(next.reduce((partialSum, a) => partialSum + a, 0)) 
}


function getPrevious(sequence) {
    const diffSequence = diff(sequence)
    // console.log(diffSequence)
    if (diffSequence.every(value => value === 0))  {
        return sequence.slice(0)[0]
    }

    return sequence.slice(0)[0] - getPrevious(diffSequence)
}


function partTwo() {
    const sequences = getData("./9/input.txt").map(row => row.split(" ").map(string => parseInt(string)))
    const differences = sequences.map(diff)

    const previous = sequences.map(getPrevious)    
    console.log(previous.reduce((partialSum, a) => partialSum + a, 0)) 
}


// partOne()
partTwo()
