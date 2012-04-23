#!/usr/bin/python2


import RGB_Interface
import IR_Interface

import cv2
from cv2 import cv
#import pygame
from SimpleCV import *
#import PIL
import numpy, glumpy



cam = RGB_Interface.RGB_Camera()
IR = IR_Interface.IR_Camera()

# OpenCV Face Detection stuff


def getFrame():


    def detect(img, cascade):
        rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, 
                                         minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
        if len(rects) == 0:
            return []
        rects[:,2:] += rects[:,:2]
        print rects[:,:]
        return rects



    def draw_rects(img, rects, color):
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)



    # Get image and prepare for face detection
    img = cam.getNumpyArray()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)


    rects = detect(gray, cascade)
    vis = img.copy()
    draw_rects(vis, rects, (0, 255, 0))

    for x1, y1, x2, y2 in rects:
        roi = gray[y1:y2, x1:x2]
        vis_roi = vis[y1:y2, x1:x2]
        #subrects = detect(roi.copy(), nested)
        #draw_rects(vis_roi, subrects, (255, 0, 0))


    return vis




cascade_fn = "../data/haarcascades/haarcascade_frontalface_default.xml"
nested_fn  = "../data/haarcascades/haarcascade_eye.xml"

cascade = cv2.CascadeClassifier(cascade_fn)
nested = cv2.CascadeClassifier(nested_fn)




print "Begin Haar face detection"




# Initilize glumpy stuff
fig = glumpy.figure( (640,480) )

Z = getFrame() 
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
        
        Z[...] = getFrame()
        image.update()
        fig.redraw()


    glumpy.show()

