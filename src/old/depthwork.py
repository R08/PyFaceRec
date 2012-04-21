#!/usr/bin/python2

#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
#                                                                      #
#                                                                      #
#                                                                      #
#                                                                      #
#                                                                      #
#                                                                      #
#                                                                      #
#                                                                      #
#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

from openni import *
from PIL import Image
import cv2
import numpy
import pygame
import ImageDraw


#------------------------------------------------
#   Globals 
#------------------------------------------------

# Stuff to draw with pygame
WINSIZE = 640,480
screen = pygame.display.set_mode(WINSIZE)

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

## Create the user generator
user = UserGenerator()
user.create(ctx)

## Pose to use to calibrate the user
pose_to_use = 'Psi'

## Obtain the skeleton & pose detection capabilities
skel_cap = user.skeleton_cap
pose_cap = user.pose_detection_cap


#------------------------------------------------
#    Callbacks
#------------------------------------------------
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


#------------------------------------------------
#    Runtime
#------------------------------------------------

## Set the profile
skel_cap.set_profile(SKEL_PROFILE_ALL)

# Start generating
ctx.start_generating_all()
print "0/4 Starting to detect users. Press Ctrl-C to exit."

#initiate display
pygame.display.init()


#------------------------------------------------
# Main Loop
#------------------------------------------------
while True:

    # Update
    nRetVal = ctx.wait_and_update_all()

    # Extract head position of each tracked user
    #for id in user.users:
        #if skel_cap.is_tracking(id):
            #head = skel_cap.get_joint_position(id, SKEL_HEAD)

            
    print "  {}: head at ({loc[0]}, {loc[1]}, {loc[2]}) [{conf}]" .format(id, loc=head.point, conf=head.confidence)

    img_rgb = img.get_synced_image_map()
    im_a = imGen2array(img)
    im_g = array2Gray(im_a)
    im = getRGB_Frame(img)
    surf = pygame.image.frombuffer(im.tostring(),(640,480), im.mode)
    
    # Draw
    screen.blit(surf, (0, 0))
    pygame.display.flip()

