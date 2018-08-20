import os
import re
import sys
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

"""
This script grabs the most recent 200
tweets containing eg. @studiopress and
tests for sentiment.
"""


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = os.environ['TWITTER_KEY']
        consumer_secret = os.environ['TWITTER_SECRET']
        access_token = os.environ['TWITTER_TOKEN']
        access_token_secret = os.environ['TWITTER_TOKEN_SECRET']

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)

        except:
            print("Error: Authentication Failed")

    def tweet(self, text):
        return self.api.update_status(text)

    def tweet_image(self, image_url, text):
        return self.api.update_with_media(image_url, text)


def main():
    # get the argument
    txt = sys.argv[1]

    # create TwitterClient object
    api = TwitterClient()

    # tweet
    response = api.tweet_image('/Users/chris.garrett/Pictures/kara.jpg', "Test #2")


if __name__ == "__main__":
    # calling main function
    main()
