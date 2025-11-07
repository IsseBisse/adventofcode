import re
import copy

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	processed_data = list()
	for entry in data:
		parts = entry.split(" = ")
		processed_data.append((parts[0], parts[1]))

	return processed_data

class Program:
	def __init__(self):
		self.mem = dict()
		self.mask = "X" * 36

	def process_command(self, line):
		if "mask" in line[0]:
			self.set_mask(line[1])

		elif "mem" in line[0]:
			ind = int(re.findall(r"\[(\d+)\]", line[0])[0])
			self.set_mem(ind, int(line[1]))

	def run(self, code):
		for line in code:
			self.process_command(line)

	def set_mask(self, value):
		self.mask = value
		print("Mask %s" % value)

	def mask_value(self, value):
		value = [bit for bit in "{0:036b}".format(value)]
		
		for i, char in enumerate(self.mask):
			if char == "1":
				value[i] = "1"
			
			elif char == "0":
				value[i] = "0"

		value = "".join(value)
		return int(value, 2)

	def set_mem(self, ind, value):
		self.mem[ind] = self.mask_value(value)

		print("Mem[%d] %s" % (ind, self.mask_value(value)))

	def sum_mem(self):
		mem_sum = 0
		for key in self.mem:
			mem_sum += self.mem[key]

		return mem_sum

def part_one():
	data = get_data("input.txt")
	program = Program()

	program.run(data)
	print("Memory sum is %d" % program.sum_mem())

class AddressProgram:
	def __init__(self):
		self.mem = dict()
		self.mask = "X" * 36

	def process_command(self, line):
		if "mask" in line[0]:
			self.set_mask(line[1])

		elif "mem" in line[0]:
			ind = int(re.findall(r"\[(\d+)\]", line[0])[0])
			self.set_mem(ind, int(line[1]))

	def run(self, code):
		for line in code:
			self.process_command(line)

	def set_mask(self, value):
		self.mask = value
		print("Mask %s" % value)

	@staticmethod
	def get_address(address, bit_ind):
		if bit_ind == len(address):
			return [address]

		if address[bit_ind] == "X":
			address_one = copy.deepcopy(address)
			address_one[bit_ind] = "1"
			address_zero = copy.deepcopy(address)
			address_zero[bit_ind] = "0"

			return AddressProgram.get_address(address_one, bit_ind+1) + AddressProgram.get_address(address_zero, bit_ind+1)

		else:
			return AddressProgram.get_address(address, bit_ind+1) 

	def get_all_mem_addresses(self, ind):
		address = [bit for bit in "{0:036b}".format(ind)]
		for i, bit in enumerate(self.mask):
			if bit != "0":
				address[i] = bit

		print(address)

		addresses_bit = AddressProgram.get_address(address, 0)

		addresses_int = list()
		for addr in addresses_bit:
			addresses_int.append(int("".join(addr), 2)) 
		
		return addresses_int

	# def mask_value(self, value):
	# 	value = [bit for bit in "{0:036b}".format(value)]
		
	# 	for i, char in enumerate(self.mask):
	# 		if char == "1":
	# 			value[i] = "1"
			
	# 		elif char == "0":
	# 			value[i] = "0"

	# 	value = "".join(value)
	# 	return int(value, 2)

	def set_mem(self, ind, value):
		mem_addresses = self.get_all_mem_addresses(ind)
		print(mem_addresses)

		for addr in mem_addresses:
			self.mem[addr] = value
			print("Mem[%d] %s" % (addr, value))

	def sum_mem(self):
		mem_sum = 0
		for key in self.mem:
			mem_sum += self.mem[key]

		return mem_sum
	
def part_two():
	data = get_data("input.txt")
	program = AddressProgram()

	program.run(data)
	print("Memory sum is %d" % program.sum_mem())

if __name__ == '__main__':
	#part_one()
	part_two()