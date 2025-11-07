import re
import numpy as np

class ResevoirMap:
    def __init__(self, map_data):
        # Find map dimensions
        dim = [[500, 500], [0, 0]]
        for line in map_data:
            for i in range(2):
                if len(line[i]) == 1:
                    # Single value
                    if line[i][0] < dim[i][0]:
                        dim[i][0] = line[i][0]
                    elif line[i][0] > dim[i][1]:
                        dim[i][1] = line[i][0]
                else:
                    # List
                    if line[i][0] < dim[i][0]:
                        dim[i][0] = line[i][0]
                    elif line[i][1] > dim[i][1]:
                        dim[i][1] = line[i][1]


        dim[0][0] -= 1
        dim[0][1] += 1

        # Create map
        self.start_coords = [dim[0][0], dim[1][0]]
        self.coords = np.zeros((dim[0][1] - dim[0][0] + 1, dim[1][1] + 1))

        # Add well
        self.setCoords([500, 0], -1)

        # Add clay
        for line in map_data:
            for x in line[0]:
                for y in line[1]:
                    self.setCoords([x,y], 1)

        print(self)

        self.water_edge = list()
        self.water_edge.append([500, 0])

    def __str__(self):      
        map_dim = self.coords.shape
        string = ""

        for y in range(map_dim[1]):
            for x in range(map_dim[0]):
                if self.coords[x, y] == 1:
                    string += "#"
                elif self.coords[x, y] == -1:
                    string += "+"
                else:
                    string += "."

            string += "\n"

        return string

    def stepWater(self):
        for coord in self.water_edge:
            coord_below = [coords[0], coords[1] + 1]
            if self.getCoords(coord_below) == 0:
                # Update water edge list
                self.water_edge.remove(coord)
                self.water_edge.append(coord_below)

    def getCoords(self, xy):
        return self.coords[xy[0] - self.start_coords[0], xy[1] - self.start_coords[1]]

    def setCoords(self, xy, value):
        self.coords[xy[0] - self.start_coords[0], xy[1] - self.start_coords[1]] = value