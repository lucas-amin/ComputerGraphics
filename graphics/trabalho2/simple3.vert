#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;

in vec4 vPosition;
in vec4 vColor;

uniform mat4 transform;
uniform vec3 objectColor;
uniform vec3 lightColor;

out vec4 eColor;

void main()
{
	gl_Position = transform * vPosition;

    eColor = vColor;

	// eColor = vColor;

}
