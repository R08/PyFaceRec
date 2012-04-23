"""
Kinect IR Camera Interface
"""
from openni import *
import pygame
from PIL import *
from numpy import * 
from HW_Interface import *

# Start Context Node.
#ctx = Context()
#ctx.init()


def colorFunc(a):
       
    if a <= 255:
        r = 255 - a
        g = 0
        b = 255
    elif a <= 510:
        r = 0
        g = a- 255
        b = 255
    elif a <= 765:
        r = 0
        g = 255
        b = 765 - a 
    elif a <= 1025:
        r = a - 765
        g = 255
        b = 0
    elif a <= 1275:
        r = 255
        g = 1275 - a
        b = 0
    else:
        r = 0
        g = 0
        b = 0

    
    return array([r, b, g], dtype='uint8')




def colorFunc2(a):
    r = a * .056
    g = a * .056
    b = 0
    
    return array([r, g, b], dtype='float32')


"""
IR_Camera Class:
"""

class IR_Camera(HW_Interface):
    """
    Provides basic interaction with the kinects IR camera.
    """
    depth = DepthGenerator()


    def __init__(self):
        """
        Create and attach an image generator to the context node.
        """
        print "Initalizing Depth Generator for IR Camera."
        self.depth.create(ctx)
        ctx.start_generating_all()
        self.depth.set_resolution_preset(RES_VGA)
        self.depth.fps = 30



    def update(self):
        """
        Updates the Depth generator node.
        """
        print "Updating Depth Generator..."

        err = ctx.wait_one_update_all(self.depth)
        print "Done updating"
 
    
    def getFrame(self):
        """
        Returns the most recent frame from the kinects IR camera.
        """ 
        self.update()
        return Image.fromstring('P',( 640, 480 ), self.depth.get_raw_depth_map())



    def getNumpyArray(self):
        """
        Returns a numpy array representation of the current frame.
        """
        print "Creating Numpy array of depth Map:..."

        self.update()
        #return array(self.depth.get_tuple_depth_map(), dtype='uint16')
        return fromstring(self.depth.get_raw_depth_map(), dtype='uint8')



    def getSurf(self):
        """
        Returns a surface of most recent frame from the kinects IR camera.
        """       
        depImg = self.rainbowSurf()
        depImg.shape = (480, 640, 3)

        pi = Image.fromarray(depImg)
        pi.show()
        print 'Max: ', max(fromstring(self.depth.get_raw_depth_map_8()))
        pi2 = Image.fromstring('L',( 640, 480 ), self.depth.get_raw_depth_map_8())        
        pi2.show()
        return pygame.image.fromstring(depImg.tostring(), (640, 480), 'RGB')



    def getDepthMap(self):
        """
        Return the depth matrix
        """


    def draw(self):
        """
        For debuggin, used to draw map to the screen in this file.
        """
        screen.blit(self.getSurf(), (0, 0))
        pygame.display.flip()



    def rainbowSurf(self):
        """
        Returns a rainbow colored depth map as a surface.
        """
        depArray = array(self.depth.map, dtype='uint16')
        #print type(depArray[1])

        vFunc = vectorize(colorFunc, otypes=[ndarray])
        depArray2 = vstack(vFunc(depArray))
        
        depArray2.shape = (480, 640, 3)
        print "Max: ", max(depArray)

        return depArray2
        


