from anytree import Node, RenderTree

def readInput(filename):
    f = open(filename, "r")

    data = list()
    for line in f:
        line = line.split("\n")[0]
        line = line.split(" -> ")

        node_information = dict()
        node_information["Children"] = list()

        parent_line = line[0].split(" ")
        node_information["ID"] = parent_line[0]
        node_information["Weight"] = parent_line[1][1:-1]

        if len(line) > 1:
            child_line = line[1].split(", ")
            for child_ID in child_line:
                node_information["Children"].append(child_ID)
            
        data.append(node_information)
        
    return data

'''
Part one
''' 
def printTree(root):
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))

def partOne():
    data = readInput("input.txt")

    all_nodes = dict()
    # Create all nodes
    for node_information in data:
        all_nodes[node_information["ID"]] = Node(node_information["ID"], weight=node_information["Weight"])

    # Attach nodes
    for node_information in data:
        parent = all_nodes[node_information["ID"]]

        # Get child nodes from dict and compile into a list
        children = list()
        for child_ID in node_information["Children"]:
            children.append(all_nodes[child_ID])

        # Attach children to parent
        parent.children = children

    #printTree(all_nodes[data[0]["ID"]].root)
    return all_nodes[data[0]["ID"]].root

'''
Part two
'''
def findUniqueWeight(weights):
    seen = {}
    duplicates = []

    # List duplicates
    for x in weights:
        if x not in seen:
            seen[x] = 1
        else:
            if seen[x] == 1:
                duplicates.append(x)
            seen[x] += 1

    # Find non-duplicate weight
    for i, weight in enumerate(weights):
        if weight not in duplicates:
            return i

def findIncorrectNode(node):
    if node.children:
        childrens_weight = list()

        for child in node.children:
            weight = getTotalWeight(child)
            childrens_weight.append(weight)
            print("%s %s, " % (child.name, weight), end="")
        print("")

        incorrect_index = findUniqueWeight(childrens_weight)
        incorrect_node = node.children[incorrect_index]

        findIncorrectNode(incorrect_node)

    else:
        print(node)

def getTotalWeight(node):
    childrens_weight = 0

    for child in node.children:
        childrens_weight += getTotalWeight(child)

    return childrens_weight + int(node.weight) 

def partTwo(root):
    print(root)
    findIncorrectNode(root)


if __name__ == '__main__':
    root = partOne()
    #print(root)  
    partTwo(root)  