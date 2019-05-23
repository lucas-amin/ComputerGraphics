#version 330 core

in vec4 vPosition;
in vec4 vColor;

uniform mat4 transform;

out vec4 eColor;

void main()
{
	gl_Position = transform*vPosition;
	eColor = vColor;
}
