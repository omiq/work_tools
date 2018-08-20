import _thread
import sys
import os
import RPi.GPIO as GPIO
import requests
import time
import picamera
import pygame
import tweeter
import tkinter as tk
from PIL import ImageTk, Image

# We are going to use the BCM numbering
GPIO.setmode(GPIO.BCM)

# Set pin 26 as input using pull up resistor
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Load up the shutter sound effect
pygame.mixer.init()


# get an image source for a given attachment ID
def get_url(image_id):
    url = "http://photome.io/wp-json/wp/v2/media/" + str(image_id)
    response = requests.get(url)
    #print(response.json())
    return response.json()['guid']['rendered']


# create WP post
def create_post(image_id):

    # get just the filename
    slug = image_id

    # get the raw URL for the attachment
    image_url = get_url(image_id)

    # this line needs to be changed to the correct site - REST API
    # does not work on WPE so using SPS
    # url = "http://geekahol.com/wp-json/wp/v2/media/?title=" + slug
    # url = "http://booth2018.wpengine.com/wp-json/wp/v2/media/?title=" + slug
    url = "http://photome.io/wp-json/wp/v2/posts/"

    # set up the parameters - basic login details from the environment variables
    user = os.environ['WP_USER']
    password = os.environ['WP_PASS']
    form_data = {
        'title': slug,
        'body': '<img src="' + image_url + '">',
        'status': 'publish',
        'featured_media': image_id,
        'post_meta': { "key": "_thumbnail_id",
                       "value":  image_id }
    }

    # send the data and get the response back
    response = requests.request(
        "POST",
        url,
        data=form_data,
        auth=(user, password))

    if (response.status_code == 403):
        print(response)
        exit()

    # parse the response via the JSON library
    json = response.json()

    return json['guid']['rendered']


# upload a selected image to WP
def upload_image(image):
    # did the user supply an image file?
    if image == "":
        print(sys.argv)
        input("You must supply an image file!")
        exit()

    # get just the filename
    slug = os.path.basename(image)

    # this line needs to be changed to the correct site - REST API
    # does not work on WPE so using SPS
    # url = "http://geekahol.com/wp-json/wp/v2/media/?title=" + slug
    # url = "http://booth2018.wpengine.com/wp-json/wp/v2/media/?title=" + slug
    url = "http://photome.io/wp-json/wp/v2/media/?title=" + slug

    # the headers for the request (right now hard coded to be JPG because photographs)
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
    user = os.environ['WP_USER']
    password = os.environ['WP_PASS']

    # send the data and get the response back
    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=file_data,
        auth=(user, password))

    if (response.status_code == 403):
        print(response)
        exit()

    # parse the response via the JSON library
    json = response.json()
    # guid = json.get('guid')
    attachment_id = json.get('id')
    #url = guid.get('raw')

    return attachment_id


# show preview of the webcam on screen
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


# display the captured image on screen
def display_captured(file):

    sys.stdout.write(u"\x1b[2J\x1b[H\u001b[41;1m" + "Uploading ...\n\n\n\n\u001b[0m")

    # transfer the file
    image_id = upload_image(file)
    response = create_post(image_id)
    print(response)

    # success sound
    pygame.mixer.music.load("tada.mp3")

    # gui window
    window = tk.Tk()
    window.attributes("-fullscreen", True)
    window.minsize(1920, 1080)
    window.bind("<Button>", clicked)
    window.bind("<Key>", key_press)
    pic = ImageTk.PhotoImage(Image.open(file))
    image_widget = tk.Label(window, image=pic)
    image_widget.place(x=0, y=0, width=1920, height=1080)
    window.update()
    window.minsize(1920, 1080)
    window.after(3000, lambda: window.destroy())
    pygame.mixer.music.play()
    window.mainloop()


# snap the picture
def capture(camera, file):
    pygame.mixer.music.load("shutter.mp3")
    pygame.mixer.music.play()
    camera.resolution = (1920, 1080)
    camera.capture(file, 'jpeg')
    camera.resolution = (1280, 720)


# tweet the pic
def tweet(file):
    # create TwitterClient object
    api = tweeter.TwitterClient()

    # set the content
    tweet_txt = "@makerhacks look at this #test "

    # tweet
    response = api.tweet_image(file, tweet_txt)


# main loop
def main():
        camera = picamera.PiCamera(resolution=(1280, 720))
        camera.vflip = True
        camera.hflip = True
        camera.awb_mode = 'auto'
        camera.exposure_mode = 'sports'

        img = Image.open('overlay.png')
        overlay = camera.add_overlay(img.tobytes(), layer=3, alpha=100)
        camera.preview_fullscreen = True

        # thread to show the camera preview in background process
        preview = _thread.start_new_thread(preview_camera, (camera,))

        # infinite loop to check the GPIO pins for button press
        while 1:
            if not GPIO.input(26):
                camera.remove_overlay(overlay)
                camera.stop_preview()

                file = "./pictures/booth_{}.jpg".format(time.time())

                capture(camera, file)

                display_captured(file)

                tweet(file)

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

        # main loop
        main()

        '''file = "./pictures/picture.jpg"
        print(display_captured(file))
        #print(upload_image(file))'''
