class Node:
    def __init__(self, name):
        self.name = name
        self.children = list()
        self.parents = list()

    def __str__(self):
        nodeInformation = "Name: " + self.name

        # Loop through children
        nodeInformation = nodeInformation + ". Children: "
        for child in self.getChildren():
            nodeInformation = nodeInformation + child.name + " "

        # Loop through parents
        nodeInformation = nodeInformation + ". Parents: "
        for parent in self.getParents():
            nodeInformation = nodeInformation + parent.name + " "

        nodeInformation = nodeInformation

        return nodeInformation

    '''
    Manage children
    '''
    def addChild(self, node):
        self.children.append(node)

    def getChildren(self):
        return self.children

    '''
    Manage parents
    '''
    def addParent(self, node):
        self.parents.append(node)

    def removeParent(self, node):
        self.parents.remove(node)

    def getParents(self):
        return self.parents 

    '''
    Others
    '''
    def getWorkTime(self):
        return ord(self.name) - 5