from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy
from enum import Enum

class VAO_IDs:
    Triangles = 0
    NumVAOs = 1
class Buffer_IDs:
    ArrayBuffer = 0
    NumBuffers = 1
class Attrib_IDs(Enum):
    vPosition = 0

VAOs = [None]*VAO_IDs.NumVAOs
Buffers = [None]*Buffer_IDs.NumBuffers

NumVertices = 6

def create_shader(shader_type, source):
	"""compile a shader."""
	shader = glCreateShader(shader_type)
	glShaderSource(shader, source)
	glCompileShader(shader)
	if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
		raise RuntimeError(glGetShaderInfoLog(shader))
	return shader

VAO = None
shaderProgram = None

def init():
    global shaderProgram
    vsStr = """
    #version 430 core
    layout(location = 0) in vec4 vPosition;
    void main()
    {
        gl_Position = vPosition;
    }
    """
    fsStr = """
    #version 430 core
    out vec4 fColor;
    void main()
    {
        fColor = vec4(0.0, 0.0, 1.0, 1.0);
    }
    """
    #vert_shader = shaders.compileShader(vsStr, GL_VERTEX_SHADER)
    #frag_shader = shaders.compileShader(fsStr, GL_FRAGMENT_SHADER)
    #shaderProgram = shaders.compileProgram(vert_shader, frag_shader)
    vert_shader = create_shader(GL_VERTEX_SHADER, vsStr)
    frag_shader = create_shader(GL_FRAGMENT_SHADER, fsStr)
    shaderProgram = glCreateProgram()
    glAttachShader(shaderProgram, vert_shader)
    glAttachShader(shaderProgram, frag_shader)
    glLinkProgram(shaderProgram)
    glUseProgram(shaderProgram)

    data = numpy.array([0.0, 0.5, 0.0, 1.0,
                        0.5, -0.366, 0.0, 1.0,
                        -0.5, -0.366, 0.0, 1.0,],
                       dtype=numpy.float32)
    
    global VAO
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
    glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
    
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, None)
    
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

def display():
    global VAO
    global shaderProgram
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glUseProgram(shaderProgram)

    glBindVertexArray(VAO)

    glDrawArrays(GL_TRIANGLES, 0, 3)

    glBindVertexArray(0)
    glUseProgram(0)

    #glFlush()
    glutSwapBuffers()

def main():
    glutInit([])
    glutInitContextVersion(4, 3)
    glutInitWindowSize(512, 512)
    glutCreateWindow(b'Tri')

    init()
    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == '__main__':
    main()