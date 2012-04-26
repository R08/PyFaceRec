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

face_rec = FaceRec.FaceRec()


# Initilize glumpy stuff
haar_fig = glumpy.figure((1280, 1760))
haar_frame = haar_face.getFrame(RGB, IR)[0]
haar_img = glumpy.image.Image(haar_frame)

depth_frame = IR.getNumpyArray().astype(np.float32)
depth_frame_8 = IR.getNumpyArray_8()
depth_img = glumpy.image.Image(depth_frame)
depth_img_8 = glumpy.image.Image(depth_frame_8)


#crop_face = np.zeros([23, 23])

    

# Draw with glumpy

# 8bit |  ...  #
# RGB  | 32bit #
@haar_fig.event
def on_draw():
    haar_fig.clear()
    haar_img.draw(x=0, y=0, z=0, width=640, height=480)
    depth_img.draw(x=640, y=0, z=0, width=640, height=480)
    depth_img_8.draw(x=0, y=480, z=0, width=640, height=480)


@haar_fig.event
def on_idle(dt):   
    haar_frame[...] = haar_face.getFrame(RGB, IR)[0]
    depth_frame[...] = IR.getNumpyArray().astype(np.float32)
    depth_frame_8[...] = IR.getNumpyArray_8()
    haar_img.update()
    depth_img.update()
    depth_img_8.update()
    haar_fig.redraw()


@haar_fig.event
def on_key_press(key, modifiers):
    if key == glumpy.window.key.SPACE:
        print "Key Press: SPACE"
        crop_face = haar_face.getCropedFaceImg(RGB, IR)
        face_rec.preprocess(crop_face)



glumpy.show()


