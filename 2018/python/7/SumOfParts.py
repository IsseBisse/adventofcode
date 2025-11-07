def parseFile(filename):
	f = open(filename, "r")

	input = list()
	for line in f:
		lineSplit = line.split("\n")

		if type(lineSplit) == list:
			string = lineSplit[0]
		else:
			string = lineSplit

		relationship = parseInput(string)
		input.append(relationship)

	return input

def parseInput(string):
	parts = string.split("step")

	relationship = dict()
	relationship["parent"] = parts[0].split()[1]
	relationship["child"] = parts[1].split()[0]

	return relationship

'''
Part 1
'''
from Graph import Graph
from Node import Node

def createGraph(relationships):
	# Create list of unique nodes
	nodeNames = list()
	for relation in relationships:
		if not relation["parent"] in nodeNames:
			nodeNames.append(relation["parent"])
		if not relation["child"] in nodeNames:
			nodeNames.append(relation["child"])

	# Initialize graph and add relationship	
	graph = Graph(nodeNames, relationships)

	return graph

def findWorkOrder(graph):
	doneList = list()
	activeList = list()
	inactiveList = list()

	# Populate active and inactive list
	for name, node in graph.nodes.items():
		if not node.getParents():
			activeList.append(node)
		else:
			inactiveList.append(node)
	
	while inactiveList or activeList:
		# Select action
		activeList.sort(key=lambda k: k.name)
		currentNode = activeList[0]
		activeList.remove(currentNode)

		# Move first (alphabetically) node to done list
		doneList.append(currentNode)

		# Move (newly) active nodes to active list
		for child in currentNode.getChildren():
			child.removeParent(currentNode)

			# Add to active list if no parents
			if not child.getParents():
				activeList.append(child)
				inactiveList.remove(child)
		'''
		print("=== Done List ===")
		for node in doneList:
			print(node)

		print("=== Active List ===")
		for node in activeList:
			print(node)

		print("=== Inactive List ===")
		for node in inactiveList:
			print(node)
		print('')
		'''
	return doneList


def partOne():
	relationships = parseFile("input.txt")
	#print(relationships)

	graph = createGraph(relationships)
	#print(graph)

	order = findWorkOrder(graph)
	answerStr = ''
	for node in order:
		answerStr += node.name
	print(answerStr)

'''
Part 2
'''
def printCurrentState(currSec, jobList, doneList):
	statusString = "%4d     "

	# Add worker status
	workerStrings = '.' * 5
	for ind, string in enumerate(workerStrings):
		if jobList[ind]:
			string = jobList[ind].name

		statusString += string + "   "

	# Add done status
	doneString = ''
	for node in doneList:
		doneString += node.name
	statusString += doneString

	print(statusString % currSec)


def addJob(jobList, node):
	for job in jobList:
		if not job:
			job = node


def findWorkTime(graph):
	numWorkers = 5

	doneList = list()
	jobList = [None] * numWorkers
	jobTimeList = [-1] * numWorkers
	availableList = list()
	unavailableList = list()

	# Populate available and unavailable list
	for name, node in graph.nodes.items():
		if not node.getParents():
			availableList.append(node)
		else:
			unavailableList.append(node)

	# Print header
	print("Second  W1  W2  W3  W4  W5  Done")
	#print("Second  W1  W2  Done")

	currSec = 0
	allDone = False
	while not allDone:
		# Clear finished jobs
		# and count down remaining time
		for ind, job in enumerate(jobList):
			if job: 
				if jobTimeList[ind] < 1:
					# Job done
					doneList.append(job)

					# Move children to active
					# if no other parent
					for child in job.getChildren():
						child.removeParent(job)

						# Add to active list if no parents
						if not child.getParents():
							availableList.append(child)
							unavailableList.remove(child)

					jobList[ind] = None

				else:
					jobTimeList[ind] -= 1

		# Sort list of available work
		availableList.sort(key=lambda k: k.name)

		# Check if workers available
		# and if so add jobs
		for ind, job in enumerate(jobList):
			# Add job if available
			if not job and availableList:
				jobNode = availableList[0]
				jobList[ind] = jobNode
				jobTimeList[ind] = jobNode.getWorkTime()
				availableList.remove(jobNode)
				

		# Print current state
		printCurrentState(currSec, jobList, doneList)

		currSec += 1

		# Check if done
		if not unavailableList and not availableList: 
			allDone = True

			for job in jobList:
				if job:
					allDone = False

	return currSec - 1


def partTwo():
	relationships = parseFile("input.txt")
	#print(relationships)

	graph = createGraph(relationships)
	#print(graph)

	workTime = findWorkTime(graph)
	print("Total work time: %d" % workTime)

'''
Main
'''
if __name__ == '__main__':
	partTwo()