import csv
import requests
import time

def get_validate(email):
    return requests.get(
        "https://api.mailgun.net/v3/address/validate",
        auth=("api", "pubkey-5ho2ohnup6y8n8h4gsfuc047c2pxx9l0"),
        params={"address": email})


with open("/Volumes/GoogleDrive/My Drive/mysp_data/all_forum_users__2018-09-06_21-53-16.csv") as f:
    reader = csv.reader(f)
    data = [r for r in reader]
    data.pop(0) # remove header


for email in data:
    print(email[0])
    validate_response = get_validate(email).json()
    print(validate_response['is_valid'])
    time.sleep(10)

