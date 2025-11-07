function getData(path) {
    const fs = require("fs")
    const text = fs.readFileSync(path).toString("utf-8")
    return text.split(",")
};


function hash(string) {
    return string.split("").reduce((previousValue, char) => {
        previousValue += char.charCodeAt(0)
        previousValue *= 17
        previousValue %= 256
        return previousValue
    }, 0)
}


function partOne() {
    const strings = getData("./15/input.txt")
    const hashes = strings.map(string => hash(string))
    
    console.log(hashes.reduce((partialSum, a) => partialSum + a, 0))
}


function parse(string) {
    const label = string.match(/[a-z]+/g)[0]
    const isRemoval =  string.includes("-")
    const focalLength = isRemoval ? null : parseInt(string.match(/[0-9]/g)[0])

    return [label, isRemoval, focalLength]
}


function remove(box, label) {
    const index = box.findIndex(item => item[0] === label)
    if (index < 0) {
        return box
    }
    
    box.splice(index, 1)
    return box
}


function add(box, label, focalLength) {
    const index = box.findIndex(item => item[0] === label)

    if (index < 0) {
        box.push([label, focalLength])
    } else {
        box[index] = [label, focalLength]
    }

    return box
}




function arrangeLenses(strings) {
    let boxes = [...Array(256)].map(e => [])
    
    for (string of strings) {
        const [label, isRemoval, focalLength] = parse(string)
        const boxIndex = hash(label)
        
        if (isRemoval) {
            boxes[boxIndex] = remove(boxes[boxIndex], label)
        } else {
            boxes[boxIndex] = add(boxes[boxIndex], label, focalLength)
        }  
        
        // console.log(string)
        // print(boxes)
    }

    return boxes
}


function print(boxes) {
    for (const [index, box] of boxes.entries()) {
        if (box.length === 0) {
            continue
        }

        const string = box.map(lens => lens.join(" ")).join(",")
        console.log(index, string)   
    }
    console.log("")
}


function focusingPower(boxes) {
    const powers = boxes.map((box, boxIndex) => box.map(([_, focalLength], lensIndex) => (boxIndex + 1)*(lensIndex + 1)*focalLength)).flat()
    return powers.reduce((partialSum, a) => partialSum+a, 0)
}


function partTwo() {
    const strings = getData("./15/input.txt")
    const boxes = arrangeLenses(strings)
    
    console.log(focusingPower(boxes))
}


// partOne()
partTwo()
