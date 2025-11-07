import numpy as np
import matplotlib.pyplot as plt

def parse_input(path):

	text = open(path, "r").read()
	text = text.split("\n")

	data = list()
	for line in text:
		parts = line.split(",")
		
		pos = [int(parts[0].split("=")[1]), int(parts[1].split("=")[1]), int(parts[2][:-1].split("=")[1])]
		data.append(pos)

	return data

class Moon():
	
	def __init__(self, pos):
		self.pos = pos
		self.vel = [0, 0, 0]

	def __str__(self):
		return "Moon at (%d, %d, %d) with velocity (%d, %d, %d)" % (self.pos[0], self.pos[1], self.pos[2], self.vel[0], self.vel[1], self.vel[2])

	def apply_gravity(self, other):
		for i in range(3):
			self.vel[i] += 2*int(self.pos[i] < other.pos[i]) + int(self.pos[i] == other.pos[i]) - 1

	def update_velocity(self, all_other):
		for other in all_other:
			self.apply_gravity(other)

	def update_position(self):
		for i in range(3):
			self.pos[i] += self.vel[i]

	def get_energy(self):
		pot = 0
		kin = 0
		for i in range(3):
			pot += abs(self.pos[i])
			kin += abs(self.vel[i])

		return pot * kin


def part_one():
	# Create data
	data = parse_input("testInput.txt")
	moons = list()
	for pos in data:
		moons.append(Moon(pos))

	# Print baseline
	print("After 0 steps:")
	for moon in moons:
		print(moon)
	print("")

	num_steps = 2772
	for i in range(num_steps):	
		# Update velocities and positions
		for moon in moons:
			moon.update_velocity(moons)
			
		for moon in moons:
			moon.update_position()

		'''
		print("After %d steps:" % (i+1))
		for moon in moons:
			print(moon)
		print("")
		'''

	print("After %d steps:" % (i+1))
	for moon in moons:
		print(moon)
	print("")

	total_energy = 0
	for moon in moons:
		total_energy += moon.get_energy()

	print("Total energy of the system is %d" % total_energy)

def find_repetition(signal):

	patch_len = 10
	offset = 0
	while True:
		if np.all(signal[:patch_len] == signal[patch_len+offset:2*patch_len+offset]):
			return offset + patch_len

		else:
			if patch_len < 1000:
				patch_len += 1

			else:
				offset += 1

		if 2*patch_len+offset > len(signal):
			return None

def primes(n):
    primfac = []
    d = 2
    while d*d <= n:
        while (n % d) == 0:
            primfac.append(d)  # supposing you want multiple factors repeated
            n //= d
        d += 1
    if n > 1:
       primfac.append(n)
    
    return primfac

def my_lcm(a, b):

	greater = a

	while (greater % b) != 0:
		greater += a

	return greater 

def part_two():
	
	data = parse_input("input.txt")
	data = np.array(data)

	calc_len = int(1e6)
	num_signals = 24
	velocity = np.zeros((data.shape[0], data.shape[1], calc_len))
	position = np.zeros((data.shape[0], data.shape[1], calc_len))
	signals = np.zeros((num_signals, calc_len))

	position[:,:,0] = data

	signals[0:12, 0] = np.reshape(data, 12)

	num_steps = calc_len - 1
	for j in range(num_steps):	
		for i in range(4):
			velocity[i,:,j+1] = velocity[i,:,j] + np.sum((position[i,:,j] < position[:,:,j]).astype(int) - (position[i,:,j] > position[:,:,j]).astype(int), axis=0)


		position[:,:,j+1] = position[:,:,j] + velocity[:,:,j+1]
		signals[0:12, j+1] = np.reshape(position[:,:,j+1], 12)
		signals[12:, j+1] = np.reshape(velocity[:,:,j+1], 12)

	# Find all periodicities
	periods = list()
	transients_fade = 5000
	for i in range(num_signals):
		# Let transients fade
		period = find_repetition(signals[i, transients_fade:])

		if period is None:
			print("No repetition found try collecting more samples!")
			break
		else:
			periods.append(period)

	'''
	start = 1000
	lenght = 10000
	end = start + lenght
	for i in range(num_signals):
		plt.subplot(6, 4, i+1)
		plt.plot(signals[i, start:end])
		
		for j in range(start, end, periods[i]):
			plt.plot([j, j], [min(signals[i,start:end]), max(signals[i,start:end])])

		plt.title("Period: %d" % periods[i])
	
	plt.tight_layout()
	plt.show()
	'''

	# All unique periods
	periods = list(set(periods))
	product = 1
	for period in periods:
		product *= period

	# Find LCM
	lcm = my_lcm(periods[0], periods[1])
	for period in periods[2:]:
		lcm = my_lcm(lcm, period)

	# Same state is reached in N steps
	# with N being lowest common multiple of periods
	print("They will reach the same state in %d steps" % lcm)
	
if __name__ == '__main__':
	#part_one()
	part_two()