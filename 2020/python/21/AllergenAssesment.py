import itertools
import re

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	for i, line in enumerate(data):
		ingredients = re.findall(r"[a-z]+", line.split(" (")[0])
		allergens = re.findall(r"[a-z]+", line.split(" (contains")[1])
		data[i] = (ingredients, allergens)

	return data

def part_one():
	all_foods = get_data("input.txt")
	all_ingredients = set(itertools.chain.from_iterable([food[0] for food in all_foods]))
	all_allergens = set(itertools.chain.from_iterable([food[1] for food in all_foods]))
	
	possible_ingredients_per_allergen = dict()
	for allergen in all_allergens:
		may_contain = None

		for food in all_foods:
			food_ingredients = food[0]
			food_allergens = food[1]

			if allergen in food_allergens:
				if may_contain is None:
					may_contain = set(food_ingredients)

				else:
					may_contain = may_contain.intersection(set(food_ingredients))

		possible_ingredients_per_allergen[allergen] = may_contain


	possible_allergenic_ingredients = set.union(*[value for _, value in possible_ingredients_per_allergen.items()])
	no_possible_allergens = all_ingredients.difference(possible_allergenic_ingredients)


	print("Ingredients: %s" % all_ingredients)
	print("Allergens: %s" % all_allergens)
	print(possible_ingredients_per_allergen)
	print("May contain allergen: %s" % possible_allergenic_ingredients)
	print("May not contain allergen: %s" % no_possible_allergens)

	num_occurances = 0
	for food in all_foods:
		num_occurances += len(no_possible_allergens.intersection(set(food[0])))

	print("Non allergenic ingredients %d times in all foods" % num_occurances)

def part_two():
	all_foods = get_data("input.txt")
	all_ingredients = set(itertools.chain.from_iterable([food[0] for food in all_foods]))
	all_allergens = set(itertools.chain.from_iterable([food[1] for food in all_foods]))
	
	possible_ingredients_per_allergen = dict()
	for allergen in all_allergens:
		may_contain = None

		for food in all_foods:
			food_ingredients = food[0]
			food_allergens = food[1]

			if allergen in food_allergens:
				if may_contain is None:
					may_contain = set(food_ingredients)

				else:
					may_contain = may_contain.intersection(set(food_ingredients))

		possible_ingredients_per_allergen[allergen] = may_contain

	allergenic_ingredients = list()
	while possible_ingredients_per_allergen:
		print(possible_ingredients_per_allergen)

		for allergen, ingredients in possible_ingredients_per_allergen.items():
			if len(ingredients) == 1:
				ingredient = list(ingredients)[0]
				allergenic_ingredients.append((ingredient, allergen))
 
				del possible_ingredients_per_allergen[allergen]
				break

		# Remove ingredient from all other allergens
		for allergen, ingredients in possible_ingredients_per_allergen.items():
			possible_ingredients_per_allergen[allergen] = ingredients.difference(set([ingredient]))

	sorted_allergenic_ingredients = sorted(allergenic_ingredients, key=lambda tup:tup[1])
	print(sorted_allergenic_ingredients)
	ingredients_string = ",".join([tup[0] for tup in sorted_allergenic_ingredients])
	print(ingredients_string)


if __name__ == '__main__':
	#part_one()
	part_two()