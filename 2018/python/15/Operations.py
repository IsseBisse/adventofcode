def testAllFunctions(input_register, output_register, opcode):
	matches = [False] * len(functions)

	for i, func in enumerate(functions):
		output = func(input_register.copy(), opcode[1], opcode[2], opcode[3])
		matches[i] = output == output_register

	ok_functions = list()
	for i, match in enumerate(matches):
		if match:
			ok_functions.append(functions[i].__name__)

	return ok_functions

'''
Addition
'''
def addr(register, A, B, C):
	register[C] = register[A] + register[B]
	return register

def addi(register, A, B, C):
	register[C] = register[A] + B
	return register

'''
Mutliplication
'''
def mulr(register, A, B, C):
	register[C] = register[A] * register[B]
	return register

def muli(register, A, B, C):
	register[C] = register[A] * B
	return register

'''
Bitwise AND
'''
def banr(register, A, B, C):
	register[C] = register[A] & register[B]
	return register

def bani(register, A, B, C):
	register[C] = register[A] & B
	return register

'''
Bitwise OR
'''
def borr(register, A, B, C):
	register[C] = register[A] | register[B]
	return register

def bori(register, A, B, C):
	register[C] = register[A] | B
	return register

'''
Assignment
'''
def setr(register, A, B, C):
	register[C] = register[A]
	return register

def seti(register, A, B, C):
	register[C] = A
	return register

'''
Greater-than testing
'''
def gtir(register, A, B, C):
	register[C] = int(A > register[B])
	return register

def gtri(register, A, B, C):
	register[C] = int(register[A] > B)
	return register

def gtrr(register, A, B, C):
	register[C] = int(register[A] > register[B])
	return register

'''
Equality testing
'''
def eqir(register, A, B, C):
	register[C] = int(A == register[B])
	return register

def eqri(register, A, B, C):
	register[C] = int(register[A] == B)
	return register

def eqrr(register, A, B, C):
	register[C] = int(register[A] == register[B])
	return register

functions = [addr, addi, mulr,  muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]