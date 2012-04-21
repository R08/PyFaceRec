"""
Kinect IR Camera Interface
"""
from openni import *
import pygame
from PIL import Image


# Start Context Node.
ctx = Context()
ctx.init()

class IR_Camera():
    """
    Provides basic interaction with the kinects IR camera.
    """
    depth = DepthGenerator()


    def __init__(self):
        """
        Create and attach an image generator to the context node.
        """
        print "initalizing generatiors"
        self.depth.create(ctx)
        ctx.start_generating_all()


    def update(self):
        """
        Updates the Depth generator node.
        """
        print "updating cam"
        err = ctx.wait_and_update_all()
 
    
    def getFrame(self):
        """
        Returns the most recent frame from the kinects IR camera.
        """ 
        print "getting frame"
        self.update()
        return Image.fromstring('P', (640, 480), depth.get_raw_depth_map_8())


    def getSurf(self):
        """
        Returns a surface of most recent frame from the kinects IR camera.
        """
        print "getting Surface"
        depImg = self.getFrame()
        depImg.convert("RGB")

        return pygame.image.fromstring(depImg.tostring(), (640, 480), depImg.mode)



    #def drawSurf(self):
        #screen.blit(self.getSurf(), (0, 0))
        
