#!/usr/bin/env python3
from OpenGL.GL import *

from OpenGL import GL as gl
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GLUT import *
import glm
import sys
from ShaderProgram import ShaderProgram
import time
import math
from Object import Object

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
vao = program = 0

ORTHO_TRANSFORMATION = 0
FRUSTUM_TRANSFORMATION = 1
PERSPECTIVE_TRANSFORMATION = 2

# Light attributes
lightPos = glm.vec3(1.2, 1.0, 2.0);


class Operator:
    transformation_mode = ORTHO_TRANSFORMATION

    def set_perspective(self):
        view_origin = glm.vec3(0, 0, 1)
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
            if self.visualization_mode is GL_LINES:
                self.visualization_mode = GL_POINTS
            else:
                self.visualization_mode = GL_LINES

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
        global program, vao

        self.visualization_mode = GL_LINES

        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)

        self.object = Object()

        if len(sys.argv) > 1:
            image_name = sys.argv[1]
        else:
            image_name = "crater3"

        colors, vertices = self.object.load_object(image_name)

        # Create vertex buffer object (vbo)matrix
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)

        # Copy data to VBO.
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertices), vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        # Create color buffer object (CBO)
        cbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, cbo)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(colors), colors, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)

        # Load and compile shaders.
        self.program = ShaderProgram(vertex_shader, fragment_shader)

        self.compile_shaders()

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
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glPointSize(1.4)
        glClearColor(0.1, 0.1, 0.1, 0.1)

    def compile_shaders(self):
        try:
            self.shader = compileProgram(compileShader(vertex_shader, gl.GL_VERTEX_SHADER),
                                         compileShader(fragment_shader, gl.GL_FRAGMENT_SHADER))

        except RuntimeError as err:
            sys.stderr.write(err.args[0])
            sys.exit(1)

        for uniform in ('Global_ambient',
                        'Light_ambient',
                        'Light_diffuse',
                        'Light_location',
                        'Material_ambient',
                        'Material_diffuse'):
            location = gl.glGetUniformLocation(self.shader, uniform)

            if location in (None, -1):
                print('Warning, no uniform: %s', (uniform))
            setattr(self, uniform + '_loc', location)

        for attribute in ('Vertex_position', 'Vertex_Normal'):
            location = gl.glGetAttribLocation(self.shader, attribute)

            if location in (None, -1):
                print('Warning, no attribute: %s', (attribute))
            setattr(self, attribute + '_loc', location)

    def Display(self):
        # Clear buffers for drawing.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        transform = self.perspective_matrix * self.view_matrix * self.matrix
        transformLoc = glGetUniformLocation(self.program.program_id, "transform")
        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(transform))

        # Draw.
        glBindVertexArray(vao)

        if self.visualization_mode is GL_POINTS:
            glDrawArrays(GL_POINTS, 0, self.object.vertex_count * 3)

        elif self.visualization_mode is GL_LINES:
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
                self.rotate_object('INCREASE_Y')

            elif mode is SCALE_MODE:
                self.scale_object('INCREASE_Y')

        if key == GLUT_KEY_DOWN:
            if mode is TRANSLATION_MODE:
                # self.translate_object([0.0, (-1) * translation, 0.0])
                self.translate_object('DOWN')

            elif mode is ROTATION_MODE:
                self.rotate_object('LOWER_Y')

            elif mode is SCALE_MODE:
                self.scale_object('LOWER_Y')

        print(self.matrix)

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
