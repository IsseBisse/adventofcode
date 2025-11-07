import networkx as nx
import matplotlib.pyplot as plt

def parse_input(path):

	f = open(path, "r")

	lines = [x for x in  f.read().split("\n")]

	graph = nx.DiGraph()
	graph.add_node("ORE")

	processes = list()
	for line in lines:
		parts = line.split(" => ")

		input_parts = parts[0].split(", ")
		input_ = list()
		for part in input_parts:
			part = part.split(" ")
			input_.append((int(part[0]), part[1]))

		output = parts[1].split(" ")
		output = (int(output[0]), output[1])

		processes.append((input_, output))

	for item in processes:
		output = item[1]
		graph.add_node(output[1])

	for item in processes:
		output = item[1]

		inputs = item[0]
		for input_ in inputs:
			graph.add_edge(input_[1], output[1])

	return graph

def part_one():
	graph = parse_input("testInput1.txt")
	
	print("Nodes of graph: ")
	print(graph.nodes())

	print("Edges of graph: ")
	print(graph.edges())

	nx.draw(graph, with_labels=True)
	plt.show()

def part_two():
	pass

if __name__ == '__main__':
	part_one()