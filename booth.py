import _thread
import sys
import os
import RPi.GPIO as GPIO
import requests
import time
import pyperclip
import picamera
import pygame
import tkinter as tk
from PIL import ImageTk, Image
from requests_oauthlib import OAuth1

# We are going to use the BCM numbering
GPIO.setmode(GPIO.BCM)

# Set pin 26 as input using pull up resistor
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Load up the shutter sound effect
pygame.mixer.init()


# upload a selected image to WP
def upload_image(image):
    # did the user supply an image file?
    if image == "":
        print(sys.argv)
        input("You must supply an image file!")
        exit()

    # get just the filename
    slug = os.path.basename(image)

    # this line needs to be changed to YOUR wp site
    url = "http://booth2018.wpengine.com/wp-json/wp/v2/media/?title=" + slug

    # the headers for the request (right now hard coded to be JPG because that is all I need)
    headers = {
        'Content-Type': "image/jpg",
        'content-disposition': "attachment; filename=" + slug,
        'Cache-Control': "no-cache",
        }

    # get the image file data
    try:
        file_data = open(image, 'rb')
    except:
        input("Can't load {} - aborting!".format(image))
        exit()

    # set up the parameters - basic login details from the environment variables
    files = {'file': file_data}
    oauth_token = os.environ['oauth_token']
    oauth_token_secret = os.environ['oauth_token_secret']
    client_key = os.environ['client_key']
    client_secret = os.environ['client_secret']

    auth = OAuth1(client_key, client_secret, oauth_token, oauth_token_secret)


    # send the data and get the response back
    response = requests.post(url,
        headers=headers,
        data=file_data,
        auth=auth)

    print(dir(response))
    print(response.content)


    # parse the response via the JSON library
    json = response.json()
    guid = json.get('guid')
    url = guid.get('raw')

    # display the generated image URL and copy
    # to clipboard. Should just work on mac/win
    # Ubuntu clipboard is pretty crap so you will need
    # xclip and Parcellite to make it usable
    pyperclip.copy(url)
    return url


def preview_camera(camera):

    camera.start_preview()
    time.sleep(5)

    while 1:
        #do nothing
        foo=False


def event_action(event):
    event.widget.quit()


def clicked(event):
    event_action(event)


def key_press(event):
    event_action(event)


def display_captured(file):

    sys.stdout.write(u"\x1b[2J\x1b[H\u001b[41;1m" + "Uploading ...\n\n\n\n\u001b[0m")

    # transfer the file
    uploaded = upload_image(file)
    print(uploaded)

    pygame.mixer.music.load("tada.mp3")

    # gui window
    window = tk.Tk()
    window.attributes("-fullscreen", True)
    window.bind("<Button>", clicked)
    window.bind("<Key>", key_press)
    pic = ImageTk.PhotoImage(Image.open(file))
    image_widget = tk.Label(window, image=pic)
    image_widget.place(x=0, y=0, width=1920, height=1080)
    window.after(3000, lambda: window.destroy())
    pygame.mixer.music.play()
    window.mainloop()


def capture(camera, file):
    pygame.mixer.music.load("shutter.mp3")
    pygame.mixer.music.play()
    camera.resolution = (1920, 1080)
    camera.capture(file, 'jpeg')
    camera.resolution = (1280, 720)


def main():
        camera = picamera.PiCamera(resolution=(1280, 720))
        camera.vflip = True
        camera.hflip = True
        camera.awb_mode = 'auto'
        camera.exposure_mode = 'sports'

        img = Image.open('overlay.png')
        overlay = camera.add_overlay(img.tobytes(), layer=3, alpha=100)
        camera.preview_fullscreen = True

        preview = _thread.start_new_thread(preview_camera, (camera,))

        while 1:
            if not GPIO.input(26):
                camera.remove_overlay(overlay)
                camera.stop_preview()

                file = "./pictures/booth_{}.jpg".format(time.time())

                capture(camera, file)

                display_captured(file)

                for x in range(0, 10):
                    sys.stdout.write(u"\u001b[1000D" + "SNAP!!")

                overlay = camera.add_overlay(img.tobytes(), layer=3, alpha=100)
                camera.start_preview()

            else:

                if time.time() % 2 > 0:
                    sys.stdout.write(u"\x1b[2J\x1b[H\u001b[47;1m" + "Waiting")
                else:
                    sys.stdout.write(u"\x1b[2J\x1b[H\u001b[47;1m" + "Waiting ..")


if __name__ == "__main__":
        #main()

        file = "./pictures/picture.jpg"
        #display_captured(file)
        print(upload_image(file))
