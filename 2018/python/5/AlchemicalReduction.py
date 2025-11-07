def parseFile(filename):
    f = open(filename, "r")

    # Read .txt file and parse into list of strings
    input = f.read()
 
    # Convert to list
    input = list(input)

    return input

'''
Part 1
'''
def collapseList(polymer):
    # Loop until full pass
    i = 1
    while i < len(polymer):
        asciiDiff = abs(ord(polymer[i]) - ord(polymer[i - 1]))

        if asciiDiff == 32:
            del polymer[i]
            del polymer[i-1]
            if i > 1:
                i -= 1
            else:
                i = 1
        else:
            i += 1

    return polymer


def partOne():
    #polymer = parseFile("input.txt")
    #print(polymer)

    polymer = list("abcdefghijklLKJIHGFEDCBA")
    polymer = collapseList(polymer)
    print(polymer)
    print('Remaining units: %d' % len(polymer))

'''
Part 2
'''
def getUniquePairs(polymer):
    # Get and sort unique
    polySet = set(polymer)
    polyList = list(polySet)
    polyList.sort()

    # Pair capital and small letters
    uniquePairs = list()
    halfLen = int(len(polyList) / 2)

    for i in range(halfLen):
        uniquePairs.append([polyList[i], polyList[i + halfLen]])

    return uniquePairs

def partTwo():
    # Read file
    polymer = parseFile("input.txt")

    # Get unique pairs
    uniquePairs = getUniquePairs(polymer)
    
    
    # Find shortest polymer
    collapsedLen = list()
    for pair in uniquePairs:
        print(pair)

        tempPolymer = list()
        # Remove all units of selected type
        for char in polymer: #TODO change to addition
            if char not in pair:
                tempPolymer.append(char)

        print('Length after removal: %d' % len(tempPolymer))

        # Collapse list
        tempPolymer = collapseList(tempPolymer)
        collapsedLen.append(len(tempPolymer))
        
        print('Length after collapse: %d' % len(tempPolymer))
    
    print('')
    print('Minimum lenght after collapse: %d' % min(collapsedLen))
    
'''
Main
'''
if __name__ == '__main__':
    partTwo()