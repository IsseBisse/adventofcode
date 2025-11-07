import math
import matplotlib.pyplot as plt
import time

import fractions

def countDivisors(n) :
    cnt = 0
    for i in range(1, (int)(math.sqrt(n)) + 1) :
        if (n % i == 0) :
             
            # If divisors are equal,
            # count only one
            if (n / i == i) :
                cnt = cnt + 1
            else : # Otherwise count both
                cnt = cnt + 2
                 
    return cnt

def get_divisors(n) :
    i = 1
    divisors = list()
    while i <= math.sqrt(n):          
        if (n % i == 0) :
            if (n / i == i) :
                divisors.append(i),
            else :
                divisors.append(i)
                divisors.append(int(n/i)),
        i = i + 1

    return divisors

def calculate_num_presents(house_number):
    divisors = get_divisors(house_number)
    num_presents = sum(divisors)
    return num_presents

def part_one():
    N = 29000000
    num_presents = [0] * int(N / 10)
    
    for elf in range(1, int(N/10)):
        for house_number in range(elf, int(N/10), elf):
            num_presents[house_number] += elf*10

    for house_number, num_presents in enumerate(num_presents):
        if num_presents > N:
            break

    print(house_number)

def part_two():
    N = 29000000
    num_presents = [0] * int(N / 10)
    
    for elf in range(1, int(N/10)):
        for house_number in range(elf, elf*51, elf):
            if house_number < len(num_presents):
                num_presents[house_number] += elf*11

    for house_number, num_presents in enumerate(num_presents):
        if num_presents > N:
            break

    print(house_number)

if __name__ == '__main__':
    #part_one()
    part_two()