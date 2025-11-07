from itertools import product
from operator import add, mul


def get_data(path: str):
    with open(path) as file:
        data = file.read().split("\n")

    return data


def parse(row: str) -> tuple[int, list[int]]:
    target, terms = row.split(": ")

    target = int(target)
    terms = [int(term) for term in terms.split(" ")]

    return target, terms


def has_solution(target: int, terms: list[int], operators) -> bool:
    operator_permutations = product(operators, repeat=len(terms) - 1)

    for op_perm in operator_permutations:
        perm_sum = terms[0]
        for op, term in zip(op_perm, terms[1:]):
            perm_sum = op(perm_sum, term)

        if perm_sum == target:
            return True

    return False


def part_one():
    data = get_data("7/input.txt")

    equations = [parse(row) for row in data]
    operators = [add, mul]
    solvable_targets = [
        target for target, terms in equations if has_solution(target, terms, operators)
    ]

    print(sum(solvable_targets))


def concat(a, b):
    return int(f"{a}{b}")


def part_two():
    data = get_data("7/input.txt")

    equations = [parse(row) for row in data]
    operators = [add, mul, concat]
    solvable_targets = [
        target for target, terms in equations if has_solution(target, terms, operators)
    ]

    print(sum(solvable_targets))


if __name__ == "__main__":
    part_one()
    part_two()
