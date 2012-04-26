"""
Kinect RGB Camera Interface
"""
from openni import *
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
        Retruns the binary string representation of the most current RGB image.
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
        np = numpy.fromstring(self.img.get_raw_image_map(), dtype='uint8')
        np.shape = (480, 640, 3)
        return np
       


    def imShow(self):
        """
        Uses PIL to display the most recent frame
        """
        im = self.getFrame()
        im.imshow()




    def draw(self, screen):
        return None
