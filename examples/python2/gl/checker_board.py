from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random

def initFun():
    glClearColor(1.0,1.0,1.0,0.0)
    glColor3f(0.0,0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0,640.0,0.0,480.0)
    

def displayFun():
    glClear(GL_COLOR_BUFFER_BIT)
    for i in range(0,25):
        gray = idx=random.randint(0,25)/25.0
        glColor3f(gray,gray,gray)
        glRecti(random.randint(0,640),random.randint(0,480),
                random.randint(0,640),random.randint(0,480))
    glFlush()

if __name__ == '__main__':
    glutInit()
    glutInitWindowSize(640,480)
    glutCreateWindow("DrawSquares")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(displayFun)
    initFun()
    glutMainLoop()
