import numpy as np
from loader import Map
import math


class Object:
    color1 = [0.1, 0.1, 0.1, 0.7]
    color2 = [1, 1, 1, 0.7]

    def __init__(self):
        self.vertices = list()
        self.colors = list()
        self.object_center_x = 0
        self.object_center_y = 0
        self.object_center_z = 0

    def generate_object(self, image_name):
        map = Map()
        self.minimum_value, self.maximum_value, self.map_matrix = map.get_map(use_script=False, image=image_name)

        self.width = len(self.map_matrix)
        self.height = len(self.map_matrix[0])

        diagonal = math.sqrt(self.width ** 2 + self.height ** 2)

        if self.maximum_value > diagonal:
            self.depth = self.maximum_value
        else:
            self.depth = diagonal

        self.vertex_count = self.width * self.height * 6

        self.generate_vertices()

        self.object_center_x = self.width / 2
        self.object_center_y = self.height / 2
        self.object_center_z = self.maximum_value / 2

        return self.colors, self.vertices

    def move(self, translation_vector):
        print(translation_vector)
        self.object_center_x += translation_vector[0]
        self.object_center_y += translation_vector[1]
        self.object_center_z += translation_vector[2]

    def scale(self, scale_vector):
        self.width *= scale_vector[0]
        self.height *= scale_vector[1]
        self.depth *= scale_vector[2]

    def generate_vertices(self):
        for i in range(self.width - 1):
            for j in range(self.height - 1):
                x_coordinate = i
                y_coordinate = j
                z_coordinate = self.normalize(self.map_matrix[i][j])

                neighbor1 = self.normalize(self.map_matrix[i + 1][j])
                neighbor2 = self.normalize(self.map_matrix[i][j + 1])
                neighbor3 = self.normalize(self.map_matrix[i + 1][j + 1])

                self.add_lines(x_coordinate, y_coordinate, z_coordinate, neighbor1, neighbor2, neighbor3)

        self.create_border_lines()

        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.colors = np.array(self.colors, dtype=np.float32)

    def create_border_lines(self):
        for i in range(self.width - 1):
            z_coordinate = self.normalize(self.map_matrix[i][self.height - 1])
            z_neighbor = self.normalize(self.map_matrix[i + 1][self.height - 1])

            self.vertices.extend([float(i), float(self.height - 1), z_coordinate, 1.0])
            self.vertices.extend([float(i + 1.0), float(self.height - 1), z_neighbor, 1.0])

        for j in range(self.height - 1):
            z_coordinate = self.normalize(self.map_matrix[self.width - 1][j])
            z_neighbor = self.normalize(self.map_matrix[self.width - 1][j + 1])

            self.vertices.extend([float(self.width - 1), float(j), z_coordinate, 1.0])
            self.vertices.extend([float(self.width - 1), float(j + 1.0), z_neighbor, 1.0])

    def normalize(self, value):
        return value

    def add_lines(self, x_coordinate, y_coordinate, z_coordinate, neighbor1, neighbor2, neighbor3):
        self.vertices.extend([float(x_coordinate), float(y_coordinate), z_coordinate, 1.0])
        self.vertices.extend([float(x_coordinate + 1.0), float(y_coordinate), neighbor1, 1.0])

        self.vertices.extend([float(x_coordinate), float(y_coordinate), z_coordinate, 1.0])
        self.vertices.extend([float(x_coordinate), float(y_coordinate + 1.0), neighbor2, 1.0])

        self.vertices.extend([float(x_coordinate), float(y_coordinate), z_coordinate, 1.0])
        self.vertices.extend([float(x_coordinate + 1.0), float(y_coordinate + 1.0), neighbor3, 1.0])

        self.colors.extend(self.color1)
        self.colors.extend(self.color1)
        self.colors.extend(self.color1)
        self.colors.extend(self.color1)
        self.colors.extend(self.color1)

    def add_triangles(self, x_coordinate, y_coordinate, z_coordinate):
        # Add triangle 1
        self.vertices.extend([float(x_coordinate), float(y_coordinate), z_coordinate, 1.0])
        self.vertices.extend([float(x_coordinate + 1.0), float(y_coordinate), z_coordinate, 1.0])

        self.vertices.extend([float(x_coordinate), float(y_coordinate + 1.0), z_coordinate, 1.0])

        self.colors.extend(self.color1)
        self.colors.extend(self.color1)
        self.colors.extend(self.color1)

        # Add triangle 2
        self.vertices.extend([float(x_coordinate + 1.0), float(y_coordinate), z_coordinate, 1.0])

        self.vertices.extend([float(x_coordinate + 1.0), float(y_coordinate + 1.0), z_coordinate, 1.0])
        self.vertices.extend([float(x_coordinate), float(y_coordinate + 1.0), z_coordinate, 1.0])

        self.colors.extend(self.color2)
        self.colors.extend(self.color2)
        self.colors.extend(self.color2)
