#!/usr/bin/env python3
import math

from OpenGL.GL import *

from OpenGL import GL as gl
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GLUT import *
import glm
import sys
from ShaderProgram import ShaderProgram
import time
from math import sin, cos
from Object import Object
import numpy as np

# Globals
vertex_shader = open("./simple3.vert").read()
fragment_shader = open("./simple3.frag").read()

# Loop variable
loop = False

# Records the time of called loop for frame synchronization
lastCall = 0

mode = 0
TRANSLATION_MODE = 0
ROTATION_MODE = 1
SCALE_MODE = 2
vao = vao_triangle_normals = vao_edge_normals = program = 0

ORTHO_TRANSFORMATION = 0
FRUSTUM_TRANSFORMATION = 1
PERSPECTIVE_TRANSFORMATION = 2

# Light attributes
lightPos = glm.vec3(1.2, 1.0, 2.0);

object_transform = glm.mat4(1)
view_origin = glm.vec3(0, 0, 1)
view_matrix = glm.lookAt(view_origin, glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
perspective_matrix = glm.perspective(glm.radians(110), 16 / 9, 0.1, 100)

# Cylindrical coordinates
lightRadius = 1
lightAngle = 0
lightHeight = 0
lightPos = glm.vec3(lightRadius * cos(lightAngle), lightHeight, lightRadius * sin(lightAngle))
lightColor = glm.vec3(1, 1, 1)

objectColor = glm.vec3(1, 0.4, 0.25)

ONLY_POINTS = "ONLY_POINTS"
POINTS_AND_EDGES = "POINTS_AND_EDGES"
POINTS_EDGES_TRIANGLES = "POINTS_EDGES_POLYGONS"
POINTS_EDGES_VERTICES = "POINTS_EDGES_VERTEX"
TERRAIN_CONSTANT = "TERRAIN_CONSTANT"
TERRAIN_SMOOTH = "TERRAIN_SMOOTH"

class Operator:
    transformation_mode = ORTHO_TRANSFORMATION

    def set_perspective(self):
        view_origin = glm.vec3(0, 0, -1)
        self.view_matrix = glm.lookAt(view_origin, glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))

        if self.transformation_mode % 3 is ORTHO_TRANSFORMATION:
            self.perspective_matrix = glm.ortho(-1, 1, -1, 1, 0.5, 100)

        elif self.transformation_mode % 3 is FRUSTUM_TRANSFORMATION:
            self.perspective_matrix = glm.frustum(-1, 1, -1, 1, 0.5, 100.0)

        elif self.transformation_mode % 3 is PERSPECTIVE_TRANSFORMATION:
            self.perspective_matrix = glm.perspective(glm.radians(90), 1, 0.5, 100.0)

        self.transformation_mode += 1

    # The glm::LookAt function requires a position, target and up vector respectively.
    # This creates a view matrix that is the same as the one used in the previous tutorial.
    def look_at(self, time):
        radius = 2.5e-4
        time *= 0.5

        camX = math.sin(3 * time) * radius
        camY = math.sin(2 * time) * radius
        camZ = math.cos(time) * radius

        view = glm.lookAt(glm.vec3(camX, camY, camZ), glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0))

        return view

    # Loop used for automatic look at function calls
    def Loop(self):
        global lastCall

        if not loop:
            return

        actual_time = time.time()
        difference = actual_time - lastCall

        view = self.look_at(difference)

        self.matrix = self.matrix * view

        # Bind transformation matrix.
        transformLoc = glGetUniformLocation(self.program.program_id, "transform")
        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(self.matrix))

        lastCall = time.time()
        self.Display()

    def global_scale(self):
        scale_factor_x = 1 / self.object.width
        scale_factor_y = 1 / self.object.height
        scale_factor_z = 1 / self.object.depth

        translation_factor_x = (-1) * self.object.object_center_x
        translation_factor_y = (-1) * self.object.object_center_y
        translation_factor_z = (-1) * self.object.object_center_z

        self.matrix = glm.scale(self.matrix, glm.vec3(scale_factor_x, scale_factor_y, scale_factor_z))

        self.matrix = glm.translate(self.matrix,
                                    glm.vec3(translation_factor_x,
                                             translation_factor_y,
                                             translation_factor_z))

    # Acts upon keyboard actions
    def Keyboard(self, key, x, y):
        global loop, mode

        # Exits program
        if key is 27 or key is b'q' or key is b'Q':
            sys.exit(0)

        if key is b'l':
            loop = not loop

        if key is b'v':
            if self.visualization_mode is ONLY_POINTS:
                self.visualization_mode = POINTS_AND_EDGES

            elif self.visualization_mode is POINTS_AND_EDGES:
                self.visualization_mode = POINTS_EDGES_TRIANGLES

            elif self.visualization_mode is POINTS_EDGES_TRIANGLES:
                self.visualization_mode = POINTS_EDGES_VERTICES

            elif self.visualization_mode is POINTS_EDGES_VERTICES:
                self.visualization_mode = TERRAIN_CONSTANT

            elif self.visualization_mode is TERRAIN_CONSTANT:
                self.visualization_mode = TERRAIN_SMOOTH

            elif self.visualization_mode is TERRAIN_SMOOTH:
                self.visualization_mode = ONLY_POINTS

        if key is b'c':
            self.set_perspective()

        if key is b't':
            mode = TRANSLATION_MODE

        elif key is b'r':
            mode = ROTATION_MODE

        elif key is b'e':
            mode = SCALE_MODE

        if key is b'a':
            if mode is TRANSLATION_MODE:
                self.translate_object('CLOSE')

            elif mode is ROTATION_MODE:
                self.rotate_object('INCREASE_Z')

            elif mode is SCALE_MODE:
                self.scale_object('INCREASE_Z')

            print(self.matrix)

        if key is b'd':
            if mode is TRANSLATION_MODE:
                self.translate_object('FAR')

            elif mode is ROTATION_MODE:
                self.rotate_object('LOWER_Z')

            elif mode is SCALE_MODE:
                self.scale_object('LOWER_Z')

            print(self.matrix)

        transformLoc = glGetUniformLocation(self.program.program_id, "transform")
        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(self.matrix))

        glutPostRedisplay()

    def rotate_object(self, direction):
        transformation_angle = 3.0

        translation_factor_x = self.object.object_center_x
        translation_factor_y = self.object.object_center_y
        translation_factor_z = self.object.object_center_z

        self.matrix = glm.translate(self.matrix,
                                    glm.vec3([translation_factor_x, translation_factor_y, translation_factor_z]))

        if direction is 'LOWER_Y':
            rotator = [-1.0, 0.0, 0.0]
        elif direction is 'INCREASE_Y':
            rotator = [1.0, 0.0, 0.0]

        if direction is 'LOWER_X':
            rotator = [0.0, -1.0, 0.0]
        elif direction is 'INCREASE_X':
            rotator = [0.0, 1.0, 0.0]

        if direction is 'LOWER_Z':
            rotator = [0.0, 0.0, -1.0]
        elif direction is 'INCREASE_Z':
            rotator = [0.0, 0.0, 1.0]

        self.matrix = glm.rotate(self.matrix, glm.radians(transformation_angle), glm.vec3(rotator))

        self.matrix = glm.translate(self.matrix,
                                    glm.vec3([(-1) * translation_factor_x,
                                              (-1) * translation_factor_y,
                                              (-1) * translation_factor_z]))

    def scale_object(self, direction):
        scaling_factor = 1.09

        translation_factor_x = self.object.object_center_x
        translation_factor_y = self.object.object_center_y
        translation_factor_z = self.object.object_center_z

        self.matrix = glm.translate(self.matrix,
                                    glm.vec3([translation_factor_x, translation_factor_y, translation_factor_z]))

        if direction is 'LOWER_X':
            scaler = [1.0 / scaling_factor, 1.0, 1.0]
        elif direction is 'INCREASE_X':
            scaler = [scaling_factor, 1.0, 1.0]

        if direction is 'LOWER_Y':
            scaler = [1.0, 1.0 / scaling_factor, 1.0]
        elif direction is 'INCREASE_Y':
            scaler = [1.0, scaling_factor, 1.0]

        if direction is 'LOWER_Z':
            scaler = [1.0, 1.0, 1 / scaling_factor]
        elif direction is 'INCREASE_Z':
            scaler = [1.0, 1.0, scaling_factor]

        self.matrix = glm.scale(self.matrix, glm.vec3(scaler))

        self.matrix = glm.translate(self.matrix,
                                    glm.vec3([(-1) * translation_factor_x, (-1) * translation_factor_y,
                                              (-1) * translation_factor_z]))

    def translate_object(self, direction):
        translation_factor = 25

        if direction is 'FAR':
            translator = [0.0, 0.0, (-1) * self.object.depth / translation_factor]
        elif direction is 'CLOSE':
            translator = [0.0, 0.0, self.object.depth / translation_factor]

        elif direction is 'UP':
            translator = [0.0, self.object.height / translation_factor, 0.0]
        elif direction is 'DOWN':
            translator = [0.0, (-1) * self.object.height / translation_factor, 0.0]

        elif direction is 'LEFT':
            translator = [(-1) * self.object.width / translation_factor, 0.0, 0.0]
        elif direction is 'RIGHT':
            translator = [self.object.width / translation_factor, 0.0, 0.0]

        self.matrix = glm.translate(self.matrix, glm.vec3(translator))

        self.object.move(translator)

    def Init(self):
        global program, vao, vao_triangle_normals, vao_edge_normals

        self.visualization_mode = ONLY_POINTS

        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)

        self.object = Object()

        if len(sys.argv) > 1:
            image_name = sys.argv[1]
        else:
            image_name = "maxmin2"

        colors, vertices = self.object.load_object(image_name)

        normals, triangle_normals, edge_normals = self.object.get_normals()

        # Treat edge normals
        triangle_normals = triangle_normals.astype(np.float32)

        # Format edge normals
        edge_normals = edge_normals.astype(np.float32)

        # ----------------------------------------------------------------------
        # Normal vertex buffers
        # ----------------------------------------------------------------------
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertices), vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        NBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, NBO)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(normals), normals, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)

        CBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, CBO)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(colors), colors, GL_STATIC_DRAW)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(2)

        # ----------------------------------------------------------------------
        # Triangle normal buffers
        # ----------------------------------------------------------------------
        vao_triangle_normals = glGenVertexArrays(1)
        glBindVertexArray(vao_triangle_normals)

        VBO_edge_arrows = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO_edge_arrows)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(triangle_normals), triangle_normals, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        vao_edge_normal_colors = glGenVertexArrays(1)
        glBindVertexArray(vao_edge_normal_colors)

        CBO_arrows = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, CBO_arrows)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(triangle_normals), triangle_normals,
                     GL_STATIC_DRAW)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(2)

        # ----------------------------------------------------------------------
        # Edge normal buffers
        # ----------------------------------------------------------------------
        vao_edge_normals = glGenVertexArrays(1)
        glBindVertexArray(vao_edge_normals)

        VBO_edge_arrows = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO_edge_arrows)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(edge_normals), edge_normals, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        vao_edge_normal_colors = glGenVertexArrays(1)
        glBindVertexArray(vao_edge_normal_colors)

        NBO_edge = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, NBO_edge)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(edge_normals), edge_normals, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)

        # Load and compile shaders.
        self.program = ShaderProgram(vertex_shader, fragment_shader)

        glUseProgram(self.program.program_id)

        # Compute a fix transformation matrix.
        self.matrix = glm.mat4(1)
        self.set_perspective()

        # Scale for easier observation
        self.global_scale()

        # Bind transformation matrix.
        transformLoc = glGetUniformLocation(self.program.program_id, "transform")
        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(self.matrix))

        # Enable depth test
        glEnable(GL_DEPTH_TEST)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glPointSize(2.5)
        glClearColor(0.2, 0.2, 0.2, 0.2)

    def Display(self):
        # Clear buffers for drawing.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        transform = self.perspective_matrix * self.view_matrix * self.matrix

        # Load shader uniforms
        modelLoc = glGetUniformLocation(self.program.program_id, "model")
        glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm.value_ptr(transform))

        viewLoc = glGetUniformLocation(self.program.program_id, "view")
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, glm.value_ptr(view_matrix))

        projectionLoc = glGetUniformLocation(self.program.program_id, "projection")
        glUniformMatrix4fv(projectionLoc, 1, GL_FALSE, glm.value_ptr(perspective_matrix))

        objColorLoc = glGetUniformLocation(self.program.program_id, "objectColor")
        glUniform3fv(objColorLoc, 1, glm.value_ptr(objectColor))

        lightColorLoc = glGetUniformLocation(self.program.program_id, "lightColor")
        glUniform3fv(lightColorLoc, 1, glm.value_ptr(lightColor))

        lightPosLoc = glGetUniformLocation(self.program.program_id, "lightPos")
        glUniform3fv(lightPosLoc, 1, glm.value_ptr(lightPos))

        viewPosLoc = glGetUniformLocation(self.program.program_id, "viewPos")
        glUniform3fv(viewPosLoc, 1, glm.value_ptr(view_origin))

        # Draw different visualization modes

        glBindVertexArray(vao)
        if self.visualization_mode == ONLY_POINTS:
            glDrawArrays(GL_POINTS, 0, self.object.vertex_count * 3)

        elif self.visualization_mode == POINTS_AND_EDGES:
            glDrawArrays(GL_LINES, 0, self.object.vertex_count * 3)

        elif self.visualization_mode == POINTS_EDGES_TRIANGLES:
            glDrawArrays(GL_LINES, 0, self.object.vertex_count * 3)

            glBindVertexArray(vao_triangle_normals)
            glDrawArrays(GL_LINES, 0, self.object.vertex_count * 3)

        elif self.visualization_mode == POINTS_EDGES_VERTICES:
            glDrawArrays(GL_LINES, 0, self.object.vertex_count * 3)

            glBindVertexArray(vao_edge_normals)
            glDrawArrays(GL_LINES, 0, self.object.vertex_count * 3)

        elif self.visualization_mode is TERRAIN_CONSTANT:
            glDrawArrays(GL_TRIANGLES, 0, self.object.vertex_count * 3)
            glDrawArrays(GL_LINES, 0, self.object.vertex_count * 3)

        elif self.visualization_mode is TERRAIN_SMOOTH:
            glDrawArrays(GL_TRIANGLES, 0, self.object.vertex_count * 3)
            glBindVertexArray(vao_edge_normals)

            glDrawArrays(GL_LINES, 0, self.object.vertex_count * 3)

        # Force display
        glutSwapBuffers()

    def catchKey(self, key, x, y):
        global loop

        if key == GLUT_KEY_LEFT:
            if mode is TRANSLATION_MODE:
                self.translate_object('LEFT')

            elif mode is ROTATION_MODE:
                self.rotate_object('LOWER_X')

            elif mode is SCALE_MODE:
                self.scale_object('LOWER_X')

        if key == GLUT_KEY_RIGHT:
            if mode is TRANSLATION_MODE:
                self.translate_object('RIGHT')

            elif mode is ROTATION_MODE:
                self.rotate_object('INCREASE_X')

            elif mode is SCALE_MODE:
                self.scale_object('INCREASE_X')

        if key == GLUT_KEY_UP:
            if mode is TRANSLATION_MODE:
                self.translate_object('UP')

            elif mode is ROTATION_MODE:
                self.rotate_object('LOWER_Y')

            elif mode is SCALE_MODE:
                self.scale_object('INCREASE_Y')

        if key == GLUT_KEY_DOWN:
            if mode is TRANSLATION_MODE:
                self.translate_object('DOWN')

            elif mode is ROTATION_MODE:
                self.rotate_object('INCREASE_Y')

            elif mode is SCALE_MODE:
                self.scale_object('LOWER_Y')

        transformLoc = glGetUniformLocation(self.program.program_id, "transform")
        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(self.matrix))

        glutPostRedisplay()


if __name__ == "__main__":
    operator = Operator()

    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(1024, 1024)
    glutInitContextVersion(3, 3)
    glutInitContextProfile(GLUT_CORE_PROFILE)
    glutCreateWindow(bytes(sys.argv[0], 'utf-8'))

    operator.Init()
    glutKeyboardFunc(operator.Keyboard)
    glutSpecialFunc(operator.catchKey)
    glutDisplayFunc(operator.Display)
    glutIdleFunc(operator.Loop)

    glutMainLoop()
