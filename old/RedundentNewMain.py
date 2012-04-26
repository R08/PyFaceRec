#!/usr/bin/python2

from RGB_Interface import *
from IR_Interface import *
from PIL import *
import numpy
import glumpy

cam = IR_Camera()
#cam2 = RGB_Camera()

#WINSIZE = 1280,480
#screen = pygame.display.set_mode(WINSIZE,0,8) 
def getFrame():
    #a = numpy.fromstring(cam.depth.get_raw_depth_map(), dtype="uint16").astype(numpy.float32)
    a = cam.rainbowSurf()#.astype(numpy.float32)
    print a
    #a.shape = (480, 640)
    return a
    


def getFrame2():
    a = numpy.fromstring(cam.depth.get_raw_depth_map(), dtype="uint16").astype(numpy.float32)
   # a = cam.rainbowSurf()#.astype(numpy.float32)
    print a
    a.shape = (480, 640)
    return a

#fig = glumpy.figure( (640,480) )
fig2 = glumpy.figure( (640,480) )

#Z = getFrame()
Z2 = getFrame2()
#image = glumpy.image.Image(Z)
image2 = glumpy.image.Image(Z2)


# Main loop
x = True
while x:


        
    @fig2.event
    def on_draw():
#        fig.clear()
        #image.draw( x=0, y=0, z=0, width=fig.width, height=fig.height )
        fig2.clear()
        image2.draw( x=0, y=0, z=0, width=fig2.width, height=fig2.height )


    
    
    @fig2.event
    def on_idle(dt):
        
#        Z[...] = getFrame()
        #image.update()
        #fig.redraw()

        Z2[...] = getFrame2()
        image2.update()
        fig2.redraw()




    glumpy.show()

    print "Image displayed."

    x = False

    


# dont die
while True:
    #print "Did it work?"
    x = False
