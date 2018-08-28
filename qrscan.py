import os
import PIL
from PIL import Image
import pyzbar.pyzbar as pyzbar
import pygame
import pygame.camera
from pygame.locals import *


# function that pulls data from the image
def read_codes(source_image):

    # read the QR code(s)
    result = pyzbar.decode(source_image)

    return result


# main function
if __name__ == '__main__':

    # set up pygame object
    pygame.init()

    # initialise
    pygame.camera.init()

    # clock so the loop does not freeze the pi
    clock = pygame.time.Clock()

    # set up our viewing screen
    # screen = pygame.display.set_mode((320, 200), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((320, 200))

    # Fill the screen with red (255, 0, 0)
    red = (255, 0, 0)
    screen.fill(red)

    # Update the display
    pygame.display.set_caption("QR Code Scan")
    pygame.display.update()

    # use the first camera in the list
    # run sudo modprobe bcm2835-v4l2 to install official camera
    camlist = pygame.camera.list_cameras()
    DEVICE = camlist[0]

    # reasonably high res capture, in RGB mode
    SIZE = (320, 200)
    camera = pygame.camera.Camera(DEVICE, SIZE, "RGB")

    # start capture
    camera.start()

    while True:

        # get the image and display it at 0,0
        image = camera.get_image()
        pygame.image.save(image, "input.jpg")
        screen.blit(image, (0, 0))
        pygame.display.update()

        # read the image
        input_image = PIL.Image.open("input.jpg")

        # check the image
        codes = read_codes(input_image)

        # Print results
        for this_code in codes:
            if "QRCODE" == this_code.type:
                print('DETECTED: {}'.format(str(this_code.data)))

        # 60 frames per second - essentially real time
        clock.tick(60)
