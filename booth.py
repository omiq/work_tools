import _thread
import sys
import os
import RPi.GPIO as GPIO
import requests
import time
import random
import picamera
import pygame
import PIL
import tweeter
import qrscan
import tkinter as tk
from PIL import ImageTk, Image, ImageDraw, ImageFont

# We are going to use the BCM numbering
GPIO.setmode(GPIO.BCM)

# Set pin 26 as input using pull up resistor
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Load up the shutter sound effect
pygame.init()
pygame.mixer.init()
beep = pygame.mixer.Sound("./beep.wav")
tada = pygame.mixer.Sound("./tada.wav")
shutter = pygame.mixer.Sound("./shutter.wav")


# overlay
def make_overlay(camera):

    # Load the arbitrarily sized image
    img = Image.open('overlay.png')

    # Create an image padded to the required size with
    # mode 'RGB'
    pad = Image.new('RGBA', (
        ((img.size[0] + 31) // 32) * 32,
        ((img.size[1] + 15) // 16) * 16,
    ))

    # Paste the original image into the padded one
    pad.paste(img, (0, 0))

    # Add the overlay with the padded image as the source,
    # but the original image's dimensions
    overlay = camera.add_overlay(pad.tobytes(), size=img.size)

    # By default, the overlay is in layer 0, beneath the
    # preview (which defaults to layer 2). Here we make
    # the new overlay semi-transparent, then move it above
    # the preview
    overlay.alpha = 155
    overlay.layer = 3

    return overlay


# get an image source for a given attachment ID
def get_url(image_id):
    url = "https://summitphotoengine.com/wp-json/wp/v2/media/" + str(image_id)
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
    url = "https://summitphotoengine.com/wp-json/wp/v2/posts/"

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
    url = "https://summitphotoengine.com/wp-json/wp/v2/media/?title=" + slug

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

    # read the image
    input_image = PIL.Image.open(file)

    '''
        # scan for QR codes
        codes = qrscan.read_codes(input_image)
    
        # Print results
        for this_code in codes:
            if "QRCODE" == this_code.type:
                sys.stdout.write(u"\x1b[2J\x1b[H\u001b[41;1m" + "QR CODE SCAN COMPLETE ...\n\n\n\n\u001b[0m")
                print('DETECTED: {}'.format(str(this_code.data)))
                exit()
    
        sys.stdout.write(u"\x1b[2J\x1b[H\u001b[41;1m" + "Uploading ...\n\n\n\n\u001b[0m")
    '''

    # gui window
    window = tk.Tk()
    window.attributes("-fullscreen", True)
    window.minsize(800, 600)
    window.configure(background='black')
    window.wait_visibility(window)
    window.wm_attributes('-alpha', 0.3)

    # image widget
    pic = ImageTk.PhotoImage(Image.open(file).resize((480, 480)))
    image_widget = tk.Label(window, image=pic, width=800, height=480, background='black')
    image_widget.place(x=0, y=0, width=800, height=480)
    image_widget.pack(expand=True)
    window.update()
    window.minsize(800, 480)

    # transfer the file
    image_id = upload_image(file)
    response = create_post(image_id)
    print(response)

    # close window
    window.after(2500, lambda: window.destroy())
    tada.play()
    window.mainloop()


# snap the picture
def capture(camera, file):

    shutter.play()
    camera.resolution = (1080, 1080)
    camera.capture(file, 'jpeg')
    camera.resolution = (800, 480)


# add smoke and logo
def combine_images(file):

    choices = 'ABCDE'
    rando = random.choice(choices)
    original = Image.open(file)
    smoke = Image.open("smoke/WPE-Summit18-PhotoEngine-Overlay-v01-Overlay-{}.png".format(rando))

    #logo = Image.open("WPE-LGO-Summit18+WPE-Center-RGB+W.png")

    area = (0, 0, 1080, 1080)
    original.paste(smoke, area, mask=smoke)

    #original.paste(logo, area, mask=logo)
    original.save(file)


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

        camera = picamera.PiCamera(resolution=(800, 480))
        camera.vflip = True
        camera.hflip = True
        camera.awb_mode = 'sport'
        overlay = make_overlay(camera)

        # start preview
        camera.preview_fullscreen = True

        # thread to show the camera preview in background process
        preview = _thread.start_new_thread(preview_camera, (camera,))

        # infinite loop to check the GPIO pins for button press
        while 1:
            if not GPIO.input(26):

                # continuously updates the overlayed layer and display stats
                overlay_renderer = None

                for x in reversed(range(5)):
                    if x > 0:
                        text = str(x)
                    else:
                        text = ""

                    img = Image.new("RGBA", (800, 480))
                    draw = ImageDraw.Draw(img)
                    draw.font = ImageFont.truetype(
                        "/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf",
                        80)
                    draw.text((390, 200), text, (255, 0, 0))

                    if not overlay_renderer:
                        """
                        If overlay layer is not created yet, get a new one. Layer
                        parameter must have 3 or higher number because the original
                        preview layer has a # of 2 and a layer with smaller number will
                        be obscured.
                        """
                        overlay_renderer = camera.add_overlay(img.tobytes(),
                                                              layer=3,
                                                              size=img.size,
                                                              alpha=255);
                    else:
                        overlay_renderer.update(img.tobytes())
                    beep.play()
                    time.sleep(1)

                #camera.remove_overlay(overlay_renderer)
                camera.remove_overlay(overlay)
                camera.stop_preview()

                file = "./pictures/booth_{}.jpg".format(time.time())

                capture(camera, file)

                combine_images(file)

                display_captured(file)

                tweet(file)

                for x in range(0, 10):
                    sys.stdout.write(u"\u001b[1000D" + "SNAP!!")

                # restore the overlay and preview
                overlay = make_overlay(camera)
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
