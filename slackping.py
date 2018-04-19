import os
from slackclient import SlackClient

# get the api key from the environment variables
secret = os.environ["SECRET"]

# connect to the api and create client
sc = SlackClient(secret)

# set up the channel api call
# excluding archived channels
api_call = sc.api_call(
    "channels.list",
    exclude_archived=1
)

# get the list of channels
channels = api_call.get('channels')

# output the channels and their IDs
# formatted in nice columns for readability
print()
for channel in channels:
    print("{} {}".format(channel.get('name').ljust(25), channel.get('id')))

# send a message to a specific channel
api_call = sc.api_call(
    "chat.postMessage",
    channel="ABCDEFG",
    text="Hello World :awesome:"
)






