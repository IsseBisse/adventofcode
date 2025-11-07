'''
Part One
'''
import hashlib

def partOne(data):
	password = ""
	
	ind = 0
	print("Looking for characters...")
	while len(password) < 8:
		string = data + str(ind)
		ind += 1

		result = hashlib.md5(string.encode())
		if result.hexdigest()[0:5] == "00000":
			password += result.hexdigest()[5]

			print("%d " % len(password), end="")

	print("Done! \n")
	print("Final password is %s" % password)

'''
Part Two
'''
def partTwo(data):
	password =  ["-"] * 8
	available = [True] * 8
	
	ind = 0
	print("Looking for characters...")
	while "-" in password:
		string = data + str(ind)
		ind += 1

		result = hashlib.md5(string.encode())
		# Check if correct start
		if result.hexdigest()[0:5] == "00000":
			char_ind = result.hexdigest()[5]

			# Check if character index is number
			if char_ind.isdigit():
				char_ind = int(char_ind)

				if char_ind < 8 and available[char_ind]:

					password[char_ind] = result.hexdigest()[6]
					available[char_ind] = False

					print("Password is %s " % "".join(password))

	print("Done! \n")
	print("Final password is %s" % "".join(password))

'''
Main
'''
if __name__ == '__main__':
	testData = "abc"
	data = "wtnhxymk"

	#partOne(data)
	partTwo(data)