import requests
import time
import mysql.connector
import MySQLdb.cursors


config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': '8889',
    'database': 'mystudiopress',
    'raise_on_warnings': True,
}

link = mysql.connector.connect(**config)


def get_validate(email):
    return requests.get(
        "https://api.mailgun.net/v3/address/validate",
        auth=("api", "pubkey-5ho2ohnup6y8n8h4gsfuc047c2pxx9l0"),
        params={"address": email})


cursor = link.cursor(dictionary=True)

cursor.execute("SELECT user_email FROM wp_users;")

data = cursor.fetchall()

for email in data:
    email_address = email['user_email']
    validate_response = get_validate(email_address).json()
    valid = validate_response['is_valid']
    print("{}: {}".format(email_address, valid))

    if valid is False:
        cursor.execute("DELETE FROM wp_users WHERE user_email = '" + email_address + "';")
        print("DELETED")

    time.sleep(10)

