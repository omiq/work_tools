import tweepy



auth = tweepy.OAuthHandler("", "")
try:
    redirect_url = auth.get_authorization_url()
    print(redirect_url)
except tweepy.TweepError:
    print('Error! Failed to get request token.')


verifier = input('Verifier:')


try:
    auth.get_access_token(verifier)
    print(auth.access_token)
    print(auth.access_token_secret)
except tweepy.TweepError:
    print('Error! Failed to get access token.')