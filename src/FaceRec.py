"""
    This source file defines the classes and functions needed to preform
facial recognition.
"""



class FaceDataSet():
    """
    Holds a RGB image, a depth image, and coordinates that defines the location
    of the face.
    """

    RGB = None
    IR = None

    # Defines a square which contains a face by the upper left 
    #   vertex (x1, y1), and the lower right (x2, y2)
    coords = None


    
    def __init__(self, RGB, IR, coords):
        
        self.RGB = RGB
        self.IR = IR
        self.coords = coords    




class FaceRec():
    """
    This class contains methods needed to identify a face.
    """
    
    cur_data_set = FaceDataSet()

    def __init__(self, data_set):
        self.cur_data_set = data_set



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

