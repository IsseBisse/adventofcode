import numpy as np
from re import findall
import matplotlib.pyplot as plt
from combinations import get_combinations

def get_data(path):
    with open(path) as file:
        data = file.read().split("\n")

    return data

def parse_data(data):
    ingredients = list()
    properties = list()
    for line in data:
        ingredients.append(line.split(":")[0])
        properties.append([int(match) for match in findall(r"[-0-9]+", line)])

    properties = np.array(properties)

    return ingredients, properties

def special_subset_sum(numbers, target, num_terms, partial=[], partial_sum=0):
    if partial_sum == target and len(partial) == num_terms:
        yield partial
    
    if partial_sum >= target or len(partial) > num_terms:
        return
    
    for i, n in enumerate(numbers):
        remaining = numbers[i + 1:]
        yield from special_subset_sum(remaining, target, num_terms, partial + [n], partial_sum + n)

def calculate_score(properties, combination):
    # Combine properties
    combination = np.array(combination)
    combined_properties = np.matmul(combination.T, properties)
    
    # Property must be >0
    combined_properties = np.maximum(np.zeros(combined_properties.shape), combined_properties)
    score = np.prod(combined_properties[:4])
    return score

def calculate_score_with_calories(properties, combination, required_calories):
    # Combine properties
    combination = np.array(combination)
    combined_properties = np.matmul(combination.T, properties)
    
    # Property must be >0
    combined_properties = np.maximum(np.zeros(combined_properties.shape), combined_properties)
    score = np.prod(combined_properties[:4])
    score = score if combined_properties[4] == required_calories else 0
    return score

def part_one():
    data = get_data("input.txt")
    ingredients, properties = parse_data(data)

    possible_terms = list(range(101)) * len(ingredients) 
    ingredient_combinations = special_subset_sum(list(range(1, 100)) + list(range(1, 100)), 100, len(ingredients))
    scores = list()
    for combination in ingredient_combinations:
        score = calculate_score(properties, combination)
        scores.append((score, combination))

    scores.sort(key=lambda x:x[0])
    print(scores[-1])
    print(ingredients)

def part_two():
    data = get_data("input.txt")
    ingredients, properties = parse_data(data)

    if len(ingredients) == 2:
        possible_terms = list(range(101)) * len(ingredients) 
        ingredient_combinations = special_subset_sum(list(range(1, 100)) + list(range(1, 100)), 100, len(ingredients))
    else:
        ingredient_combinations = get_combinations()

    scores = list()
    for combination in ingredient_combinations:
        score = calculate_score_with_calories(properties, combination, 500)
        scores.append((score, combination))

    scores.sort(key=lambda x:x[0])
    print(calculate_score_with_calories(properties, (46, 14, 30, 10), 500))
    print(scores[-1])
    print(ingredients)


if __name__ == '__main__':
    # part_one()
    part_two()