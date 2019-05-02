#!/usr/bin/env python3
import numpy as np
from OpenGL.arrays import ArrayDatatype
from OpenGL.GL import *
from OpenGL.GLUT import *
import glm
import sys
from ShaderProgram import ShaderProgram
import math
import time

# Globals
vertex_shader = open("simple3.vert").read()
fragment_shader = open("simple3.frag").read()

# Records the time of called loop for frame synchronization
lastCall = 0

# Global transformation matrix   
trans = 0

# Initialization variables
vao = program = 0

# Loop variable
loop = False

# Scale factor
scale = 0.3

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
	global scale

	trans = glm.mat4(1)

	scale_matrix = glm.scale(trans, glm.vec3(scale, scale, scale))

	matrix = scale_matrix * matrix

	return matrix

# Acts upon keyboard actions
def Keyboard(key, x, y):
	global trans, program, loop, scale

	# Exits program
	if key is 27 or key is b'q' or key is b'Q':
		sys.exit(0)

	if key is b'l':
		loop = not loop

	# Symmetric projection
	if key is b's':
		print("Symmetric view!")
		view = glm.vec3(1.0, 1.0, 0.5)
		view_matrix = glm.lookAt(view, glm.vec3(0.0 ,0.0 , 0.0), glm.vec3(0, 0.1, 0))

		trans = global_scale(view_matrix)

	# Dimetric projection
	elif key is b'd':
		print("Dimetric view!")

		view = glm.vec3(1.0, 0.3, 0.5)
		view_matrix = glm.lookAt(view, glm.vec3(0.0 ,0.0 , 0.0), glm.vec3(0, 1.0, 0))

		trans = global_scale(view_matrix)

	# Isometric projection
	elif key is b't':
		print("Isometric view!")

		view = glm.vec3(1.0, 1.0, 1.0)
		view_matrix = glm.lookAt(view, glm.vec3(0.0 ,0.0 , 0.0), glm.vec3(0, 1.0, 0))

		trans = global_scale(view_matrix)

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


	print(trans)

	transformLoc = glGetUniformLocation(program.program_id, "transform")
	glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(trans))

	Display()

def Init():
    global program, vao, trans, scale
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
        1.0, 1.0, 1.0, 1.0, # Face 0.1 - White
        1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 0.0, 1.0, # Face 1.1 - Yellow
        1.0, 1.0, 0.0, 1.0,
        1.0, 1.0, 0.0, 1.0,
        0.2, 0.2, 0.2, 1.0, # Face 2.1 - Grey
        0.2, 0.2, 0.2, 1.0,
        0.2, 0.2, 0.2, 1.0,
        1.0, 1.0, 0.0, 1.0, # Face 1.2 - Yellow
        1.0, 1.0, 0.0, 1.0,
        1.0, 1.0, 0.0, 1.0,
        1.0, 1.0, 1.0, 1.0, # Face 0.2 - White
        1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0,
        0.2, 0.2, 0.2, 1.0, # Face 2.2 - Grey
        0.2, 0.2, 0.2, 1.0,
        0.2, 0.2, 0.2, 1.0,
        1.0, 0.0, 0.0, 1.0, # Face 4.1 - Red
        1.0, 0.0, 0.0, 1.0,
        1.0, 0.0, 0.0, 1.0,
        0.0, 1.0, 0.0, 1.0, # Face 5.1 - Green
        0.0, 1.0, 0.0, 1.0,
        0.0, 1.0, 0.0, 1.0,
        0.0, 1.0, 0.0, 1.0, # Face 5.2 - Green
        0.0, 1.0, 0.0, 1.0,
        0.0, 1.0, 0.0, 1.0,
        0.0, 0.0, 1.0, 1.0, # Face 3.1 - Blue
        0.0, 0.0, 1.0, 1.0,
        0.0, 0.0, 1.0, 1.0,
        0.0, 0.0, 1.0, 1.0, # Face 3.2 - Blue
        0.0, 0.0, 1.0, 1.0,
        0.0, 0.0, 1.0, 1.0,
        1.0, 0.0, 0.0, 1.0, # Face 4.2 - Red
        1.0, 0.0, 0.0, 1.0,
        1.0, 0.0, 0.0, 1.0,
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

    # Scale for easier observation
    trans = glm.scale(trans, glm.vec3(scale, scale, scale))

    # Bind transformation matrix.
    transformLoc = glGetUniformLocation(program.program_id, "transform")
    glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(trans))
            
    # Enable depth test
    glEnable(GL_DEPTH_TEST)

# Function called on each display update call
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
    glutIdleFunc(Loop)

    glutMainLoop()
