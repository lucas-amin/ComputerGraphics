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


camera_pos = glm.vec3(0.0, 0.0, 3.0)
camera_target = glm.vec3(0.0, 0.0, 0.0)
camera_direction = glm.normalize(camera_pos - camera_target)

up = glm.vec3(0.0, 1.0, 0.0)
camera_right = glm.normalize(glm.cross(up, camera_direction))

camera_up = glm.cross(camera_direction, camera_right)

view = glm.lookAt(glm.vec3(0.0, 0.0, 3.0), glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0))

print(help(glfw))
radius = 10.0;
camX = math.sin(glfw.GetTime()) * radius
camZ = math.cos(glfw.GetTime()) * radius
view = glm.lookAt(glm.vec3(camX, 0.0, camZ), glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0))
