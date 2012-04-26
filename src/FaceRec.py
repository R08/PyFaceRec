"""
    This source file defines the classes and functions needed to preform
facial recognition.
"""

import cv2           # OpenCV - Computer vision library
from cv2 import cv   # Legacy support for opencv ver. < 2.x
from PIL import Image
from PIL import ImageFilter
from PIL import ImageOps
from PIL import *
import ImageDraw
from PIL.ImageColor import getrgb
#from PIL import convert
import numpy as np
from math import floor

#from scipy.interpolate import girddata







def draw_rects(self, img, rects, color):
    """
    Draws a square of of a given color at a given location on a given image.
    """
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)









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
            x = (rect[0] + rect[1])/2
            y = (rect[2] + rect[3])/2
            #print x, y
            if x > 0 and x < 640 and y > 0 and y < 480:
                d = IR.getDepthMap()[int(x), int(y)]
                #if d > 0:
                    #print "Face depth from camera: ", d
                #small_rect = np.array([x, x+2, y, y+2]).astype(np.uint32)




        
        vis = img.copy()
        #self.draw_rects(vis, small_rect, (255, 0, 0))
        self.draw_rects(vis, rects, (0, 255, 0))
        #print type(rects[0])


        for x1, y1, x2, y2 in rects:
            roi = gray[y1:y2, x1:x2]
            vis_roi = vis[y1:y2, x1:x2]
            subrects = self.detect(roi.copy(), self.nested)
            self.draw_rects(vis_roi, subrects, (255, 0, 0))


        return (vis, rects)




    def getCropedFaceImg(self, RGB, IR):
        """
        Returns a croped image represented as an array containing the first face found.
        """

        
        frame = self.getFrame(RGB, IR)
        
        vis = np.array(IR.getDepthMap(), dtype='int')#.getNumpyArray()
        #print type(vis[0])
        vis.shape = (480, 640)

        rects = frame[1]
        #print 'IR shape: ', vis.shape

        tol = 20
        if len(rects) > 0:
            rect = rects[0]
            vis = vis[rect[1]-tol:rect[3]+tol, rect[0]-tol+tol/2:rect[2]+tol*2]

            #pi = Image.fromstring('L', (vis.shape[1], vis.shape[0]), vis.tostring())

            print vis.shape
            # Display images
            #pi.show() 
            #pi2.show()
            return vis




class FaceRec():
    """
    This class contains methods needed to identify a face.
    """
    
    cur_data_set = FaceDataSet()

#    def __init__(self, data_set):
        #self.cur_data_set = data_set



    def preprocess(self, vis):
        """
        Preforms preprocessing on the images to remove and/or correct
          any artifacts or abnormalities.
        """

        vis2 = vis.astype(np.uint8)
        pi = Image.fromstring('L', (vis2.shape[1], vis2.shape[0]), vis2.tostring())
        #pi.show()


        # Apply filters and effects
        pi = pi.filter(ImageFilter.MedianFilter(7))
        #pi.show()
        pi.convert('RGB')
        pi = ImageOps.equalize(pi)
        #pi.show()
        pi = ImageOps.colorize(pi, "black", "yellow")
        
        #pi.show()


        a = np.array(vis, dtype='int')
        #a.astype(np.uint32)

        def findMin(a):
            if a < 20:
                return 30000 

            else:
                return a


        vecfunc = np.vectorize(findMin)
        row_shape = a.shape[1]
        col_shape = a.shape[0]

        a = a.reshape(-1, 1) 
        #print "SHAPE: ", a.shape
        #print a
        a_min = vecfunc(a)
        min_value = np.amin(a_min)

        
        a_min.shape = (row_shape, col_shape)
        a_min_index = np.argmin(a_min)
        
        row_index = int(a_min_index % row_shape)
        col_index = int(floor(a_min_index / col_shape))

        print "MIN: ", min_value
        print "Min index (nose position): (" , row_index, ", ", col_index, ")"

        #draw = ImageDraw.Draw(pi)
        #draw.line([row_index, col_index])#, (255, 0, 0))
        #pi.show()
        # Change to pil form and resize
        a2 = np.fromstring(pi.tostring(), dtype='uint8')
        print a2.shape
        a2.shape = (col_shape, row_shape, 3)
        cv2.rectangle(a2, (row_index, col_index), (row_index+2, col_index+2), (255, 0, 0) , 2)

        pi = Image.fromstring('RGB', (row_shape, col_shape), a2.tostring())
        pi.show()
        #a.astype(np.uint8)
        
        #pi = Image.fromarray(a2).convert('RGB')
        #pi.show()
        #pi = Image.fromstring('L', (row_shape, col_shape), a)
        #pi2 = ImageOps.fit(pi, (200, 200))
        #pi2.show()

        #return (row_index, col_index)



    def faceRec(self):
        """
        Attemts to recognize and match face to a face that is already known
          by the system.
        """

        print "Facial recognition goes here"

