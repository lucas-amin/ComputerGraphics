#!/usr/bin/env python3
import numpy as np
from OpenGL.arrays import ArrayDatatype
from OpenGL.GL import *
from OpenGL.GLUT import *
import glm
import sys
from ShaderProgram import ShaderProgram
from loader import Map
import time
import math

# Globals
vertex_shader = open("simple3.vert").read()
fragment_shader = open("simple3.frag").read()

# Scaling factor
scale_factor = 0.07

# Loop variable
loop = False

# Records the time of called loop for frame synchronization
lastCall = 0

mode = 0
TRANSLATION_MODE = 0
ROTATION_MODE = 1
SCALE_MODE = 2

# The glm::LookAt function requires a position, target and up vector respectively. 
# This creates a view matrix that is the same as the one used in the previous tutorial. 
def look_at(time):
    radius = 2.5e-4
    time *= 0.5

    camX = math.sin(3 * time) * radius 
    camY = math.sin(2 * time) * radius 
    camZ = math.cos(time) * radius 

    view = glm.lookAt(glm.vec3(camX, camY, camZ), glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0))

    return view

# Loop used for automatic look at function calls
def Loop():
    global trans, lastCall

    if not loop:
        return

    actual_time = time.time()
    difference = actual_time - lastCall

    view = look_at(difference)
    
    trans = trans * view

    # Bind transformation matrix.
    transformLoc = glGetUniformLocation(program.program_id, "transform")
    glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(trans))

    lastCall = time.time()
    Display()

def global_scale(matrix):
    global scale_factor

    trans = glm.mat4(1)

    scale_matrix = glm.scale(trans, glm.vec3(scale_factor, scale_factor, scale_factor))

    matrix = scale_matrix * matrix

    return matrix

# Acts upon keyboard actions
def Keyboard(key, x, y):

    global trans, program, loop, scale_factor, mode
    # Exits program
    if key is 27 or key is b'q' or key is b'Q':
        sys.exit(0)

    if key is b'l':
        loop = not loop

    # Symmetric projection
    if key is b'i':
        print("Symmetric view!")
        view = glm.vec3(1.0, 1.0, 0.5)
        view_matrix = glm.lookAt(view, glm.vec3(0.0 ,0.0 , 0.0), glm.vec3(0, 0.1, 0))

        trans = global_scale(view_matrix)

    # Dimetric projection
    elif key is b'o':
        print("Dimetric view!")

        view = glm.vec3(1.0, 0.3, 0.5)
        view_matrix = glm.lookAt(view, glm.vec3(0.0 ,0.0 , 0.0), glm.vec3(0, 1.0, 0))

        trans = global_scale(view_matrix)

    # Isometric projection
    elif key is b'p':
        print("Isometric view!")

        view = glm.vec3(1.0, 1.0, 1.0)
        view_matrix = glm.lookAt(view, glm.vec3(0.0 ,0.0 , 0.0), glm.vec3(0, 1.0, 0))

        trans = global_scale(view_matrix)

    if key is b't':
        mode = TRANSLATION_MODE

    elif key is b'r':
        mode = ROTATION_MODE

    elif key is b'e':
        mode = SCALE_MODE

    translation = scale_factor * 10
    transformation_angle = 5
    scaling_factor = 1.2

    if key is b'a':
        if mode is TRANSLATION_MODE:
            trans = glm.translate(trans, glm.vec3(0.0, 0.0, translation))

        elif mode is ROTATION_MODE:
            trans = glm.rotate(trans, glm.radians(transformation_angle), glm.vec3(0.0, 0.0, 1.0))

        elif mode is SCALE_MODE:
            trans = glm.scale(trans, glm.vec3(1.0, 1.0, scaling_factor))

    if key is b'd':
        if mode is TRANSLATION_MODE:
            trans = glm.translate(trans, glm.vec3(0.0, 0.0, -1 * translation))

        elif mode is ROTATION_MODE:
            trans = glm.rotate(trans, glm.radians(-1 * transformation_angle), glm.vec3(0.0, 0.0, 1.0))

        elif mode is SCALE_MODE:
            trans = glm.scale(trans, glm.vec3(1.0, 1.0, 1 / scaling_factor))

    # Perform manual transformations
    if key is b'z':
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
    glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(trans))

    glutPostRedisplay()

vertex_count = 0    
trans = 0
vao = program = 0
def Init():
    global program, vao, trans, scale_factor, vertex_count
    vbo = vbo = 0
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    map = Map()

    minimum, maximum, result = map.get_map(use_script=False, image = "crater3")
    width = len(result)
    height = len(result[0])

    vertex_count = width * height * 2

    vertices = list()
    colors = list()
    color1 = [0.0, 1.0, 0.0, 0.0]
    color2 = [1.0, 0.0, 0.0, 0.0]

    image_diagonal = math.sqrt((width ** 2) + (height ** 2))
    scale_factor = 20 / image_diagonal

    print(scale_factor)

    for i in range(len(result)):
        for j in range(len(result[i])):
            x_coordinate = i * scale_factor
            y_coordinate = j * scale_factor
            z_coordinate = (result[i][j] / maximum) / scale_factor

            vertices.extend([float(x_coordinate), float(y_coordinate), z_coordinate, 1.0])
            vertices.extend([float(x_coordinate + 1.0 * scale_factor), float(y_coordinate), z_coordinate, 1.0])
            vertices.extend([float(x_coordinate), float(y_coordinate + 1.0 * scale_factor), z_coordinate, 1.0])

            vertices.extend([float(x_coordinate + 1.0 * scale_factor), float(y_coordinate), z_coordinate, 1.0])
            vertices.extend([float(x_coordinate + 1.0 * scale_factor), float(y_coordinate + 1.0 * scale_factor), z_coordinate, 1.0])
            vertices.extend([float(x_coordinate), float(y_coordinate + 1.0 * scale_factor), z_coordinate, 1.0])

            colors.extend(color1)
            colors.extend(color1)
            colors.extend(color1)

            colors.extend(color2)
            colors.extend(color2)
            colors.extend(color2)

    vertices = np.array(vertices,dtype=np.float32)
    colors = np.array(colors,dtype=np.float32)

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

    # Scale for easier observation
    trans = global_scale(trans)

    d_x = 0
    d_y = 0
    d_z = 0

    trans = glm.translate(trans, glm.vec3(d_x, d_y, d_z))

    # Bind transformation matrix.
    transformLoc = glGetUniformLocation(program.program_id, "transform")
    glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(trans))
            
    # Enable depth test
    glEnable(GL_DEPTH_TEST)


def Display():
    global vertex_count

    #Clear buffers for drawing.
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw.
    glBindVertexArray(vao)

    glDrawArrays(GL_TRIANGLES, 0, vertex_count * 3);

    # Force display
    glutSwapBuffers()

def catchKey(key, x, y):
    global trans, program, loop, scale_factor
    translation = scale_factor * 10
    transformation_angle = 5
    scaling_factor = 2

    if key == GLUT_KEY_LEFT:
        if mode is TRANSLATION_MODE:
            trans = glm.translate(trans, glm.vec3((-1) * translation, 0.0, 0.0))

        elif mode is ROTATION_MODE:
            trans = glm.rotate(trans, glm.radians((-1) * transformation_angle), glm.vec3(0.0, 1.0, 0.0))

        elif mode is SCALE_MODE:
            trans = glm.scale(trans, glm.vec3(1 / scaling_factor, 1.0, 1.0))

    if key == GLUT_KEY_RIGHT:
        if mode is TRANSLATION_MODE:
            trans = glm.translate(trans, glm.vec3(translation, 0.0, 0.0))

        elif mode is ROTATION_MODE:
            trans = glm.rotate(trans, glm.radians(transformation_angle), glm.vec3(0.0, 1.0, 0.0))

        elif mode is SCALE_MODE:
            trans = glm.scale(trans, glm.vec3(scaling_factor, 1.0, 1.0))


    if key == GLUT_KEY_UP:
        if mode is TRANSLATION_MODE:
            trans = glm.translate(trans, glm.vec3(0.0, translation, 0.0))

        elif mode is ROTATION_MODE:
            trans = glm.rotate(trans, glm.radians(transformation_angle), glm.vec3(1.0, 0.0, 0.0))

        elif mode is SCALE_MODE:
            trans = glm.scale(trans, glm.vec3(1.0, scaling_factor, 1.0))

    if key == GLUT_KEY_DOWN:
        if mode is TRANSLATION_MODE:
            trans = glm.translate(trans, glm.vec3(0.0, (-1) * translation, 0.0))

        elif mode is ROTATION_MODE:
            trans = glm.rotate(trans, glm.radians((-1) * transformation_angle), glm.vec3(1.0, 0.0, 0.0))

        elif mode is SCALE_MODE:
            trans = glm.scale(trans, glm.vec3(1.0, 1 / scaling_factor, 1.0))


    print(trans)

    transformLoc = glGetUniformLocation(program.program_id, "transform")
    glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(trans))

    glutPostRedisplay()


if __name__ == "__main__":
    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(1024, 1024)
    glutInitContextVersion(3, 3)
    glutInitContextProfile(GLUT_CORE_PROFILE)
    glutCreateWindow(bytes(sys.argv[0], 'utf-8'))

    Init()
    glutKeyboardFunc(Keyboard)
    glutSpecialFunc(catchKey)
    glutDisplayFunc(Display)
    glutIdleFunc(Loop)

    glutMainLoop()
