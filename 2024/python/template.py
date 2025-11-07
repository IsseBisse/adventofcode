def get_data(path):
    with open(path) as file:
        data = file.read().split("\n")

    return data


def part_one():
    _ = get_data("smallInput.txt")


def part_two():
    _ = get_data("smallInput.txt")


if __name__ == "__main__":
    part_one()
    part_two()
