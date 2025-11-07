import math
import numpy as np
import re


def get_data(path):
	with open(path) as file:
		data = file.read()

	nums = [int(string) for string in re.findall(r"[\-0-9]+", data)] 

	x_pos = (nums[0], nums[1])
	y_pos = (nums[2], nums[3])

	return (x_pos, y_pos)

def one_step(pos, vel):
	pos += vel
	vel[0] = max(0, vel[0]-1)
	vel[1] -= 1

	return pos, vel

def part_one():
	x_pos, y_pos = get_data("input.txt")

	# y_v at y=0 will be -y0_v
	# So y0_v < y_min
	y_vel = -y_pos[0]-1
	# x0_v^2/2 must be within x_pos
	x_vel = math.floor((2*x_pos[1])**(1/2))
	max_vel = (x_vel, y_vel)

	pos = np.array([0, 0])
	vel = np.array(max_vel)
	hit_pos = None
	y_max = 0
	while pos[1] >= y_pos[0]:
		pos, vel = one_step(pos, vel)

		y_max = max(y_max, pos[1])
		if pos[0] in range(*x_pos) and pos[1] in range(*y_pos):
			hit_pos = pos.copy()

	print()
	print(hit_pos, y_max)

def get_x_min_vel(x_pos):
	x_min = 0
	while sum(range(x_min)) < x_pos[0]:
		x_min += 1

	return x_min-1

def is_hit_vel(init_vel, x_pos, y_pos):
	pos = np.array([0, 0])
	vel = np.array(init_vel)
	while pos[1] >= y_pos[0]:
		pos, vel = one_step(pos, vel)

		if pos[0] in range(x_pos[0], x_pos[1]+1) and pos[1] in range(y_pos[0], y_pos[1]+1):
			return True

	return False

def part_two():
	x_pos, y_pos = get_data("input.txt")

	y_min_vel = y_pos[0]
	y_max_vel = -y_pos[0]-1

	x_min_vel = get_x_min_vel(x_pos)
	x_max_vel = x_pos[1]

	good_vels = list()
	for x_vel in range(x_min_vel, x_max_vel+1):
		for y_vel in range(y_min_vel, y_max_vel+1):
			init_vel = (x_vel, y_vel)

			if is_hit_vel(init_vel, x_pos, y_pos):
				good_vels.append(init_vel)

	print(len(good_vels))

if __name__ == '__main__':
	# part_one()
	part_two()