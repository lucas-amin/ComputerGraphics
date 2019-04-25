#!/usr/bin/env python3
import numpy as np
from OpenGL.arrays import ArrayDatatype
from OpenGL.GL import *
from OpenGL.GLUT import *
import glm
import sys
from ShaderProgram import ShaderProgram
from loader import Map

# Globals
vertex_shader = open("simple3.vert").read()
fragment_shader = open("simple3.frag").read()

def Keyboard(key, x, y):
    global trans, program
    if key is 27 or key is b'q' or key is b'Q':
        sys.exit(0)
    
    if key is b'd':
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

        Display()

    
trans = 0
vao = program = 0
def Init():
    global program, vao, trans
    vbo = vbo = 0
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    map = Map()

    minimum, maximum, result = map.get_map()

    print(minimum,maximum)
    vertices = list()
    colors = list()
    for i in range(len(result)):
        for j in range(len(result[i])):
            vertices.extend([float(i), float(j), 0.0, 1.0])
            colors.extend([0.583, 0.771, 0.014, 1.0,])

    for i in range(0, len(vertices), 4):
        print(vertices[i:i+4])


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
    glutInitWindowSize(800, 600)
    glutInitContextVersion(3, 3)
    glutInitContextProfile(GLUT_CORE_PROFILE)
    glutCreateWindow(bytes(sys.argv[0], 'utf-8'))

    Init()
    glutKeyboardFunc(Keyboard)
    glutDisplayFunc(Display)


    glutMainLoop()
