const { start } = require("repl")

function getData(path) {
    const fs = require("fs")
    const text = fs.readFileSync(path).toString("utf-8")
    return text.split("\r\n\r\n")
};


function parseNodeString(string) {
    const [nodeName, ...nextNames] = string.match(/[0-9A-Z]{3}/g)
    return [nodeName, nextNames]
}


class Node {
    constructor(name) {
        this.name = name   
        this.next = []
    }

    setNext(nextNodes) {
        this.next = nextNodes
    }

    getNext(rightOrLeft) {
        if (rightOrLeft === "R") {
            return this.next[1]
        } else {
            return this.next[0]
        }
    }
}


function stepsToEnd(currentNode, instructions) {
    let instructionsIndex = 0
    let steps = 0
    while (currentNode.name !== "ZZZ") {
        currentInstruction = instructions[instructionsIndex]
        instructionsIndex = (instructionsIndex + 1) % instructions.length

        currentNode = currentNode.getNext(currentInstruction)
        steps += 1
    }

    return steps
}


function partOne() {
    const [moverString, nodesStrings] = getData("./8/input.txt")
    const parsedNodeStrings = nodesStrings.split("\n").map(parseNodeString)
    let nodes = {}
    parsedNodeStrings.forEach(([name, _]) => nodes[name] = new Node(name))
    parsedNodeStrings.forEach(([name, nextNames]) => nodes[name].setNext(nextNames.map(name => nodes[name])))
    
    console.log(stepsToEnd(nodes["AAA"], moverString.split("")))
}


function isAllNodesAtEnd(currentNodes) {
    return currentNodes.filter(node => node.name[2] === "Z").length === currentNodes.length
}


function ghostStepsToEnd(currentNode, instructions) {
    let instructionsIndex = 0
    let steps = 0
    while (currentNode.name[2] !== "Z") {
        currentInstruction = instructions[instructionsIndex]
        instructionsIndex = (instructionsIndex + 1) % instructions.length
        currentNode = currentNode.getNext(currentInstruction)
        
        steps += 1
    }
    
    return steps 
} 



function leastCommonMultiple(numbers) {
    function gcd(a, b) {
        return !b ? a : gcd(b, a % b);
    }

    function lcm(a, b) {
        return (a * b) / gcd(a, b);   
    }

    var multiple = numbers[0];
    numbers.forEach(function(n) {
        multiple = lcm(multiple, n);
    });

    return multiple;
}


function partTwo() {
    const [moverString, nodesStrings] = getData("./8/input.txt")
    const parsedNodeStrings = nodesStrings.split("\n").map(parseNodeString)
    
    let nodes = {}
    parsedNodeStrings.forEach(([name, _]) => nodes[name] = new Node(name))
    parsedNodeStrings.forEach(([name, nextNames]) => nodes[name].setNext(nextNames.map(name => nodes[name])))
    
    const startNodes = Object.values(nodes).filter(node => node.name[2] === "A")
    const stepPatterns = startNodes.map(node => ghostStepsToEnd(node, moverString.split("")))
    const lcmSteps = leastCommonMultiple(stepPatterns)
    console.log(lcmSteps)
}


// partOne()
partTwo()
