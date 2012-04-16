#!/usr/bin/python2


from openni import *
import pygame


#--------------------
#   Globals
#--------------------
#screen
#surf


#def initOpenNI():
ctx = Context()
ctx.init()

# Create an image generator
img = ImageGenerator()
img.create(ctx)

# Start generating
ctx.start_generating_all()


WINSIZE = 640,480
screen = pygame.display.set_mode(WINSIZE,0,8)



while True:
    
    # Update
    nRetVal = ctx.wait_one_update_all(img)
    img_rgb = img.get_synced_image_map()
    surf = pygame.image.frombuffer(img_rgb,(640,480), 'RGB')
 
    # Draw
    screen.blit(surf, (0, 0))
    pygame.display.flip()

