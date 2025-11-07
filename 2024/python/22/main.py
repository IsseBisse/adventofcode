def get_data(path: str) -> list[int]:
    with open(path) as file:
        data = file.read().split("\n")

    numbers = [int(row) for row in data]

    return numbers


def mix(first: int, second: int) -> int:
    return first ^ second


def prune(number: int) -> int:
    mod = 16777216
    return number % mod


def next_secret(secret: int) -> int:
    first = secret * 64
    first = mix(first, secret)
    secret = prune(first)

    second = secret // 32
    second = mix(second, secret)
    secret = prune(second)

    third = secret * 2048
    third = mix(third, secret)
    secret = prune(third)

    return secret


def part_one():
    secrets = get_data("22/input.txt")

    secrets_sum = 0
    num_laps = 2000
    for secret in secrets:
        for _ in range(num_laps):
            secret = next_secret(secret)

        secrets_sum += secret

    print(secrets_sum)


def ones(number: int) -> int:
    return number % 10


def get_sequences(change: list[tuple[int, int]]) -> dict[str, int]:
    window_size = 4
    sequences = dict()
    for idx in range(len(change) - window_size + 1):
        sequence = change[idx : idx + window_size]
        sequence_key = ",".join(str(num[0]) for num in sequence)
        price = sequence[-1][1]

        if sequence_key not in sequences:
            sequences[sequence_key] = price

    return sequences


def part_two():
    secrets = get_data("22/input.txt")

    changes = list()
    num_laps = 2000
    for secret in secrets:
        change = list()
        for _ in range(num_laps):
            new_secret = next_secret(secret)
            diff = ones(new_secret) - ones(secret)
            change.append((diff, ones(new_secret)))
            secret = new_secret

        changes.append(change)

    sequences = [get_sequences(change) for change in changes]
    all_keys = {sequence_key for sequence in sequences for sequence_key in sequence}
    best_key = ""
    best_price = 0
    for key in all_keys:
        total_price = sum(sequence.get(key, 0) for sequence in sequences)

        if total_price > best_price:
            best_key = key
            best_price = total_price

    print(best_key, best_price)


if __name__ == "__main__":
    # part_one()
    part_two()
