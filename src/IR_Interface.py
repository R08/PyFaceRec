"""
Kinect IR Camera Interface
"""
from openni import *
from PIL import *
from numpy import * 
from HW_Interface import *




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
        self.depth.create(self.ctx)
        self.depth.set_resolution_preset(RES_VGA)
        self.depth.fps = 30
        self.ctx.start_generating_all()




    def update(self):
        """
        Updates the Depth generator node.
        """
        print "Updating Depth Generator..."

        err = self.ctx.wait_one_update_all(self.depth)
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
        a = fromstring(self.depth.get_raw_depth_map(), dtype='uint16')
        a.shape = (480, 640)
        a = a.astype(uint8)
        return a




    def getDepthMap(self):
        """
        Return the depth matrix
        """
        return self.depth.map




    def draw(self):
        """
        For debuggin, used to draw map to the screen in this file.
        """
        return None


   
   
    def rainbowSurf(self):
        """
        Returns a rainbow colored depth map as a surface.
        """
        depArray = array(self.depth.map, dtype='uint16')

        vFunc = vectorize(colorFunc, otypes=[ndarray])
        depArray2 = vstack(vFunc(depArray))
        
        depArray2.shape = (480, 640, 3)
        print "Max: ", max(depArray)

        return depArray2
        


