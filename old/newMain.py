#!/usr/bin/python2


import RGB_Interface
import IR_Interface

import cv2
from cv2 import cv
#import pygame
from SimpleCV import *
#import PIL
import numpy, glumpy

import FaceRec



RGB = RGB_Interface.RGB_Camera()
IR = IR_Interface.IR_Camera()







print "Begin Haar face detection"




# Initilize glumpy stuff
fig = glumpy.figure( (640,480) )

Z = haar_face.getFrame(RGB) 
image = glumpy.image.Image(Z)




## Main loop
run = True
while run:

    # Draw with glumpy
    @fig.event
    def on_draw():
        fig.clear()
        image.draw( x=0, y=0, z=0, width=fig.width, height=fig.height )


    @fig.event
    def on_idle(dt):
        
        Z[...] = haar_face.getFrame(RGB)
        image.update()
        fig.redraw()


    glumpy.show()

