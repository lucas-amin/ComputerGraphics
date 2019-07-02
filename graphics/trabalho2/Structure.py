import numpy as np

class Structure():

    def __init__(self):
        self.polygons = []
        self.vertices = []
        self.lines = []

    def add_line(self, line):
        self.lines.extend(line)

    def add_vertex(self, vertex):
        self.vertices.extend(vertex)

    def add_triangle(self, points):
        for points in points:
            self.add_vertex(points)

        first_line = (points[0], points[1])
        second_line = (points[1], points[2])
        third_line = (points[2], points[0])

        self.add_line(first_line)
        self.add_line(second_line)
        self.add_line(third_line)

        self.add_polygon(points)

    def add_polygon(self, polygon):
        self.polygons.extend(polygon)

    @staticmethod
    def get_triangle_normal(triangle):
        first_line = triangle[0]
        second_line = triangle[1]

        first_point = first_line[0]
        second_point = first_line[1]
        third_point = second_line[2]

        normal = np.cross(second_point - first_point, third_point - first_point)

        return normal
