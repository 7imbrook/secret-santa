# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = ""
auth_token = ""


def send_message(message: str, number: str) -> None:
    # client = Client(account_sid, auth_token)
    # message = client.messages.create(body=message, from_="", to=number)
    print(f"[to: {number}] {message}")
