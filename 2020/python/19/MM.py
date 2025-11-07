import re

"""
Data parsing
"""


def get_data(path):
    with open(path) as file:
        file_parts = file.read().split("\n\n")
        rules_data = file_parts[0].split("\n")
        received_messages = file_parts[1].split("\n")

    return rules_data, received_messages


def parse_rule_set(string):
    rule_set = string.split(" ")
    rule_set = list(map(int, rule_set))
    return rule_set


def parse_rule(string):
    rule = re.findall(r"[0-9]+: (.+)", string)[0]
    if re.findall(r"[a-z]+", rule):
        return rule[1:-1]

    else:
        first_level_split = rule.split(" | ")
        second_level_split = list(map(parse_rule_set, first_level_split))
        return second_level_split


def rule_sorter(string):
    return int(re.findall(r"^[0-9]+", string)[0])


"""
Node class
"""


class RuleNode:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Node with value {self.value}"

    def add_children(self, children):
        self.children = children

    def has_value(self):
        return self.value is not None

    def get_value(self):
        return self.value

    def generate_value(self):
        if self.has_value():
            return True

        children_strings = list()
        for sub_children in self.children:

            sub_children_strings = list()
            for child in sub_children:
                if child.has_value():
                    sub_children_strings.append(child.get_value())

                else:
                    return False

            children_strings.append("".join(sub_children_strings))

        self.value = "(%s)" % "|".join(children_strings)
        return True

    # # TODO: flip this upside down (i.e. start from node with only chars)
    # def get_regex(self):
    # 	if self.value is not None:
    # 		return self.value

    # 	else:
    # 		substrings = list()
    # 		for sub_children in self.children:
    # 			substrings.append("".join([child.get_regex() for child in sub_children]))

    # 		return "(%s)" % "|".join(substrings)

    @staticmethod
    def generate_children(rule_nodes, rule):
        children = list()
        for i, outer_rule in enumerate(rule):
            sub_children = list()

            for j, inner_rule in enumerate(outer_rule):
                sub_children.append(rule_nodes[inner_rule])

            children.append(sub_children)

        return children


def pattern_matcher(pattern):
    def match_pattern(string):
        return re.search(pattern, string) is not None

    return match_pattern


def part_one(path):
    rules_string, received_messages = get_data(path)
    rules_string.sort(key=rule_sorter)
    parsed_rules = list(map(parse_rule, rules_string))

    # Create rule nodes
    rule_nodes = list()
    for rule in parsed_rules:
        value = rule if isinstance(rule, str) else None
        node = RuleNode(value)
        rule_nodes.append(node)

    # Add children to rule nodes
    for i, rule in enumerate(parsed_rules):
        if not isinstance(rule, str):
            children = RuleNode.generate_children(rule_nodes, rule)
            rule_nodes[i].add_children(children)

    # Generate pattern
    all_values_set = False
    has_value = [False] * len(rule_nodes)
    while not all_values_set:
        for i, node in enumerate(rule_nodes):
            has_value[i] = node.generate_value()

        print("%d of %d has value" % (sum(has_value), len(rule_nodes)))
        all_values_set = all(has_value)

    # Filter messages
    pattern = "^%s$" % rule_nodes[0].get_value()
    matcher = pattern_matcher(pattern)
    correct_messages = filter(matcher, received_messages)

    print(len(list(correct_messages)))


def part_two():
    part_one("manualLooping_mediumInput.txt")


if __name__ == '__main__':
    # part_one("input.txt")
    part_two()