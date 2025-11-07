from tqdm import tqdm


def get_data(string):
    cups = [int(char) for char in string]
    return cups


class CycleNode:
    def __init__(self, value):
        self.value = value
        self.next_node = None

    def __str__(self):
        string = f"({self.value})"
        next_node = self.next_node
        while next_node != self and next_node is not None:
            string += f", {next_node.value}"
            next_node = next_node.next_node

        return string

    def to_list(self):
        nodes = [self]
        next_node = self.next_node
        while next_node != self and next_node is not None:
            nodes.append(next_node)
            next_node = next_node.next_node

        return nodes

    def uncouple(self, num_nodes=3):
        removed = self.next_node
        self.next_node = self.next_node.next_node.next_node.next_node
        removed.next_node.next_node.next_node = None

        return removed

    def couple(self, node):
        node.next_node.next_node.next_node = self.next_node
        self.next_node = node


def move_faster(node, nodes):
    current = node
    uncoupled = current.uncouple()
    next_current = current.next_node

    # TODO: This could be quicker as well
    # coupled_nodes = current.to_list()
    # coupled_values = {node.value for node in coupled_nodes}
    # destination = None
    # target = current.value - 1
    # while destination is None:
    #     if target in coupled_values:
    #         destination = target
    #
    #     else:
    #         target -= 1
    #         if target < min(coupled_values):
    #             target = max(coupled_values)

    # Use zero-based numbering for easier wrap around
    destination_zero_based = (current.value - 1 - 1) % len(nodes)
    uncoupled_values = {node.value for node in uncoupled.to_list()}
    while destination_zero_based+1 in uncoupled_values:
        destination_zero_based = (destination_zero_based - 1) % len(nodes)
    destination = destination_zero_based + 1

    next_node = nodes[destination]
    next_node.couple(uncoupled)

    return next_current


def move(node):
    current = node
    # print(current)
    uncoupled = current.uncouple()
    next_current = current.next_node
    # print(uncoupled)
    # print(current)

    coupled_nodes = current.to_list()
    coupled_values = {node.value for node in coupled_nodes}
    destination = None
    target = current.value - 1
    while destination is None:
        if target in coupled_values:
            destination = target

        else:
            target -= 1
            if target < min(coupled_values):
                target = max(coupled_values)

    # print(destination)
    while current.value != destination:
        current = current.next_node

    current.couple(uncoupled)
    # print(current)
    # print()

    return next_current


def part_one():
    cups = get_data("389125467")
    # cups = get_data("186524973")
    cups = [CycleNode(value) for value in cups]
    for idx, node in enumerate(cups):
        node.next_node = cups[(idx + 1) % len(cups)]

    current = cups[0]
    num_moves = 100
    for _ in range(num_moves):
        current = move(current)

        # print(current)
        # print()

    print(current)
    while current.value != 1:
        current = current.next_node
    current = current.next_node

    values = (node.value for node in current.to_list())
    string = "".join(str(num) for num in values)
    print(string[:-1])


def part_two():
    # cups = get_data("389125467")
    cups = get_data("186524973")
    num_total_cups = int(1e6)
    cups += list(range(max(cups) + 1, num_total_cups+1))
    cups = [CycleNode(value) for value in cups]
    for idx, node in enumerate(cups):
        node.next_node = cups[(idx + 1) % len(cups)]

    current = cups[0]   # First cup
    cups_dict = {cup.value: cup for cup in cups}
    # states = {tuple(current.to_list())}
    num_moves = int(1e7)
    for turn in tqdm(range(num_moves)):
        current = move_faster(current, cups_dict)
        # state = tuple(current.to_list())
        # if state in states:
        #     print(turn)
        #     break
        # states.add(state)
    # return

    while current.value != 1:
        current = current.next_node

    print(current.next_node.value * current.next_node.next_node.value)


if __name__ == '__main__':
    # part_one()
    part_two()
