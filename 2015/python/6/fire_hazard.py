import re
import numpy as np
import matplotlib.pyplot as plt

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data[:-1]

def parse_data(raw_data):

	# Parse data
	data = list()
	for entry in raw_data:
		indicies = re.findall(r"[0-9]+", entry)
		status = re.findall(r"[a-z ]+", entry)[0][:-1]
		
		data.append({"status": status,
			"x_dim": (int(indicies[0]), int(indicies[2])+1),
			"y_dim": (int(indicies[1]), int(indicies[3])+1)})

	return data

def update_lights(lights, instr):

	status = instr["status"]
	x_dim = instr["x_dim"]
	y_dim = instr["y_dim"]

	if instr["status"] == "turn on":
		lights[x_dim[0]:x_dim[1], y_dim[0]:y_dim[1]] = 1

	elif instr["status"] == "turn off":
		lights[x_dim[0]:x_dim[1], y_dim[0]:y_dim[1]] = 0

	elif instr["status"] == "toggle":
		lights[x_dim[0]:x_dim[1], y_dim[0]:y_dim[1]] = np.invert(lights[x_dim[0]:x_dim[1], y_dim[0]:y_dim[1]])

	return lights

def part_one():
	raw_data = get_data("input.txt")
	data = parse_data(raw_data)

	lights = np.zeros((1000, 1000), dtype=bool)
	for entry in data:
		lights = update_lights(lights, entry)

	plt.imshow(lights)
	plt.show()
	print("Number of lit lights: %d" % np.count_nonzero(lights))
	

def turn_off(light):
	return max(light-1, 0)

vturn_off = np.vectorize(turn_off)

def new_update_lights(lights, instr):

	status = instr["status"]
	x_dim = instr["x_dim"]
	y_dim = instr["y_dim"]

	if instr["status"] == "turn on":
		lights[x_dim[0]:x_dim[1], y_dim[0]:y_dim[1]] += 1

	elif instr["status"] == "turn off":
		lights[x_dim[0]:x_dim[1], y_dim[0]:y_dim[1]] = vturn_off(lights[x_dim[0]:x_dim[1], y_dim[0]:y_dim[1]])

	elif instr["status"] == "toggle":
		lights[x_dim[0]:x_dim[1], y_dim[0]:y_dim[1]] += 2

	return lights

def part_two():
	raw_data = get_data("input.txt")
	data = parse_data(raw_data)

	lights = np.zeros((1000, 1000), dtype=int)
	for entry in data:
		lights = new_update_lights(lights, entry)

	print(type(lights))

	plt.imshow(lights)
	plt.show()
	print("Brightness: %d" % np.sum(lights))

if __name__ == '__main__':
	#part_one()
	part_two()