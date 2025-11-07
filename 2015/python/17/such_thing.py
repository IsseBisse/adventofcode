from itertools import chain, combinations

def powerset(iterable):
    """Stole powerset generator.

    https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def get_data(path):
    with open(path) as file:
        data = file.read().split("\n")

    return data

def parse_data(data):
    for i, entry in enumerate(data):
        data[i] = int(entry)

    return data
    
def find_possible_combinations(containers, store_volume):
    container_powerset = powerset(containers)
    
    correct_combinations = list()
    for comb in container_powerset:
        if sum(comb) == store_volume:
            correct_combinations.append(comb)

    return correct_combinations

def part_one():
    data = get_data("input.txt")
    containers = parse_data(data)

    store_volume = 150
    combinations = find_possible_combinations(containers, store_volume)
    
    # print(combinations)
    print(len(combinations))

def part_two():
    data = get_data("input.txt")
    containers = parse_data(data)

    store_volume = 150
    combinations = find_possible_combinations(containers, store_volume)
    
    min_combination_length = min([len(comb) for comb in combinations])
    num_min_length_combinations = sum([len(comb) == min_combination_length for comb in combinations])

    print(num_min_length_combinations)

if __name__ == '__main__':
    #part_one()
    part_two()