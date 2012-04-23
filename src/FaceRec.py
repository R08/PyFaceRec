"""
    This source file defines the classes and functions needed to preform
facial recognition.
"""

import cv2           # OpenCV - Computer vision library
from cv2 import cv   # Legacy support for opencv ver. < 2.x
from PIL import Image
from PIL import ImageFilter
from PIL import ImageOps
from PIL.ImageColor import getrgb
import numpy as np

class FaceDataSet():
    """
    Holds a RGB image, a depth image, and coordinates that defines the location
    of the face.
    """

    img_RGB = None
    img_IR = None

    # Defines a square which contains a face by the upper left 
    #   vertex (x1, y1), and the lower right (x2, y2)
    coords = None


    
#    def __init__(self, RGB, IR, coords):
        
        #self.RGB = RGB
        #self.IR = IR
        #self.coords = coords    



class HaarDetectFace():
    """
    Defines methods needed to detect a face in a given RGB image.
    """
    
    
    cascade_fn = "../data/haarcascades/haarcascade_frontalface_default.xml"
    nested_fn  = "../data/haarcascades/haarcascade_eye.xml"

    cascade = cv2.CascadeClassifier(cascade_fn)
    nested = cv2.CascadeClassifier(nested_fn)



    def detect(self, img, cascade):
        """
        Preforms the actual face detection given an image and a cascade 
          classifier. Returns an array of sub arrays that define the coordinates
          of a square(s) [[x1, y1, x2, y2],[...]]
        """
        rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, 
                                 minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
        if len(rects) == 0:
            return []
        
        rects[:,2:] += rects[:,:2]
        return rects



    def draw_rects(self, img, rects, color):
        """
        Draws a square of of a given color at a given location on a given image.
        """
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)





    def getFrame(self, RGB, IR):
        """
        Returns an image represented as an array with green squares drawn 
          around any found faces when given an RGB_Camera object.
        """
        # Get image and prepare for face detection
        img = RGB.getNumpyArray()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        #small_rect = np.array([0, 0, 0, 0]).astype(np.uint32)
        rects = self.detect(gray, self.cascade)
        if len(rects) > 0:
            rect = rects[0]
            x = (rect[3] - rect[1])/2
            y = (rect[2] - rect[0])/2
            print x, y
            if x > 0 and x < 640 and y > 0 and y < 480:
                print IR.getDepthMap()[int(x), int(y)]
                #small_rect = np.array([x, x+2, y, y+2]).astype(np.uint32)




        
        vis = img.copy()
        #self.draw_rects(vis, small_rect, (255, 0, 0))
        self.draw_rects(vis, rects, (0, 255, 0))
        #print type(rects[0])


        for x1, y1, x2, y2 in rects:
            roi = gray[y1:y2, x1:x2]
            vis_roi = vis[y1:y2, x1:x2]
            #subrects = detect(roi.copy(), nested)
            #draw_rects(vis_roi, subrects, (255, 0, 0))


        return (vis, rects)




    def getCropedFaceImg(self, RGB, IR):
        """
        Returns a croped image represented as an array containing the first face found.
        """

        
        frame = self.getFrame(RGB, IR)
        
        vis = IR.getNumpyArray()
        rects = frame[1]
        print 'IR shape: ', vis.shape

        tol = 20
        if len(rects) > 0:
            rect = rects[0]
            vis = vis[rect[1]-tol:rect[3]+tol, rect[0]-tol+tol/2:rect[2]+tol*2]

            pi = Image.fromstring('L', (vis.shape[1], vis.shape[0]), vis.tostring())

            # Apply filters and effects
            pi2 = pi.filter(ImageFilter.MedianFilter(7))
            pi2.convert('RGB')
            pi2 = ImageOps.equalize(pi2)
            #r, g, b = getrgb(color)
            pi2 = ImageOps.colorize(pi2, "black", "yellow")
            #pi2 = ImageOps.colorize(pi2, (0,0,0), (255,255,255))


            # Display images
            pi.show() 
            pi2.show()
            return vis




class FaceRec():
    """
    This class contains methods needed to identify a face.
    """
    
    cur_data_set = FaceDataSet()

#    def __init__(self, data_set):
        #self.cur_data_set = data_set



    def preprocess(self):
        """
        Preforms preprocessing on the images to remove and/or correct
          any artifacts or abnormalities.
        """

        print "Preprocessing goes here"




    def faceRec(self):
        """
        Attemts to recognize and match face to a face that is already known
          by the system.
        """

        print "Facial recognition goes here"

