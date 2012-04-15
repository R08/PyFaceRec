import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def display():
    glEnable( GL_LIGHTING )
    glEnable( GL_LIGHT0 )
    glEnable( GL_DEPTH_TEST )

    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glPushMatrix()
    gluLookAt( 0,2.5,-7, 0,0,0, 0,1,0 )
    glutSolidTeapot( 2.5 )
    glPopMatrix()
    glFlush()

def reshape(w,h):
    glViewport( 0, 0, w, h )
    glMatrixMode( GL_PROJECTION )
    glLoadIdentity()
    gluPerspective( 45.0, 1.0*w/h, 0.1, 100.0 )
    glMatrixMode( GL_MODELVIEW )
    glLoadIdentity()

def keyboard(key,x,y):
    if key==chr(27): sys.exit(0)

glutInit( sys.argv )
glutInitDisplayMode( GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH )
glutInitWindowSize( 500, 400)
glutCreateWindow( 'teapot' )
glutReshapeFunc( reshape )
glutKeyboardFunc( keyboard )
glutDisplayFunc( display )
glutMainLoop()
