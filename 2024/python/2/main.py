def get_data(path):
    with open(path) as file:
        data = file.read().split("\n")

    return data


def parse(row):
    return [int(num) for num in row.split(" ")]


def is_safe(report):
    first_increasing = (report[1] - report[0]) > 0
    if not (1 <= abs(report[1] - report[0]) <= 3):
        return False

    for first, second in zip(report[1:-1], report[2:]):
        is_increaing = (second - first) > 0
        is_correct_diff = 1 <= abs(second - first) <= 3

        if first_increasing != is_increaing or not is_correct_diff:
            return False

    return True


def part_one():
    data = get_data("2/input.txt")
    reports = [parse(row) for row in data]
    safe_reports = filter(is_safe, reports)
    print(len(list(safe_reports)))


def permute(report):
    perm = [report]
    for idx in range(len(report)):
        new_report = [num for num in report]  # Copy
        del new_report[idx]
        perm.append(new_report)

    return perm


def part_two():
    data = get_data("2/input.txt")
    reports = [parse(row) for row in data]
    # This is innefficient as hell but good enough here
    permutations = [permute(report) for report in reports]
    safe_reports = filter(
        lambda perm: any(is_safe(report) for report in perm), permutations
    )
    print(len(list(safe_reports)))


if __name__ == "__main__":
    part_one()
    part_two()
