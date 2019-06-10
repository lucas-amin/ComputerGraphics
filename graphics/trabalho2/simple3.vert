#version 330 core

in vec4 vPosition;
in vec3 vColor;

uniform mat4 transform;

out vec3 eColor;

void main()
{
	gl_Position = transform*vPosition;
	eColor = vColor;
}
