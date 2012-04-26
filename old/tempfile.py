from openni import *
from itk import *
from PIL import *
import IR_Interface
import numpy
from HW_Interface import *



image_type = itk.Image[itk.SS, 2]
itk_py_converter = itk.PyBuffer[image_type]

ctx = Context()
ctx.init()

IR = IR_Camera()
depimg = IR.getNumpyArray()


image_array = itk_py_converter.GetImageFromArray(depimg.tolist())

print type(image_array)
