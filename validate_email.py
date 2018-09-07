import csv
import requests
import time
import mysql.connector

config = {
  'user': 'root',
  'password': 'root',
  'host': 'localhost:8889',
  'database': 'mystudiopress',
  'raise_on_warnings': True,
}

link = mysql.connector.connect(**config)


def get_validate(email):
    return requests.get(
        "https://api.mailgun.net/v3/address/validate",
        auth=("api", "pubkey-5ho2ohnup6y8n8h4gsfuc047c2pxx9l0"),
        params={"address": email})


cursor = link.cursor()

cursor.execute("SELECT * FROM wp_users;")

result = cursor.fetchall()

for x in result:
    print(x)

exit()

for email in data:
    print(email[0])
    validate_response = get_validate(email).json()
    print(validate_response['is_valid'])
    time.sleep(10)

