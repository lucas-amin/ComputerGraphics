/**
 * @file appColoredCube.cpp
 * @brief Drawing a colored cube.
 * @author Ricardo Dutra da Silva
 */

//#include <cg.h>
#include <GL/glew.h>
#include <GL/freeglut.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>
#include "shader.h"
#include <iostream>


/* Globals */
GLuint VAO, VBO, CBO;


/* Functions. */
void Init(void);
void Display(void);
void Keyboard(unsigned char, int, int);


void Keyboard(unsigned char key, int x, int y)
{
	/* Closing a window using the keyboard. */
	switch (key)
	{
		/* Escape key.*/
		case 27: 
			exit(0);
		/* q key. */
		case 'q':
		case 'Q':
			exit(0);
	}
}


void Init()
{
	/* Create vertex array object (VAO). */
	glGenVertexArrays(1, &VAO);
	glBindVertexArray(VAO);

	/* Some vertices for the cube. */
	GLfloat vertices[] = {
		-0.5f,-0.5f,-0.5f, 1.0f,
		-0.5f,-0.5f, 0.5f, 1.0f,
		-0.5f, 0.5f, 0.5f, 1.0f,
		 0.5f, 0.5f,-0.5f, 1.0f,
		-0.5f,-0.5f,-0.5f, 1.0f,
		-0.5f, 0.5f,-0.5f, 1.0f,
		 0.5f,-0.5f, 0.5f, 1.0f,
		-0.5f,-0.5f,-0.5f, 1.0f,
		 0.5f,-0.5f,-0.5f, 1.0f,
		 0.5f, 0.5f,-0.5f, 1.0f,
		 0.5f,-0.5f,-0.5f, 1.0f,
		-0.5f,-0.5f,-0.5f, 1.0f,
		-0.5f,-0.5f,-0.5f, 1.0f,
		-0.5f, 0.5f, 0.5f, 1.0f,
		-0.5f, 0.5f,-0.5f, 1.0f,
		 0.5f,-0.5f, 0.5f, 1.0f,
		-0.5f,-0.5f, 0.5f, 1.0f,
		-0.5f,-0.5f,-0.5f, 1.0f,
		-0.5f, 0.5f, 0.5f, 1.0f,
		-0.5f,-0.5f, 0.5f, 1.0f,
		 0.5f,-0.5f, 0.5f, 1.0f,
		 0.5f, 0.5f, 0.5f, 1.0f,
		 0.5f,-0.5f,-0.5f, 1.0f,
		 0.5f, 0.5f,-0.5f, 1.0f,
		 0.5f,-0.5f,-0.5f, 1.0f,
		 0.5f, 0.5f, 0.5f, 1.0f,
		 0.5f,-0.5f, 0.5f, 1.0f,
		 0.5f, 0.5f, 0.5f, 1.0f,
		 0.5f, 0.5f,-0.5f, 1.0f,
		-0.5f, 0.5f,-0.5f, 1.0f,
		 0.5f, 0.5f, 0.5f, 1.0f,
		-0.5f, 0.5f,-0.5f, 1.0f,
		-0.5f, 0.5f, 0.5f, 1.0f,
		 0.5f, 0.5f, 0.5f, 1.0f,
		-0.5f, 0.5f, 0.5f, 1.0f,
		 0.5f,-0.5f, 0.5f, 1.0f
  	};

	/* Some color for the cube. */
  	GLfloat colors[] = {
		0.583f, 0.771f, 0.014f, 1.0f,
		0.609f, 0.115f, 0.436f, 1.0f,
		0.327f, 0.483f, 0.844f, 1.0f,
		0.822f, 0.569f, 0.201f, 1.0f,
		0.435f, 0.602f, 0.223f, 1.0f,
		0.310f, 0.747f, 0.185f, 1.0f,
		0.597f, 0.770f, 0.761f, 1.0f,
		0.559f, 0.436f, 0.730f, 1.0f,
		0.359f, 0.583f, 0.152f, 1.0f,
		0.483f, 0.596f, 0.789f, 1.0f,
		0.559f, 0.861f, 0.639f, 1.0f,
		0.195f, 0.548f, 0.859f, 1.0f,
		0.014f, 0.184f, 0.576f, 1.0f,
		0.771f, 0.328f, 0.970f, 1.0f,
		0.406f, 0.615f, 0.116f, 1.0f,
		0.676f, 0.977f, 0.133f, 1.0f,
		0.971f, 0.572f, 0.833f, 1.0f,
		0.140f, 0.616f, 0.489f, 1.0f,
		0.997f, 0.513f, 0.064f, 1.0f,
		0.945f, 0.719f, 0.592f, 1.0f,
		0.543f, 0.021f, 0.978f, 1.0f,
		0.279f, 0.317f, 0.505f, 1.0f,
		0.167f, 0.620f, 0.077f, 1.0f,
		0.347f, 0.857f, 0.137f, 1.0f,
		0.055f, 0.953f, 0.042f, 1.0f,
		0.714f, 0.505f, 0.345f, 1.0f,
		0.783f, 0.290f, 0.734f, 1.0f,
		0.722f, 0.645f, 0.174f, 1.0f,
		0.302f, 0.455f, 0.848f, 1.0f,
		0.225f, 0.587f, 0.040f, 1.0f,
		0.517f, 0.713f, 0.338f, 1.0f,
		0.053f, 0.959f, 0.120f, 1.0f,
		0.393f, 0.621f, 0.362f, 1.0f,
		0.673f, 0.211f, 0.457f, 1.0f,
		0.820f, 0.883f, 0.371f, 1.0f,
		0.982f, 0.099f, 0.879f, 1.0f
	};

	/* Create vertex buffer object (VBO). */
	glGenBuffers(1, &VBO);
	glBindBuffer(GL_ARRAY_BUFFER, VBO);

	/* Copy data to VBO. */
	glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
	glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, 0);
	glEnableVertexAttribArray(0);

	/* Create color buffer object (CBO). */
	glGenBuffers(1, &CBO);
  	glBindBuffer(GL_ARRAY_BUFFER, CBO);
  	glBufferData(GL_ARRAY_BUFFER, sizeof(colors), colors, GL_STATIC_DRAW);
  	glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, 0);
	glEnableVertexAttribArray(1);

	/* Load and compile shaders. */
	GLuint program = LoadShaders("simple3.vert", "simple3.frag");
	glUseProgram(program);

	/* Compute a fix transformation matrix. */
	glm::mat4 trans = glm::mat4(1.0f);
	trans = glm::rotate(trans, glm::radians(45.0f), glm::vec3(0.0, 0.0, 1.0));
	trans = glm::rotate(trans, glm::radians(30.0f), glm::vec3(0.0, 1.0, 0.0));
	
	/* Bind transformation matrix. */
	unsigned int transformLoc = glGetUniformLocation(program, "transform");
	glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm::value_ptr(trans));
		
	/* Enable depth test (UNCOMMENT THIS PLEASE). */
	//glEnable(GL_DEPTH_TEST);
}


void Display(void)
{

	/* Clear buffers for drawing. */
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	
	/* Draw. */ 
	glBindVertexArray(VAO);
	glDrawArrays(GL_TRIANGLES, 0, 12*3);

	/* Force to display. */
	glFlush();
}


int main(int argc, char** argv)
{
	/* Init GLUT and GL. */
	glutInit(&argc, argv);

	/* Init display mode. */
	glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH);

	/* Window size. */
	glutInitWindowSize(512, 512);

	/* OpenGL Context. */
	glutInitContextVersion(3, 3);
	glutInitContextProfile(GLUT_CORE_PROFILE);

	/* Create window. */
	glutCreateWindow(argv[0]);

	/* Init GLEW. */
	if (glewInit())
       	{
		fprintf(stderr, "Unable to initialize GLEW ... exiting.");
		exit(EXIT_FAILURE);
	}
	
	/* Init GL drawing. */
	Init();

	/* Bind callback functions. */
	glutKeyboardFunc(Keyboard);
	glutDisplayFunc(Display);

	/* Give control to GLUT.*/
	glutMainLoop();
}
