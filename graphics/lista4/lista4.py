#!/usr/bin/env python3
import numpy as np
from OpenGL.arrays import ArrayDatatype
from OpenGL.GL import *
from OpenGL.GLUT import *
import glm
import sys
from ShaderProgram import ShaderProgram
import cyglfw3 as glfw
import math
import time

# Globals
vertex_shader = open("simple3.vert").read()
fragment_shader = open("simple3.frag").read()

counter = 0


class Walk():
    def __init__(self):
        self.camera_speed = 0.001; # adjust accordingly
        self.camera_pos = glm.vec3(0.0, 0.0, 3.0)
        self.camera_front = glm.vec3(0.0,0.0, -1.0)
        self.camera_up = glm.vec3(0.0, 1.0, 0.0)
    
    def move_up(self):
        self.camera_pos += self.camera_speed * self.camera_front;

    def move_down(self):
        self.camera_pos -= self.camera_speed * self.camera_front;

    def move_left(self):
        self.camera_pos -= self.get_normalization()

    def move_right(self):
        self.camera_pos += self.get_normalization()

    def get_normalization(self):
        return glm.normalize(glm.cross(self.camera_front, self.camera_up)) * self.camera_speed

    def get_view(self):
        return glm.lookAt(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

    def update(self, trans):
        view = self.get_view()

        trans = trans * view
        print("____", trans)

        # Bind transformation matrix.
        transformLoc = glGetUniformLocation(program.program_id, "transform")
        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(trans))
                
        # Enable depth test
        glEnable(GL_DEPTH_TEST)

        Display()


walker = Walk()


def Keyboard(key, x, y):
    global trans, program, counter, walker

    if key is 27 or key is b'q' or key is b'Q':
        sys.exit(0)
    
    if key is b'e':        
        camera_pos = glm.vec3(0.0, 0.0, 3.0)
        camera_target = glm.vec3(0.0, 0.0, 0.0)
        camera_direction = glm.normalize(camera_pos - camera_target)

        up = glm.vec3(0.0, 1.0, 0.0)
        camera_right = glm.normalize(glm.cross(up, camera_direction))
        camera_up = glm.cross(camera_direction, camera_right)

        radius = 0.1;
        actual_time = counter
        counter += 0.01
        
        camX = math.sin(actual_time) * radius
        camZ = math.cos(actual_time) * radius
        view = glm.lookAt(glm.vec3(camX, 0.0, camZ), glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0))
        print(trans)

        trans = trans * view

        # Bind transformation matrix.
        transformLoc = glGetUniformLocation(program.program_id, "transform")
        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(trans))
                
        # Enable depth test
        glEnable(GL_DEPTH_TEST)

        Display()

    if key is b'w':
        walker.move_up()

    if key is b's':
        walker.move_down()

    if key is b'a':
        walker.move_left()

    if key is b'd':
        walker.move_right()

    # walker.update(trans)


    '''if key is b'd':
        transformation_code = int(input("Next transformation:"))

        if transformation_code is 1:
            print("Rotation! ")
            transformation_angle = int(input("Angle:"))

            trans = glm.rotate(trans, glm.radians(transformation_angle), glm.vec3(0.0, 0.0, 1.0))
        
        elif transformation_code is 2:
            print("Rotation! ")
            transformation_angle = int(input("Angle:"))

            trans = glm.rotate(trans, glm.radians(transformation_angle), glm.vec3(0.0, 1.0, 0.0))
        
        elif transformation_code is 3:
            print("Rotation! ")
            transformation_angle = int(input("Angle:"))

            trans = glm.rotate(trans, glm.radians(transformation_angle), glm.vec3(1.0, 0.0, 0.0))

        elif transformation_code is 4:
            print("Translation! ")

            d_x = float(input("dx:"))
            d_y = float(input("dy:"))
            d_z = float(input("dz:"))

            trans = glm.translate(trans, glm.vec3(d_x, d_y, d_z))

        elif transformation_code is 5:
            print("Scale! ")

            s_x = float(input("sx:"))
            s_y = float(input("sy:"))
            s_z = float(input("sz:"))


            trans = glm.scale(trans, glm.vec3(s_x, s_y, s_z))
    
        transformLoc = glGetUniformLocation(program.program_id, "transform")
        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(trans))'''
    
trans = 0
vao = program = 0


def Init():
    global program, vao, trans
    vbo = vbo = 0
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vertices = np.array([
        -0.5,-0.5,-0.5, 1.0,
        -0.5,-0.5, 0.5, 1.0,
        -0.5, 0.5, 0.5, 1.0,
         0.5, 0.5,-0.5, 1.0,
        -0.5,-0.5,-0.5, 1.0,
        -0.5, 0.5,-0.5, 1.0,
         0.5,-0.5, 0.5, 1.0,
        -0.5,-0.5,-0.5, 1.0,
         0.5,-0.5,-0.5, 1.0,
         0.5, 0.5,-0.5, 1.0,
         0.5,-0.5,-0.5, 1.0,
        -0.5,-0.5,-0.5, 1.0,
        -0.5,-0.5,-0.5, 1.0,
        -0.5, 0.5, 0.5, 1.0,
        -0.5, 0.5,-0.5, 1.0,
         0.5,-0.5, 0.5, 1.0,
        -0.5,-0.5, 0.5, 1.0,
        -0.5,-0.5,-0.5, 1.0,
        -0.5, 0.5, 0.5, 1.0,
        -0.5,-0.5, 0.5, 1.0,
         0.5,-0.5, 0.5, 1.0,
         0.5, 0.5, 0.5, 1.0,
         0.5,-0.5,-0.5, 1.0,
         0.5, 0.5,-0.5, 1.0,
         0.5,-0.5,-0.5, 1.0,
         0.5, 0.5, 0.5, 1.0,
         0.5,-0.5, 0.5, 1.0,
         0.5, 0.5, 0.5, 1.0,
         0.5, 0.5,-0.5, 1.0,
        -0.5, 0.5,-0.5, 1.0,
         0.5, 0.5, 0.5, 1.0,
        -0.5, 0.5,-0.5, 1.0,
        -0.5, 0.5, 0.5, 1.0,
         0.5, 0.5, 0.5, 1.0,
        -0.5, 0.5, 0.5, 1.0,
         0.5,-0.5, 0.5, 1.0
    ], dtype=np.float32)

    colors = np.array([
        0.583, 0.771, 0.014, 1.0,
        0.609, 0.115, 0.436, 1.0,
        0.327, 0.483, 0.844, 1.0,
        0.822, 0.569, 0.201, 1.0,
        0.435, 0.602, 0.223, 1.0,
        0.310, 0.747, 0.185, 1.0,
        0.597, 0.770, 0.761, 1.0,
        0.559, 0.436, 0.730, 1.0,
        0.359, 0.583, 0.152, 1.0,
        0.483, 0.596, 0.789, 1.0,
        0.559, 0.861, 0.639, 1.0,
        0.195, 0.548, 0.859, 1.0,
        0.014, 0.184, 0.576, 1.0,
        0.771, 0.328, 0.970, 1.0,
        0.406, 0.615, 0.116, 1.0,
        0.676, 0.977, 0.133, 1.0,
        0.971, 0.572, 0.833, 1.0,
        0.140, 0.616, 0.489, 1.0,
        0.997, 0.513, 0.064, 1.0,
        0.945, 0.719, 0.592, 1.0,
        0.543, 0.021, 0.978, 1.0,
        0.279, 0.317, 0.505, 1.0,
        0.167, 0.620, 0.077, 1.0,
        0.347, 0.857, 0.137, 1.0,
        0.055, 0.953, 0.042, 1.0,
        0.714, 0.505, 0.345, 1.0,
        0.783, 0.290, 0.734, 1.0,
        0.722, 0.645, 0.174, 1.0,
        0.302, 0.455, 0.848, 1.0,
        0.225, 0.587, 0.040, 1.0,
        0.517, 0.713, 0.338, 1.0,
        0.053, 0.959, 0.120, 1.0,
        0.393, 0.621, 0.362, 1.0,
        0.673, 0.211, 0.457, 1.0,
        0.820, 0.883, 0.371, 1.0,
        0.982, 0.099, 0.879, 1.0
    ], dtype=np.float32)


    # Create vertex buffer object (vbo)
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    # Copy data to VBO.
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertices), vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)
    
    # Create color buffer object (CBO)
    cbo = glGenBuffers(1);
    glBindBuffer(GL_ARRAY_BUFFER, cbo)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(colors), colors, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(1)
    
    # Load and compile shaders. 
    program = ShaderProgram(vertex_shader, fragment_shader)
    glUseProgram(program.program_id)

    # Compute a fix transformation matrix.
    trans = glm.mat4(1)

    i = 0
    while i < 2:
        transformation_code = int(input("Next transformation:"))

        if transformation_code is 1:
            print("Rotation! ")
            transformation_angle = int(input("Angle:"))

            trans = glm.rotate(trans, glm.radians(transformation_angle), glm.vec3(0.0, 0.0, 1.0))
        
        elif transformation_code is 2:
            print("Rotation! ")
            transformation_angle = int(input("Angle:"))

            trans = glm.rotate(trans, glm.radians(transformation_angle), glm.vec3(0.0, 1.0, 0.0))
        
        elif transformation_code is 3:
            print("Rotation! ")
            transformation_angle = int(input("Angle:"))

            trans = glm.rotate(trans, glm.radians(transformation_angle), glm.vec3(1.0, 0.0, 0.0))

        elif transformation_code is 4:
            print("Translation! ")

            d_x = float(input("dx:"))
            d_y = float(input("dy:"))
            d_z = float(input("dz:"))

            trans = glm.translate(trans, glm.vec3(d_x, d_y, d_z))

        elif transformation_code is 5:
            print("Scale! ")

            s_x = float(input("sx:"))
            s_y = float(input("sy:"))
            s_z = float(input("sz:"))


            trans = glm.scale(trans, glm.vec3(s_x, s_y, s_z))
        
        i+=1

    print("Matrix:" + str(trans))

    # Bind transformation matrix.
    transformLoc = glGetUniformLocation(program.program_id, "transform")
    glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(trans))
            
    # Enable depth test
    glEnable(GL_DEPTH_TEST)


def Display():
    #Clear buffers for drawing.
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw.
    glBindVertexArray(vao)
    glDrawArrays(GL_TRIANGLES, 0, 12*3);

    # Force display
    glutSwapBuffers()


if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(512, 512)
    glutInitContextVersion(3, 3)
    glutInitContextProfile(GLUT_CORE_PROFILE)
    glutCreateWindow(bytes(sys.argv[0], 'utf-8'))

    Init()
    glutKeyboardFunc(Keyboard)
    glutDisplayFunc(Display)

    glutMainLoop()
