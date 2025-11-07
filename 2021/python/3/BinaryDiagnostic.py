from math import floor

def get_data(path):
    with open(path) as file:
        data = file.read().split("\n")

    return data

def parse_data(data):
    return [[int(char) for char in line] for line in data]

def inverse(binary_string):
    inverse_string = ["1" if char == "0" else "0" for char in binary_string]
    return "".join(inverse_string)  

def get_gamma(diagnostics):
    half_numbers = floor(len(diagnostics) / 2)
    gamma = list()
    for i in range(len(diagnostics[0])):
        num_positive = sum([line[i] for line in diagnostics])
        gamma.append(1 if num_positive > half_numbers else 0)

    gamma = "".join([str(bit) for bit in gamma])
    return gamma
        
def part_one():
    data = get_data("input.txt")
    diagnostics = parse_data(data)

    gamma = get_gamma(diagnostics)
    epsilon = inverse(gamma)

    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)

    print(gamma * epsilon)
    
def select_diagnostics(diagnostics, bit_ind, most_common=True):
    num_ones = sum([line[bit_ind] for line in diagnostics])
    num_zeros = len(diagnostics) - num_ones

    # This could probably be simplified
    if most_common:
        selective_bit = 1 if num_ones >= num_zeros else 0

    else:
        selective_bit = 0 if num_zeros <= num_ones else 1

    selected_diagnostics = list()
    for diag in diagnostics:
        if diag[bit_ind] == selective_bit:
            selected_diagnostics.append(diag)

    return selected_diagnostics

def find_rating(diagnostics, most_common=True):
    selected_diagnostics = diagnostics
    for bit_ind in range(len(diagnostics[0])):
        selected_diagnostics = select_diagnostics(selected_diagnostics, bit_ind, most_common=most_common)

        if len(selected_diagnostics) == 1:
            break

    return "".join([str(num) for num in selected_diagnostics[0]])

def part_two():
    data = get_data("input.txt")
    diagnostics = parse_data(data)

    oxygen_rating = find_rating(diagnostics)
    scrubber_rating = find_rating(diagnostics, most_common=False)

    oxygen_rating = int(oxygen_rating, 2)
    scrubber_rating = int(scrubber_rating, 2)

    print(oxygen_rating * scrubber_rating)

if __name__ == '__main__':
    part_one()
    part_two()