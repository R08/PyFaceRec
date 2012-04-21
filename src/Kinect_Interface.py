"""
This file holds all of the class and function definitions need to 
    interact with the kinect hardware.
"""

from openni import *
from PIL import Image


# Create and initalize openNI context node.
ctx = Context()
ctx.init()




class RGB_Camera():
    """
    Provides basic interaction with the kinects RGB camera.
    """

    img = None    # Image Generator
    
    def __init__(self):
        """
        Create and attach an image generator to the context node.
        """
        img = ImageGenerator()
        img.create(ctx)
    


    def update(self):
        """
        Updates the image generator node.
        """
        ctx.wait_one_update_all(self.img)



    def getFrame(self):
        """
        Returns the most recent frame from the kinects RGB camera. 
        """




class IR_Camera():
    def __init__(self):
        # Create a depth generator and attach it to the context node.
        depth = DepthGenerator()
        depth.create(ctx)


