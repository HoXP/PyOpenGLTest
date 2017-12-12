from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import os
import numpy
#用class实现Python所不支持的enum
class VAO_IDs:  #定义VAO名称枚举
    Triangles = 0
    NumVAOs = 1
class Buffer_IDs:   #定义VBO名称枚举
    ArrayBuffer = 0
    NumBuffers = 1
class Attrib_IDs:
    vPosition = 0

VAOs = [None] * VAO_IDs.NumVAOs
Buffers = [None] * Buffer_IDs.NumBuffers

NumVertices = 6 #顶点数

def CreateShader(shaderType, source):
    shader = glCreateShader(shaderType)    #创建着色器对象，并得到着色器对象名（一个非0整数）
    glShaderSource(shader, source)  #将着色器源码关联到着色器对象上
    glCompileShader(shader) #编译着色器源码
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE: #如果编译状态不为GL_TRUE，即编译失败
        raise RuntimeError(glGetShaderInfoLog(shader))  #则返回日志信息
    return shader

def LoadFile(filename): #获取文件中的文本
    with open(os.path.join(os.path.dirname(__file__), filename)) as fp:
        return fp.read()

def init():
    VAOs[VAO_IDs.Triangles] = glGenVertexArrays(VAO_IDs.NumVAOs)    #生成VAO，并得到VAO名（一个非0整数）
    glBindVertexArray(VAOs[VAO_IDs.Triangles])  #绑定VAO
    #顶点数据
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
    shaderProgram = glCreateProgram()   #创建空的着色器程序
    glAttachShader(shaderProgram, vertShader)   #将着色器对象关联到着色器程序上
    glAttachShader(shaderProgram, fragShader)
    glLinkProgram(shaderProgram)    #链接着色器程序
    glUseProgram(shaderProgram) #使用着色器程序处理顶点片元

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