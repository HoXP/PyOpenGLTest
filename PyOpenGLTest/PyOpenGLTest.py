from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import os
import numpy

class VAO_IDs:
    Triangles = 0
    NumVAOs = 1
class Buffer_IDs:
    ArrayBuffer = 0
    NumBuffers = 1
class Attrib_IDs:
    vPosition = 0

VAOs = [None] * VAO_IDs.NumVAOs
Buffers = [None] * Buffer_IDs.NumBuffers

NumVertices = 6

def CreateShader(shader_type, source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(shader))
    return shader

def LoadFile(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as fp:
        return fp.read()

def init():
    VAOs[VAO_IDs.Triangles] = glGenVertexArrays(VAO_IDs.NumVAOs)
    glBindVertexArray(VAOs[VAO_IDs.Triangles])

    data = numpy.array([-0.90, -0.90,   #Triangle 1
                        0.85, -0.90,
                        -0.90,  0.85,
                        0.90, -0.85,    #Triangle 2
                        0.90,  0.90,
                        -0.85,  0.90],
                       dtype=numpy.float32)

    Buffers[Buffer_IDs.ArrayBuffer] = glGenBuffers(Buffer_IDs.NumBuffers)
    glBindBuffer(GL_ARRAY_BUFFER, Buffers[Buffer_IDs.ArrayBuffer])
    glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)

    vsStr = LoadFile('vs.shader')
    fsStr = LoadFile('fs.shader')
    vertShader = CreateShader(GL_VERTEX_SHADER, vsStr)
    fragShader = CreateShader(GL_FRAGMENT_SHADER, fsStr)
    shaderProgram = glCreateProgram()
    glAttachShader(shaderProgram, vertShader)
    glAttachShader(shaderProgram, fragShader)
    glLinkProgram(shaderProgram)
    glUseProgram(shaderProgram)

    glVertexAttribPointer(Attrib_IDs.vPosition, 2, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(Attrib_IDs.vPosition)
    
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    glBindVertexArray(VAOs[VAO_IDs.Triangles])
    glDrawArrays(GL_TRIANGLES, 0, NumVertices)

    glFlush()

def main():
    glutInit([])
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(512, 512)
    glutInitContextVersion(4, 3)
    glutInitContextProfile(GLUT_CORE_PROFILE)
    glutCreateWindow(b'Tris')

    init()

    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == '__main__':
    main()