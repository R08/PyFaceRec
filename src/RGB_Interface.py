"""
Kinect Camera Interface
"""
from openni import *
import pygame
from PIL import Image
from PIL import *
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
        Returns the most recent frame from the kinects RGB camera as a 
            PIL image with the RGB mode. 
        """
        self.update()
        return Image.fromstring('RGB', (640, 480), self.getString())



    def getNumpyArray(self):
        """
        Returns a numpy array representation of the current frame.
        """
        self.update()
        #np = numpy.array(self.img.get_tuple_image_map(), dtype='uint8')
        np = numpy.fromstring(self.img.get_raw_image_map(), dtype='uint8')
        np.shape = (480, 640, 3)
        return np



    def getSurf(self):
        """
        Returns a pygame surface of the most recent frame from the kinects
            RGB camera.
        """
        im = self.getFrame()
        return pygame.image.fromstring(self.getString(), (640, 480), im.mode)
       


    def imShow(self):
        im = self.getFrame()
        im.imshow()

    def draw(self, screen):
        """
        Draws the current frame in a pygame window.
        """
        screen.blit(self.getSurf(), (0, 0))
        pygame.display.flip()
