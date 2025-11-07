from collections import defaultdict
from functools import cache


def parse_wire(wire: str) -> tuple[str]:
    input_string, output = wire.split(" -> ")
    arg1, op, arg2 = input_string.split(" ")

    return (arg1, arg2, op, output)


def get_data(path: str) -> tuple[dict[str, int], list[tuple[str]]]:
    with open(path) as file:
        state_string, wire_string = (part.split("\n") for part in file.read().split("\n\n"))

    initial_states = dict()
    for row in state_string:
        key, value = row.split(": ")
        initial_states[key] = int(value)
    
    wires = tuple(parse_wire(wire) for wire in wire_string)

    return initial_states, wires


STR_TO_OP = {
    "AND": lambda arg1, arg2: arg1 and arg2,
    "OR": lambda arg1, arg2: arg1 or arg2,
    "XOR": lambda arg1, arg2: arg1 ^ arg2,
}


def bits_to_output(states: dict[str, int], prefix="z") -> int:
    output_states = [key for key in states if prefix in key]

    output = 0
    for key in output_states:
        exp = int(key[1:])
        output += states[key] * (2 ** exp)

    return output


def get_output(initial_states: dict[str, int], wires: list[tuple[str]]) -> int:
    states = initial_states.copy()

    unused_wires = set(wires)
    laps = 0
    while unused_wires:
        wire = unused_wires.pop()

        arg1_key, arg2_key, op_key, output_key = wire
        if arg1_key in states and arg2_key in states:
            op = STR_TO_OP[op_key]
            arg1 = states[arg1_key]
            arg2 = states[arg2_key]

            states[output_key] = op(arg1, arg2)

        else:
            unused_wires.add(wire)

        laps += 1
        if laps > len(wires) * 100:
            return None

    return bits_to_output(states)


def part_one():
    states, wires = get_data("24/input.txt")
    print(get_output(states, wires))


@cache
def get_dependencies(wires: tuple[tuple[str]]) -> dict[str, list[int]]:
    output_state_keys = [wire[-1] for wire in wires if "z" in wire[-1]]

    dependencies = dict()
    for key in output_state_keys:
        laps = 0
        dependent_idx = set()
        current_layers = {key}

        while current_layers:
            current_key = current_layers.pop()

            for idx, wire in enumerate(wires):
                if current_key == wire[-1]:
                    dependent_idx.add(idx)
                    current_layers.add(wire[0])                
                    current_layers.add(wire[1])

            laps += 1
            # For some reason len(wires) isn't enough...
            if laps > len(wires) * 100:
                # Wires contains a loop
                return            

        dependencies[key] = dependent_idx

    return dependencies


def swap(first: tuple[str], second: tuple[str]) -> tuple[tuple[str]]:
    new_first = first[:-1] + (second[-1],)
    new_second = second[:-1] + (first[-1],)

    return new_first, new_second


def rewire(wires: tuple[tuple[str]], first_idx: int, second_idx: int) -> tuple[tuple[str]]:
    new_wires = list(wires)

    first = new_wires[first_idx]
    second = new_wires[second_idx]

    new_first, new_second = swap(first, second)
        
    new_wires[first_idx] = new_first
    new_wires[second_idx] = new_second

    return tuple(new_wires)


def get_incorrect_output_keys(states: dict[str, int], wires: list[tuple[str]]) -> list[str]:
    # Get incorrect bits
    arg1 = bits_to_output(states, prefix="x")
    arg2 = bits_to_output(states, prefix="y")
    expected_output = f"{arg1 + arg2:b}"
    expected_output_state = {f"z{idx:02d}": value for idx, value in enumerate(reversed(expected_output))}

    states = get_output(states, wires)
    if states is None:
        return None

    output = f"{states:b}"
    output_state = {f"z{idx:02d}": value for idx, value in enumerate(reversed(output))}

    incorrect_output_keys = list()
    for key, expected_value in expected_output_state.items():
        if output_state.get(key, "0") != expected_value:
            incorrect_output_keys.append(key)

    return incorrect_output_keys


def try_rewire(states: dict[str, int], wires: tuple[tuple[str]], previous_incorrect_bits: int, swaps_left: int = 4) -> tuple[tuple[str]] | None:
    incorrect_output_keys = get_incorrect_output_keys(states, wires)
    if incorrect_output_keys is None:
        return
    
    print(swaps_left, len(incorrect_output_keys))

    if len(incorrect_output_keys) > previous_incorrect_bits:
        return

    if len(incorrect_output_keys) == 0:
        return wires
    
    if swaps_left == 0:
        return
    
    dependencies = get_dependencies(wires)
    if dependencies is None:
        return

    candidates = defaultdict(lambda: 0)
    for key in incorrect_output_keys:
        for dep in dependencies[key]:
            candidates[dep] += 1

    top_candidates = [cand[0] for cand in sorted(candidates.items(), key=lambda item: item[1], reverse=True)]
    new_wires = list()
    for first_idx, second_idx in zip(top_candidates[::2], top_candidates[1::2]):    
        new_wire = rewire(wires, first_idx, second_idx)
        new_incorrect_bits = get_incorrect_output_keys(states, new_wire)

        if new_incorrect_bits is not None:
            new_wires.append((new_wire, len(new_incorrect_bits)))

    top_new_wires = sorted(new_wires, key=lambda item: item[1])

    for new_wire, _ in top_new_wires:
        new_rewire = try_rewire(states, new_wire, len(incorrect_output_keys), swaps_left-1)

        if new_rewire is not None:
            return new_rewire


def part_two():
    states, wires = get_data("24/input.txt")
    new_rewire = try_rewire(states, wires, 1000)
    print(new_rewire)


if __name__ == "__main__":
    # part_one()
    part_two()
