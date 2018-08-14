import _thread
import sys
import os
import RPi.GPIO as GPIO
import requests
import time
import pyperclip
import picamera
from picamera import color
import tkinter as tk
from PIL import ImageTk, Image

# We are going to use the BCM numbering
GPIO.setmode(GPIO.BCM)

# Set pin 26 as input using pull up resistor
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)


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
    url = "https://makerhacks.com/wp-json/wp/v2/media/?title=" + slug

    # the headers for the request (right now hard coded to be PNG because that is all I need)
    headers = {
        'Content-Type': "image/png",
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
    user = os.environ['WPUSER']
    password = os.environ['WPPASS']

    # send the data and get the response back
    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=file_data,
        auth=(user, password))

    # parse the response via the JSON library
    json = response.json()
    guid = json.get('guid')
    url = guid.get('raw')

    # display the generated image URL and copy
    # to clipboard. Should just work on mac/win
    # Ubuntu clipboard is pretty crap so you will need
    # xclip and Parcellite to make it usable
    print(url)
    pyperclip.copy(url)
    time.sleep(5)
    return url


def preview(camera):

    camera.start_preview()
    time.sleep(5)

    while 1:
        #do nothing
        foo=False


def event_action(event):
    print(repr(event))
    event.widget.quit()


def clicked(event):
    event_action(event)


def key_press(event):
    event_action(event)


def captured():
    window = tk.Tk()
    window.attributes("-fullscreen", True)
    window.bind("<Button>", clicked)
    window.bind("<Key>", key_press)
    pic = ImageTk.PhotoImage(Image.open("./picture.jpg"))
    image_widget = tk.Label(window, image=pic)
    image_widget.place(x=0, y=0, width=1920, height=1080)
    window.mainloop()


def main():
        camera = picamera.PiCamera(resolution=(1280, 720))
        camera.vflip = True
        camera.hflip = True
        camera.awb_mode = 'auto'
        camera.exposure_mode = 'auto'

        img = Image.open('overlay.png')
        camera.add_overlay(img.tobytes(), layer = 3, alpha = 100)
        camera.preview_fullscreen = True


        _thread.start_new_thread(preview, (camera,))

        while 1:
            if not GPIO.input(26):
                camera.stop_preview()
                file = "./picture.jpg"
                camera.resolution = (1920, 1080)
                camera.capture(file, 'jpeg')

                _thread.start_new_thread(captured, ())

                camera.resolution = (1280, 720)
                print("SNAP!!")
                print("SNAP!!")
                print("SNAP!!")
                print("SNAP!!")
                print("SNAP!!")
                print("SNAP!!")
                print("SNAP!!")
                print("SNAP!!")
                print("SNAP!!")
                print("SNAP!!")
                print("SNAP!!")
                print("SNAP!!")
                print("SNAP!!")


                time.sleep(5)
                camera.start_preview()
            else:
                print("Waiting")


if __name__ == "__main__":
        main()
        #captured()

