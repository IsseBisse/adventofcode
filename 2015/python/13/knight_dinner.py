from re import findall
from itertools import permutations

def get_data(path):
    with open(path) as file:
        data = file.read().split("\n")

    return data

def calculate_happiness(seating_configuration, happiness_dict):
    happiness = 0
    for i, attendant in enumerate(seating_configuration):
        next_attendant = seating_configuration[(i+1) % len(seating_configuration)]
        
        happiness += happiness_dict[attendant][next_attendant]
        happiness += happiness_dict[next_attendant][attendant]

    return happiness

def parse_data(data):
    attendants = set([[parts for parts in line.split(" ")][0] for line in data])
    
    happiness_dict = {attendant: dict() for attendant in attendants}
    for line in data:
        receiver = line.split(" ")[0]
        giver = line.split(" ")[-1][:-1]
        happiness_factor = 1 if "gain" in line else -1
        happiness = int(findall(r"[0-9]+", line)[0]) * happiness_factor

        happiness_dict[receiver][giver] = happiness

    return attendants, happiness_dict

def part_one():
    data = get_data("input.txt")
    attendants, happiness_dict = parse_data(data)
    
    seating_configurations = permutations(attendants)
    configuration_happiness = list()
    for conf in seating_configurations:
        configuration_happiness.append((calculate_happiness(conf, happiness_dict), conf))
    
    configuration_happiness.sort(key=lambda x:x[0])
    print(configuration_happiness[-1])


def part_two():
    data = get_data("input.txt")
    attendants, happiness_dict = parse_data(data)
    
    myself = "Myself"
    for key in happiness_dict:
        happiness_dict[key][myself] = 0
    happiness_dict[myself] = {attendant: 0 for attendant in attendants}
    attendants.add(myself)

    seating_configurations = permutations(attendants)
    configuration_happiness = list()
    for conf in seating_configurations:
        configuration_happiness.append((calculate_happiness(conf, happiness_dict), conf))
    
    configuration_happiness.sort(key=lambda x:x[0])
    print(configuration_happiness[-1])

if __name__ == '__main__':
    #part_one()
    part_two()