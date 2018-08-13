import sys
import os
import requests
import time
import pyperclip


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


