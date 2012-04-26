#!/usr/bin/python2

"""
This source file is passed to the python interpreter by the user to start the
  system. This source file contains function definitions for drawing and the
  main while loop.
"""




# Third party modules
#import cv2           # OpenCV - Computer vision library
#from cv2 import cv   # Legacy support for opencv ver. < 2.x
import numpy as np   # Python matrix library
import glumpy        # Visualizes numpy arrays using OpenGL


# Our modules
import RGB_Interface    # Interface for interacting with the kinect RGB camera.
import IR_Interface     # Interface for interacting with the kinect IR camera.
import FaceRec          # Face detection and recognition implementation.





# Create instaces of the RGB and IR interface
RGB = RGB_Interface.RGB_Camera()
IR = IR_Interface.IR_Camera()



# OpenCV Face Detection stuff
haar_face = FaceRec.HaarDetectFace()



# Initilize glumpy stuff
haar_fig = glumpy.figure((1280, 480))
#fig1  = haar_fig.add_figure(cols=2,rows=1, position=[0,0])

haar_frame = haar_face.getFrame(RGB)[0]
#haar_frame = fig1.add_frame(aspect=1)
#haar_frame.push(haar_face.getFrame(RGB)[0])

haar_img = glumpy.image.Image(haar_frame)


#haar_croped_frame = haar_face.getCropedFaceImg(RGB)
#haar_croped_img = glumpy.image.Image(haar_croped_frame)


## Main loop
#run = True
#while run:

    # Draw with glumpy

    # haar
@haar_fig.event
def on_draw():
    #haar_croped_frame = haar_face.getCropedFaceImg(RGB)

    haar_fig.clear()
    haar_img.draw(x=0, y=0, z=0, width=640, height=480)
    #haar_croped_img.draw( x=640, y=0, z=0, width=640, height=480)

@haar_fig.event
def on_idle(dt):
    h_frame = haar_face.getFrame(RGB)[0]
    haar_frame[...] = h_frame
   # haar_croped_frame[...] = haar_face.getCropedFaceImg(RGB)
   # haar_croped_img.update()
    haar_img.update()
    haar_fig.redraw()


@haar_fig.event
def on_key_press(key, modifiers):
    if key == glumpy.window.key.SPACE:
        print "Key pressed"
        haar_face.getCropedFaceImg(RGB, IR)

# Hacked in
#from PIL import Image
#pi = Image.fromstring('RGB', (



glumpy.show()




#haar_croped_fig = glumpy.figure((100, 100))
##haar_croped_frame = haar_face.getFrame(RGB)
##haar_croped_frame = haar_face.getCropedFaceImg(RGB)
##haar_croped_img = glumpy.image.Image(haar_croped_frame)

## haar croped
#@haar_croped_fig.event
#def on_draw():
    #haar_croped_fig.clear()
    #haar_croped_img.draw( x=0, y=0, z=0, width=haar_croped_fig.width, height=haar_croped_fig.height )


#@haar_croped_fig.event
#def on_idle(dt):
    #haar_croped_frame[...] = haar_face.getCropedFaceImg(RGB)
    #haar_croped_img.update()
    #haar_croped_fig.redraw()


#while True:
    #glumpy.show()

