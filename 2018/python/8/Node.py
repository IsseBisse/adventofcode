class Node:
    def __init__(self, name):
        # Variables
        self.name = name
        self.children = list()
        self.metadata = list()

    def __str__(self):
        string = self.name + " - "
        
        # Get metadata
        for data in self.metadata:
            string += "%d " % data

        # Get value
        string += " - "
        string += "%d" % self.getValue()
        string += "\n"

        # Print children
        for child in self.children:
            string += str(child)

        return string


    '''
    Filedata
    '''
    def eatFiledata(self, filedata):
        numChildren = filedata.pop(0)
        numMetadata = filedata.pop(0)

        for i in range(numChildren):
            child = Node("%s.%d" % (self.name, i))
            filedata = child.eatFiledata(filedata)

            self.children.append(child)

        for i in range(numMetadata):
            self.metadata.append(filedata.pop(0))

        return filedata

    '''
    Helpers
    '''
    def addMetadata(metadata):
        self.metadata = metadata

    def addChild(node):
        self.children.append(node)

    def getValue(self):
        value = 0

        if not self.children:
            value = sum(self.metadata)
        else:
            # Sum children specified by metadata
            for data in self.metadata:
                data -= 1

                if data < len(self.children):
                    value += self.children[data].getValue()

        #print(value)
        return value
            