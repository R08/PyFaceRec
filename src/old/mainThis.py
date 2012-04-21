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
#WINSIZE = 640,480
#screen = pygame.display.set_mode(WINSIZE) 


# Create and initalize openNI context node.
ctx = Context()
ctx.init()

# Create an image generator
#img = ImageGenerator()
#img.create(ctx)

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

## Set the profile
skel_cap.set_profile(SKEL_PROFILE_ALL)

# Start generating
ctx.start_generating_all()
print "0/4 Starting to detect users. Press Ctrl-C to exit."

#initiate display
#pygame.display.init()

    # Extract head position of each tracked user
    for id in user.users:
        if skel_cap.is_tracking(id):
            head = skel_cap.get_joint_position(id, SKEL_HEAD)
# Main Loop
while True:

    # Update
    nRetVal = ctx.wait_and_update_all()


    head = skel_cap.get_joint_position(id, SKEL_HEAD)
            
    p = Image.fromstring('P', (640, 480), depth.get_raw_depth_map_8())
    p = p.convert("RGB")
    draw = ImageDraw.Draw(p)
    draw.ellipse((head.point[0],head.point[1],12,25), outline="red")
    surf = pygame.image.fromstring(p.tostring(), (640, 480), 'RGB')
            
    screen.blit(surf,(0,0))
    pygame.display.flip()
    print "  {}: head at ({loc[0]}, {loc[1]}, {loc[2]}) [{conf}]" .format(id, loc=head.point, conf=head.confidence)

    


#########
#p.show()

#img_rgb = imGen2numpy(img)
            #depthMap = depth.map

            #print type(depthMap), ' ', depthMap.shape

            #Mx = numpy.max(depthMap)
            #Mn = numpy.min(depthMap)

            #temp1 = numpy.matrix(depthMap)
            #temp2 = Mx/240
            #temp1 = temp1/temp2

            ##numpy.trunc(temp1)
            #temp1.resize(640,480)#img_rgb = imGen2numpy(img)
            #depthMap = depth.map

            #print type(depthMap), ' ', depthMap.shape

            #Mx = numpy.max(depthMap)
            #Mn = numpy.min(depthMap)

            #temp1 = numpy.matrix(depthMap)
            #temp2 = Mx/240
            #temp1 = temp1/temp2

            ##numpy.trunc(temp1)
            #temp1.resize(640,480)
            #print temp1, ' ', temp1.max(), ' ', temp1.min()
            #print temp1.shape

            #temp1 = numpy.array(temp1, dtype='uint8')
            ##temp1 = numpy.array.tostring(temp1)
            ##$temp1 = temp1.tostring()

            #print temp1


            #temp1 = Image.fromarray(temp1, "L")

            #print temp1, ' ', temp1.max(), ' ', temp1.min()
            #print temp1.shape

            #temp1 = numpy.array(temp1, dtype='uint8')
            ##temp1 = numpy.array.tostring(temp1)
            ##$temp1 = temp1.tostring()

            #print temp1


            #temp1 = Image.fromarray(temp1, "L")
            ##temp1 = temp1.convert("DodgerBlue")



    # Extract head position of each tracked user
    #for id in user.users:
        #if skel_cap.is_tracking(id):
            #head = skel_cap.get_joint_position(id, SKEL_HEAD)


#def imGen2numpy(g_im):
    #"""Returns the numpy array representation from a given ImageGenerator."""
    #return numpy.fromstring(g_im.get_synced_image_map())


## Register them
#user.register_user_cb(new_user, lost_user)
#pose_cap.register_pose_detected_cb(pose_detected)
#skel_cap.register_c_start_cb(calibration_start)
#skel_cap.register_c_complete_cb(calibration_complete)

