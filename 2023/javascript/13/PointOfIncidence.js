function getData(path) {
    const fs = require("fs")
    const text = fs.readFileSync(path).toString("utf-8")
    return text.split("\r\n\r\n")
};


function isMirrorLine(lines, startIndex) {
    let upper = startIndex
    let lower = startIndex + 1

    while (upper >= 0 && lower < lines.length) {
        if (lines[upper] !== lines[lower]) {
            return false
        }

        upper -= 1
        lower += 1
    }

    return true
}


function findMirrorLine(lines, previousIndex=0) {
    // Find two adjacent equal lines
    const matchingIndicies = lines.map((element, index) => element === lines[index+1] ? index : -1).filter(index => index !== -1)
    const mirrorIndicies = matchingIndicies.filter(index => isMirrorLine(lines, index))
    const nonPreviousIndicies = mirrorIndicies.filter(index => index+1 !== previousIndex)
    return nonPreviousIndicies.length > 0 ? nonPreviousIndicies[0]+1 : 0
}


function rotate(lines) {
    return lines[0].split("").map((_, colIndex) => lines.map(line => line[colIndex]).join("")) 
}


function find2DMirrorLine(pattern, previousLine=0, previousRotatedLine=0) {
    const lines = pattern.split("\r\n")
    const mirrorLine = findMirrorLine(lines, previousLine) 
    const rotatedMirrorLine = findMirrorLine(rotate(lines), previousRotatedLine)

    return [mirrorLine !== previousLine ? mirrorLine : 0, rotatedMirrorLine !== previousRotatedLine ? rotatedMirrorLine : 0]
}


function calculateScore(mirrorLines) {
    const scores = mirrorLines.map(([line, rotatedLine]) => line*100 + rotatedLine)
    return scores.reduce((partialSum, a) => partialSum + a, 0)
}


function partOne() {
    const patterns = getData("./13/input.txt")
    const mirrorLines = patterns.map(pattern => find2DMirrorLine(pattern))
    const score = calculateScore(mirrorLines)
    console.log(score)
}


function swapSmudge(pattern, index) {
    if (!["#", "."].includes(pattern[index])) {
        return null
    }

    const replacementChar = pattern[index] === "#" ? "." : "#"
    return pattern.substring(0, index) + replacementChar + pattern.substring(index+1);
}


function findOneSmudge2DMirrorLine(pattern) {
    const [previousLine, previousRotatedLine] = find2DMirrorLine(pattern)

    const smudgePatterns = pattern.split("").map((_, index) => swapSmudge(pattern, index)).filter(pattern => pattern)
    const smudgeMirrorLines = smudgePatterns.map(pattern => find2DMirrorLine(pattern, previousLine, previousRotatedLine))
    const nonZeroSmudgeMirrorLine = smudgeMirrorLines.filter(smudgeLine => smudgeLine.join(",") !== "0,0")
    
    if (nonZeroSmudgeMirrorLine.length === 0) {
        console.log()
    }

    return nonZeroSmudgeMirrorLine[0]
}


function partTwo() {
    const patterns = getData("./13/input.txt")
    const mirrorLines = patterns.map(pattern => findOneSmudge2DMirrorLine(pattern))
    const score = calculateScore(mirrorLines)
    console.log(score)
}


// partOne()
partTwo()
