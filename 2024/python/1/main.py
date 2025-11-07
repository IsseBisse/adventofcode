from collections import Counter


def get_data(path):
    with open(path) as file:
        data = file.read().split("\n")

    return data


def parse(data):
    pairs = [[int(value) for value in row.split("   ")] for row in data]
    columns = zip(*pairs)
    number_lists = [sorted(numbers) for numbers in columns]
    return number_lists


def part_one():
    data = get_data("1/input.txt")
    left, right = parse(data)
    diff = [abs(l_num - r_num) for l_num, r_num in zip(left, right)]
    print(sum(diff))


def part_two():
    data = get_data("1/input.txt")
    left, right = parse(data)

    occurance = Counter(right)
    score = [num * occurance[num] for num in left]
    print(sum(score))


if __name__ == "__main__":
    part_one()
    part_two()
