#!/usr/bin/python2


from RGB_Interface import *
from PIL import *


# Stuff to draw with pygame
WINSIZE = 640,480
screen = pygame.display.set_mode(WINSIZE,0,8) 


cam = RGB_Camera()

cam.getSurf()

#img = cam.getFrame()

#img.show()

# Main loop
while True:
   # Update
    #nRetVal = ctx.wait_one_update_all(img)
    surf = cam.getSurf()
    # Draw
    screen.blit(surf, (0, 0))
    pygame.display.flip()
