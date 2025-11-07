const { start } = require("repl")

function getData(path) {
    const fs = require("fs")
    const text = fs.readFileSync(path).toString("utf-8")
    return text.split("\r\n")
};


class Node {
    constructor(value) {
        this.value = value
        
        this.adjacent = {"north": null, "south": null, "west": null, "east": null}
    }

    tilt(direction) {
        if (this.value !== "O") {
            return
        } 

        if (this.adjacent[direction] === null || this.adjacent[direction].value !== ".") {
            return
        }
        
        const tempValue = this.adjacent[direction].value
        this.adjacent[direction].value = this.value
        this.value = tempValue

        this.adjacent[direction].tilt(direction)
    }
}


function getNode(nodes, rowIndex, colIndex) {
    if (typeof nodes[rowIndex] === "undefined") {
        return null
    }

    if (typeof nodes[rowIndex][colIndex] === "undefined") {
        return null
    }

    return nodes[rowIndex][colIndex]
}


function createNodes(lines) {
    const nodes = lines.map(row => row.split("").map(value => new Node(value)))

    for (const [rowIndex, nodeRow] of nodes.entries()) {
        for (const [colIndex, node] of nodeRow.entries()) {
            node.adjacent["north"] = getNode(nodes, rowIndex-1, colIndex)
            node.adjacent["south"] = getNode(nodes, rowIndex+1, colIndex)
            node.adjacent["west"] = getNode(nodes, rowIndex, colIndex-1)
            node.adjacent["east"] = getNode(nodes, rowIndex, colIndex+1)
        }
    }

    return nodes
}


function tilt(nodes, direction) {
    const rowIndicies = [...Array(nodes.length).keys()]
    if (direction === "south") {
        rowIndicies.reverse()
    }    

    const colIndicies = [...Array(nodes[0].length).keys()]
    if (direction === "east") {
        colIndicies.reverse()
    }

    for (rowIndex of rowIndicies) {
        for (colIndex of colIndicies) {
            nodes[rowIndex][colIndex].tilt(direction)
        }
    }
}

function print(nodes) {
    const string = nodes.map(row => row.map(node => node.value).join("")).join("\r\n")
    console.log(string)
    console.log("")
}


function partOne() {
    const lines = getData("./14/input.txt")
    const nodes = createNodes(lines)
    // print(nodes)

    tilt(nodes, "north")
    // print(nodes)
    
    const weight = nodes.map((row, rowIndex) => row.filter(node => node.value === "O").length * (nodes.length - rowIndex))
    console.log(weight.reduce((partialSum, a) => partialSum+a, 0))
}


function spinCycle(nodes) {
    // const spunNodes  = ["north", "west", "south", "east"].reduce((previousNodes, direction) => tilt(previousNodes, direction), nodes)
    ["north", "west", "south", "east"].map(direction => tilt(nodes, direction))
    // return spunNodes
}


function toString(nodes) {
    return nodes.map(row => row.map(node => node.value).join("")).join("")
}


function partTwo() {
    const lines = getData("./14/input.txt")
    const nodes = createNodes(lines)
    const totalCycles = 1000000000
    
    let cycles = 0
    let nodesString = toString(nodes)
    let previousNodesStates = {}
    while (!(nodesString in previousNodesStates)) {
        previousNodesStates[nodesString] = cycles

        spinCycle(nodes)
        cycles += 1
        nodesString = toString(nodes)
    }

    const numCyclesUntilRepeat = cycles - previousNodesStates[nodesString]
    const numCyclesLeft = (totalCycles - cycles) % numCyclesUntilRepeat

    for (let idx = 0; idx < numCyclesLeft; idx++) {
        spinCycle(nodes)
    }

    const weight = nodes.map((row, rowIndex) => row.filter(node => node.value === "O").length * (nodes.length - rowIndex))
    console.log(weight.reduce((partialSum, a) => partialSum+a, 0))
}


// partOne()
partTwo()
