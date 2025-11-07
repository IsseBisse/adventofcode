# I felt like writing something I actually know

def get_data(path: str):
    with open(path) as file:
        text = file.read()

    workflow_string, parts_string = text.split("\n\n")
    return workflow_string, parts_string




def parse_workflows(string: str):
    def parse(string: str):

    
    workflows = {key: value for key, value in }
    print(string)


def part_one():
    workflow_string, parts_string = get_data("19/smallInput.txt")

    workflows = parse_workflows(workflow_string)
    # part

def part_two():
    pass


if __name__ == "__main__":
    part_one()
    # part_two()