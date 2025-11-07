function getData(path) {
    const fs = require("fs")
    const text = fs.readFileSync(path).toString("utf-8")
    return text.split("\n")
};


function parseCard(string) {
    // const cardNumber = parseInt(string.split(":")[0].split(" ")[1])
    const winningNumbersString = string.split(": ")[1].split(" | ")[0]
    const winningNumbers = new Set(winningNumbersString.match(/[0-9]+/g).map(numberString => parseInt(numberString)))

    const numbersString = string.split(": ")[1].split(" | ")[1]
    const numbers = numbersString.match(/[0-9]+/g).map(numberString => parseInt(numberString))

    return [winningNumbers, numbers]
}


function calculateNumMatches(cardString) {
    const [winningNumbers, numbers] = parseCard(cardString)

    const scoreNumbers = numbers.filter(number => winningNumbers.has(number))
    
    return scoreNumbers.length
}


function partOne() {
    const cards = getData("./4/input.txt")
    const numMatches = cards.map(calculateNumMatches)
 
    const scores = numMatches.map(len => len>0 ? 2**(len -1) : 0)
    console.log(scores.reduce((partialSum, a) => partialSum + a, 0))
}


function partTwo() {
    const cards = getData("./4/input.txt")
    const numMatches = cards.map(calculateNumMatches)
    const numOfEachCard = Array.from({ length: cards.length}, () => 1)

    for (let i = 0; i < cards.length; i++) {
        numOfCurrent = numOfEachCard[i]
        for (let j = 1; j < numMatches[i]+1; j++) {
            if (i+j < cards.length) {
                numOfEachCard[i+j] += numOfCurrent
            }
        }
    }

    console.log(numOfEachCard.reduce((partialSum, a) => partialSum + a, 0))
}


partOne()
partTwo()
