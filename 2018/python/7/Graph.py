from Node import Node

class Graph:
    def __init__(self, nodeNames, relationships):
        # Add all nodes
        self.nodes = dict()
        for name in nodeNames:
            self.nodes[name] = Node(name)

        # Update relationships
        self.updateRelationships(relationships)

        '''
        # Create start and end nodes
        self.start = Node("start")
        self.end = Node("end")

        # Attach start and end
        for name, node in self.nodes.items():
            # Attach nodes without parent to start
            if not node.getParents():
                node.addParent(self.start)

            # Attach nodes without child to end
            if not node.getChildren():
                node.addChild(self.end)
        '''


    def __str__(self):
        information = "=== Nodes === \n"

        # Loop through nodes
        for name, node in self.nodes.items():
            nodeInformation = str(node)

            information = information + nodeInformation + "\n"

        return information


    def updateRelationships(self, relationships):
        for relation in relationships:
            # Add child
            self.nodes[relation["parent"]].addChild(self.nodes[relation["child"]])

            # Add parent
            self.nodes[relation["child"]].addParent(self.nodes[relation["parent"]])
