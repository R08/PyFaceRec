"""
Kinect Camera Interface
"""
from openni import *
import pygame
from PIL import Image
from HW_Interface import *
import numpy



class RGB_Camera(HW_Interface):
    """
    Provides basic interaction with the kinect's RGB camera.
    """
    img = ImageGenerator()      # Image Generator



    def __init__(self):
        """
        Create and attach an image generator to the context node.
        """
        print "Initalizing Image Generator for RGB Camera."
        self.img.create(self.ctx)
        self.ctx.start_generating_all()


        # Needed to draw with pygame
        WINSIZE = 640,480
        self.screen = pygame.display.set_mode(WINSIZE,0,8)



    def update(self):
        """
        Updates the image generator node.
        """
        err = self.ctx.wait_one_update_all(self.img)
       


    def getString(self):
        """
        Retruns the string representation of the most current RGB image.
        """
        self.update()
        return self.img.get_raw_image_map()



    def getFrame(self):
        """
        Returns the most recent frame from the kinects RGB camera as an 
            RGB image. 
        """
        self.update()
        return Image.fromstring('RGB', (640, 480), self.getString())



    def getNumpyArray(self):
        """
        Returns a numpy array representation of the current frame.
        """
        self.update()
        np = numpy.array(self.img.get_tuple_image_map(), dtype='uint8')
        np.shape = (480, 640, 3)
        return np



    def getSurf(self):
        """
        Returns a python surface of the most recent frame from the kinects
            RGB camera.
        """
        im = self.getFrame()
        return pygame.image.fromstring(self.getString(), (640, 480), im.mode)
       


    def draw(self):
        """
        Draws the current frame in a pygame window.
        """
        self.screen.blit(self.getSurf(), (0, 0))
        pygame.display.flip()
