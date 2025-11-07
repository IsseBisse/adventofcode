from Recipies import Recipes

'''
Part 1
'''
def partOne(number_of_recipies):
	input = [3, 7]
	recipies = Recipies(input)

	# Loop through recipies
	while len(recipies) < number_of_recipies + 10:
		recipies.createNewRecipe()
	#print(recipies)
	print(recipies.getScore(number_of_recipies, 10))

'''
Part 2
'''
def partTwo(score):
	input = [3, 7]
	recipes = Recipes(input)

	# Loop through until correct score
	current_recipe = 1
	current_score = 0
	while current_score != score:
		if len(recipes) < current_recipe + len(score):
			recipes.createNewRecipe()
		else:
			current_score = recipes.getScore(current_recipe, len(score))
			current_score = current_score[0:len(score)]
			#print("Current: %s. Given: %s" % (current_score, score))
			current_recipe += 1

	print("Number of recipies: %d" % (current_recipe - 1))


'''
Main
'''
if __name__ == '__main__':
	#partOne(286051)
	partTwo("286051")
	