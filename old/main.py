#!/usr/bin/python2


from openni import *
import pygame
import numpy
import cv2
from PIL import Image


#--------------------
#   Globals 
#--------------------

# Stuff to draw with pygame
WINSIZE = 640,480
screen = pygame.display.set_mode(WINSIZE,0,8) 


# Create and initalize openNI context node.
ctx = Context()
ctx.init()

# Create an image generator
img = ImageGenerator()
img.create(ctx)

# Create a depth generator
depth = DepthGenerator()
depth.create(ctx)

# Set it to VGA maps at 30 FPS
depth.set_resolution_preset(RES_VGA)
depth.fps = 30


# Create the user generator
user = UserGenerator()
user.create(ctx)


# Pose to use to calibrate the user
pose_to_use = 'Psi'


# Obtain the skeleton & pose detection capabilities
skel_cap = user.skeleton_cap
pose_cap = user.pose_detection_cap



def getRGB_Frame(g_im):
    """Returns the RGB image from the from the camera."""
    return Image.fromstring('RGB', (640, 480), g_im.get_raw_image_map()) 


def imGen2array(g_im):
    """Returns the numpy array representation from a given ImageGenerator."""
    #surf = pygame.image.fromstring(g_im.get_synced_image_map(), (g_im.res[0], g_im.res[1]), "RGB")
    #array = pygame.surfarray.array3d(surf)
    #return array
    return numpy.fromstring(g_im.get_synced_image_map(), dtype='float16')



def array2Gray(a):
    """Returns a grayscaled copy of the array representation of an image"""
    return cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)


# Declare the callbacks
def new_user(src, id):
    print "1/4 User {} detected. Looking for pose..." .format(id)
    pose_cap.start_detection(pose_to_use, id)



def pose_detected(src, pose, id):
    print "2/4 Detected pose {} on user {}. Requesting calibration..." .format(pose,id)
    pose_cap.stop_detection(id)
    skel_cap.request_calibration(id, True)



def calibration_start(src, id):
    print "3/4 Calibration started for user {}." .format(id)




def calibration_complete(src, id, status):
    if status == CALIBRATION_STATUS_OK:
        print "4/4 User {} calibrated successfully! Starting to track." .format(id)
        skel_cap.start_tracking(id)
    else:
        print "ERR User {} failed to calibrate. Restarting process." .format(id)
        new_user(user, id)



def lost_user(src, id):
    print "--- User {} lost." .format(id)




# Register them
user.register_user_cb(new_user, lost_user)
pose_cap.register_pose_detected_cb(pose_detected)
skel_cap.register_c_start_cb(calibration_start)
skel_cap.register_c_complete_cb(calibration_complete)

# Set the profile
skel_cap.set_profile(SKEL_PROFILE_ALL)



# Start generating
ctx.start_generating_all()
print "0/4 Starting to detect users. Press Ctrl-C to exit."





# Main Loop
while True:

    
    # Extract head position of each tracked user
    for id in user.users:
        if skel_cap.is_tracking(id):
            head = skel_cap.get_joint_position(id, SKEL_HEAD)
            print "  {}: head at ({loc[0]}, {loc[1]}, {loc[2]}) [{conf}]" .format(id, loc=head.point, conf=head.confidence)


    
    # Update
    nRetVal = ctx.wait_one_update_all(img)
    #img_rgb = img.get_synced_image_map()
    depthMap = depth.map
    #im_a = imGen2array(img)
    #im_g = array2Gray(im_a)
    im = getRGB_Frame(img)
    surf = pygame.image.frombuffer(im.tostring(),(640,480), im.mode)
    
 
    # Draw
    screen.blit(surf, (0, 0))
    pygame.display.flip()

