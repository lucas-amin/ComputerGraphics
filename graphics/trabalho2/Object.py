import glm

import numpy as np
from Loader import Loader

from Structure import Structure

class Object:
    color1 = [0.1, 0.1, 0.1, 0.7]
    color2 = [1, 1, 1, 0.7]

    def __init__(self):
        self.vertices = list()
        self.colors = list()

    def load_object(self, image_name):
        map = Loader()
        self.structure = Structure()

        self.minimum_value, self.maximum_value, self.map_matrix = map.get_map(use_script=False, image=image_name)

        self.width = len(self.map_matrix)
        self.height = len(self.map_matrix[0])
        self.depth = np.max(self.map_matrix)

        self.vertex_count = self.width * self.height * 6

        self.generate_vertices()

        self.object_center_x = self.width / 2
        self.object_center_y = self.height / 2
        self.object_center_z = self.maximum_value / 2

        return self.colors, self.vertices

    def get_normals(self):
        normals = np.array([])
        normal_arrows = np.array([])

        # 3 floats per vertex, 3 vertices per triangle
        for i in range(len(self.vertices) // 9):
            P = [self.vertices[9 * i], self.vertices[9 * i + 1], self.vertices[9 * i + 2]]
            Q = [self.vertices[9 * i + 3], self.vertices[9 * i + 4], self.vertices[9 * i + 5]]
            R = [self.vertices[9 * i + 6], self.vertices[9 * i + 7], self.vertices[9 * i + 8]]
            middle_point = [P[0] + Q[0] + R[0] / 3, P[1] + Q[1] + R[1] / 3, P[2] + Q[2] + R[2] / 3]

            # For P, Q, R, defined counter-clockwise, glm.cross(R-Q, P-Q)
            RQ = glm.vec3(self.vertices[9 * i + 6] - self.vertices[9 * i + 3],
                          self.vertices[9 * i + 7] - self.vertices[9 * i + 4],
                          self.vertices[9 * i + 8] - self.vertices[9 * i + 5])

            PQ = glm.vec3(self.vertices[9 * i] - self.vertices[9 * i + 3],
                          self.vertices[9 * i + 1] - self.vertices[9 * i + 4],
                          self.vertices[9 * i + 2] - self.vertices[9 * i + 5])

            normal = glm.normalize(glm.cross(RQ, PQ))

            normal_x = middle_point[0] + normal.x
            normal_y = middle_point[1] + normal.y
            normal_z = middle_point[2] + normal.z

            print(middle_point, normal.x, normal.y, normal.z)
            normal_arrows = np.append(normal_arrows, [middle_point[0], middle_point[1], middle_point[2], normal_x, normal_y, normal_z])

            # Insert once for each vertex
            normals = np.append(normals, [normal.x, normal.y, normal.z] * 3)

        return normals, normal_arrows

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
                z_coordinate = self.map_matrix[i][j]

                neighbor1 = self.map_matrix[i + 1][j]
                neighbor2 = self.map_matrix[i][j + 1]
                neighbor3 = self.map_matrix[i + 1][j + 1]

                # self.add_lines(x_coordinate, y_coordinate, z_coordinate, neighbor1, neighbor2, neighbor3)
                self.add_triangle(x_coordinate, y_coordinate, z_coordinate, neighbor1, neighbor2, neighbor3)

        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.colors = np.array(self.colors, dtype=np.float32)

    def add_triangle(self, x_coordinate, y_coordinate, z_coordinate, neighbor1, neighbor2, neighbor3):
        # For P, Q, R, defined counter-clockwise, glm.cross(R-Q, P-Q)

        self.add_attribute(x_coordinate + 1.0, y_coordinate, neighbor1)
        self.add_attribute(x_coordinate, y_coordinate + 1.0, neighbor2)
        self.add_attribute(x_coordinate, y_coordinate, z_coordinate)

        self.add_attribute(x_coordinate + 1.0, y_coordinate + 1.0, neighbor3)
        self.add_attribute(x_coordinate, y_coordinate + 1.0, neighbor2)
        self.add_attribute(x_coordinate + 1.0, y_coordinate, neighbor1)

        polygon = ((x_coordinate, y_coordinate, z_coordinate),
                   (x_coordinate + 1.0, y_coordinate, neighbor1),
                   (x_coordinate, y_coordinate + 1.0, neighbor2))

        self.structure.add_triangle(polygon)

    def add_lines(self, x_coordinate, y_coordinate, z_coordinate, neighbor1, neighbor2, neighbor3):
        # Add first line of triangle
        self.add_attribute(x_coordinate, y_coordinate, z_coordinate)
        self.add_attribute(x_coordinate + 1.0, y_coordinate, neighbor1)

        # Add second line of triangle
        self.add_attribute(x_coordinate, y_coordinate, z_coordinate)
        self.add_attribute(x_coordinate, y_coordinate + 1.0, neighbor2)

        # Add third line of triangle
        self.add_attribute(x_coordinate + 1.0, y_coordinate, neighbor1)
        self.add_attribute(x_coordinate, y_coordinate + 1.0, neighbor2)

        polygon = ((x_coordinate, y_coordinate, z_coordinate),
                   (x_coordinate + 1.0, y_coordinate, neighbor1),
                   (x_coordinate, y_coordinate + 1.0, neighbor2))

        self.structure.add_triangle(polygon)

    def add_attribute(self, x_coordinate, y_coordinate, z_coordinate):
        self.vertices.extend([x_coordinate, y_coordinate, z_coordinate])

        self.colors.extend(self.get_color(x_coordinate, y_coordinate, z_coordinate))

    def get_color(self, x_coordinate, y_coordinate, z_coordinate):
        # return [0.4 , 0.4, 0.4]
        return [x_coordinate / self.width, y_coordinate / self.height, z_coordinate / self.depth]
