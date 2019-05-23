import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.arrays import ArrayDatatype
import numpy as np
from ShaderProgram import ShaderProgram

WINDOW_SIZE = 512
MAX_NUM_POINTS = 1000

vertex_shader = open("simple.vert").read()
fragment_shader = open("simple.frag").read()
vao = vbo = 0

# VBO IS A BUFFER
array = np.array([] ,dtype=np.float32)

def Init():
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    # Each point has 3 coordinates, each coordinate is a float, which has 4 bytes
    glBufferData(GL_ARRAY_BUFFER, MAX_NUM_POINTS * 12, None, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferSubData(GL_ARRAY_BUFFER, 0, ArrayDatatype.arrayByteCount(array), array)

    program = ShaderProgram(fragment=fragment_shader, vertex=vertex_shader)
    glUseProgram(program.program_id)

    return vao, vbo, program


def Keyboard(key, x, y):
	if key is 27 or key is 'q' or key is 'Q':
		exit(0);


def Mouse(button, state, x, y):
    if button is GLUT_LEFT_BUTTON:
        if state is GLUT_DOWN:
            print("MOUSE CLICK (%d, %d)\n", x, y)
            xc = x / (float) (WINDOW_SIZE / 2)
            yc = y / (float) (- WINDOW_SIZE / 2)
            xc-=1
            yc+=1
            print("MOUSE CLICK (%f, %f)\n", xc , yc)

            # Create a class point
            array = np.concatenate([array, (xc,yc,0)]).astype(np.float32)

            glBindBuffer(GL_ARRAY_BUFFER, VBO)
            glBufferSubData(GL_ARRAY_BUFFER, 0, ArrayDatatype.arrayByteCount(array), array)
            glutPostRedisplay()

    elif GLUT_RIGHT_BUTTON:
        if state is GLUT_DOWN:
            glBindBuffer(GL_ARRAY_BUFFER, vbo)
            glBufferData(GL_ARRAY_BUFFER, MAX_NUM_POINTS * 12, None, GL_STATIC_DRAW)



def Display():
    # Clear screen
    glClear(GL_COLOR_BUFFER_BIT)

    glBindVertexArray(vao)

    glDrawArrays(GL_POINTS, 0, MAX_NUM_POINTS)

    glFlush()


if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA)

    glutInitWindowSize(WINDOW_SIZE, WINDOW_SIZE)
    glutInitContextVersion(3, 3)
    glutInitContextProfile(GLUT_CORE_PROFILE)
    glutCreateWindow(b'Lista1 - ex1')

    vao, vbo, program = Init()

    glutKeyboardFunc(Keyboard)
    glutMouseFunc(Mouse)
    glutDisplayFunc(Display)

    glutMainLoop();
