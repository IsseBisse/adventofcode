import binascii

from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import reduce
from operator import mul
from typing import List

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data

def hex_to_bin(hex_string):
	return "".join([f"{int(char, 16):0>4b}" for char in hex_string])

def decode_literal(bin_string):
	parts = ""
	start = 0
	while True:
		sub_string = bin_string[start*5:(start+1)*5]
		parts += sub_string[1:]
		start += 1
		
		if sub_string[0] == "0":
			break

	return int(parts, 2), bin_string[start*5:]

@dataclass
class Packet(ABC):
	version: int
	type_id: int

	@abstractmethod
	def get_value(self):
		pass

@dataclass
class Literal(Packet):
	value: int

	def get_value(self):
		return self.value

@dataclass
class Operator(Packet):
	length_type_id: int
	length: int

	sub_packets: List

	def __post_init__(self):
		values = [packet.get_value() for packet in self.sub_packets]

		if self.type_id == 0:
			self.eval_value = sum(values)
		
		elif self.type_id == 1:
			self.eval_value = reduce(mul, values, 1)
		
		elif self.type_id == 2:
			self.eval_value = min(values)
		
		elif self.type_id == 3:
			self.eval_value = max(values)

		elif self.type_id == 5:
			self.eval_value = int(values[0] > values[1])

		elif self.type_id == 6:
			self.eval_value = int(values[0] < values[1])

		elif self.type_id == 7:
			self.eval_value = int(values[0] == values[1])
		

	def get_value(self):
		# NOTE: This requires bottom-up creation of packet hierarchy
		return self.eval_value

def decode_packet(bin_string):
	version = int(bin_string[:3], 2)
	type_id = int(bin_string[3:3+3], 2)

	if type_id == 4:
		# Literal packet
		value, rem = decode_literal(bin_string[6:])
		packet = [Literal(version, type_id, value)]
		
	else:
		# Operator packet
		length_type_id = int(bin_string[6], 2)
		if length_type_id == 0:
			# Num bits
			num_bits = int(bin_string[7:7+15], 2)
			sub_packet_string = bin_string[7+15:]

			bits_consumed = 0
			sub_packets = list()
			while bits_consumed < num_bits:
				packets, rem = decode_packet(sub_packet_string)
				bits_consumed += len(sub_packet_string) - len(rem)
				sub_packet_string = rem
				sub_packets += packets

			packet = [Operator(version, type_id, length_type_id, num_bits, sub_packets)]

		else: 
			# Num packets
			num_packets = int(bin_string[7:7+11], 2)
			sub_packet_string = bin_string[7+11:]

			sub_packets = list()
			for _ in range(num_packets):
				packets, rem = decode_packet(sub_packet_string)
				sub_packet_string = rem
				sub_packets += packets

			packet = [Operator(version, type_id, length_type_id, num_packets, sub_packets)]

	return packet, rem

def unpack(packets):
	packet_list = list()
	for packet in packets:
		if isinstance(packet, Literal):
			packet_list.append(packet)

		else:
			packet_list.append(packet)
			packet_list += unpack(packet.sub_packets)

	return packet_list

def part_one():
	hex_strings = get_data("input.txt")
	for string in hex_strings:
		print(string)
		bin_string = hex_to_bin(string)
		packets, rem = decode_packet(bin_string)
		print(packets)
		packet_list = unpack(packets)
		version_sum = sum([packet.version for packet in packet_list])
		print(version_sum)
		print("")

def part_two():
	hex_strings = get_data("input.txt")
	for string in hex_strings:
		bin_string = hex_to_bin(string)
		packets, rem = decode_packet(bin_string)
		print(packets[0].get_value())

if __name__ == '__main__':
	# part_one()
	part_two()