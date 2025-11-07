def parseInput(filename):
	f = open(filename, "r")

	input = f.read()
	input = input.split()

	filedata = list()
	for char in input:
		filedata.append(int(char))

	return filedata

'''
Part 1
'''
#def createNodeStructure(filedata):

def eatFiledata(filedata):
	global nodeList

	numChildren = filedata.pop(0)
	numMetadata = filedata.pop(0)
	metadata = list()

	print('Created node with %d children and %d data' % (numChildren, numMetadata))	
	for i in range(numChildren):
		filedata = eatFiledata(filedata)

	for i in range(numMetadata):
		metadata.append(filedata.pop(0))
	nodeList.append(metadata)

	return filedata

def partOne():
	filedata = parseInput("testInput.txt")
	print(filedata)

	global nodeList
	nodeList = list()
	eatFiledata(filedata)
	print(nodeList)

	metadataSum = 0
	for node in nodeList:
		metadataSum += sum(node)
	print("Sum of metadata: %d" % metadataSum)

'''
Part 2
'''
from Node import Node

def partTwo():
	filedata = parseInput("input.txt")
	print(filedata)

	root = Node("1")
	root.eatFiledata(filedata)
	print(root)

	sumOfNodes = root.getValue()
	print("Sum of selected nodes: %d" % sumOfNodes)

'''
Main
'''
if __name__ == '__main__':
	partTwo()