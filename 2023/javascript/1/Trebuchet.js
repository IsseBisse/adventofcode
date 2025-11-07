function getData(path) {
    const fs = require("fs")
    const text = fs.readFileSync(path).toString("utf-8")
    return text.split("\n")
};


function getDigits(string) {
    return string.match(/\d/g)
}


function calibrationNumberGetter(numberGetter) {
    function getCalibrationNumber(string) {
        numbers = numberGetter(string)
        firstLastNumbers = [numbers[0], numbers.slice(-1)[0]]
        calibrationNumber = parseInt(firstLastNumbers.join(""))

        // console.log(string, calibrationNumber)
        return calibrationNumber
    }

    return getCalibrationNumber
}


function partOne() {
    const lines = getData("./1/input.txt")
    getCalibration = calibrationNumberGetter(getDigits)
    const calibrationNumbers = lines.map(getCalibration)
    const calibrationSum = calibrationNumbers.reduce((partialSum, a) => partialSum + a, 0)
    console.log(calibrationSum)
}

const wordsToDigits = {
    "one":      "1",
    "two":      "2",
    "three":    "3",
    "four":     "4",
    "five":     "5",
    "six":      "6",
    "seven":    "7",
    "eight":    "8",
    "nine":     "9"    
}
function parseDigit(string) {
    if (string.match(/[a-z]/)) {
        return wordsToDigits[string]
    } else {
        return string
    }
}


function getDigitsAndDigitWords(string) {
    const regexExpression = new RegExp("(?=(" + Object.keys(wordsToDigits).concat(["\\d"]).join("|") + "))", "g")
    const digitsAndWords = [...string.matchAll(regexExpression)].map(subArray => subArray[1])
    const digits = digitsAndWords.map(parseDigit)
    return digits
}


function partTwo() {
    const lines = getData("./1/input.txt")
    getCalibration = calibrationNumberGetter(getDigitsAndDigitWords)
    const calibrationNumbers = lines.map(getCalibration)
    const calibrationSum = calibrationNumbers.reduce((partialSum, a) => partialSum + a, 0)

    console.log(calibrationSum)
}


partOne()
partTwo()
