#!/usr/bin/python2

import sys
sys.path.append("/share/PyFaceRec/src/")

#from RGB_Interface import *
from PIL import Image
from openni import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *





# Create and initalize openNI context node.
ctx = Context()
ctx.init()

# Create an image generator
img = ImageGenerator()
img.create(ctx)

# Start generating
ctx.start_generating_all()
nRetVal = ctx.wait_one_update_all(img)


def getRGB_Frame(g_im):
    """Returns the RGB image from the from the camera."""
    return Image.fromstring('RGB', (640, 480), g_im.get_raw_image_map(), 'raw')


camera = getRGB_Frame(img)




def initFun():
    glClearColor(1.0,1.0,1.0,0.0)
    glColor3f(0.0,0.0, 0.0)
    glPointSize(4.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0,640.0,0.0,480.0)
    

def displayFun():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)
    glVertex2i(100,50)
    glVertex2i(100,130)
    glVertex2i(150,130)
    glEnd()

    # 2D texture test
    glEnable(GL_TEXTURE_2D)
    #glBindTexture(GL_TEXTURE_2D, camera)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE)
    
    glFlush()





# Initilize openGL and glut
glutInit()
glutInitWindowSize(640,480)
glutCreateWindow("Drawdots")
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutDisplayFunc(displayFun)
initFun()
glutMainLoop()




# Main Loop
run = True
while run:

    # Update
    nRetVal = ctx.wait_one_update_all(img)
    camera = getRGB_Frame(img)
    
        
