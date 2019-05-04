import sys

import numpy as np
from ShaderProgram import ShaderProgram
from loader import Map
import time
import math


class Object:
    color1 = [0.0, 1.0, 0.0, 0.0]
    color2 = [1.0, 0.0, 0.0, 0.0]

    def __init__(self):
        self.vertices = list()
        self.colors = list()

    def generate_object(self):
        map = Map()
        self.minimum_value, self.maximum_value, self.map_matrix = map.get_map(use_script=False, image="crater3")

        self.width = len(self.map_matrix)
        self.height = len(self.map_matrix[0])
        self.depth = self.maximum_value - self.minimum_value

        self.vertex_count = self.width * self.height * 2

        self.image_diagonal = math.sqrt((self.width ** 2) + (self.height ** 2))

        self.generate_vertices()

        self.object_center_x = self.width / 2
        self.object_center_y = self.height / 2
        self.object_center_z = self.depth / 2

        return self.colors, self.vertices

    def move(self, translation_vector):
        self.object_center_x += translation_vector[0]
        self.object_center_y += translation_vector[1]
        self.object_center_z += translation_vector[2]

    def scale(self, scale_vector):
        self.width *= scale_vector[0]
        self.height *= scale_vector[1]
        self.depth *= scale_vector[2]

    def generate_vertices(self):
        for i in range(len(self.map_matrix)):
            for j in range(len(self.map_matrix[i])):
                x_coordinate = i
                y_coordinate = j
                z_coordinate = self.map_matrix[i][j]

                self.add_square(x_coordinate, y_coordinate, z_coordinate)

        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.colors = np.array(self.colors, dtype=np.float32)

    def add_square(self, x_coordinate, y_coordinate, z_coordinate):
        # Add triangle 1
        self.vertices.extend([float(x_coordinate), float(y_coordinate), z_coordinate, 1.0])
        self.vertices.extend([float(x_coordinate + 1.0), float(y_coordinate), z_coordinate, 1.0])
        self.vertices.extend([float(x_coordinate), float(y_coordinate + 1.0), z_coordinate, 1.0])

        self.colors.extend(self.color1)
        self.colors.extend(self.color1)
        self.colors.extend(self.color1)

        # Add triangle 2
        self.vertices.extend([float(x_coordinate + 1.0), float(y_coordinate), z_coordinate, 1.0])
        self.vertices.extend([float(x_coordinate + 1.0),
                              float(y_coordinate + 1.0),
                              z_coordinate, 1.0])

        self.vertices.extend([float(x_coordinate), float(y_coordinate + 1.0), z_coordinate, 1.0])

        self.colors.extend(self.color2)
        self.colors.extend(self.color2)
        self.colors.extend(self.color2)
