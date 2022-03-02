# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = "AC3435acdb7efebd2e8b635e59cd39a61a"
auth_token = "7c0315f2556be8ab71200cfd421755a1"
account_number = "+1 616 449 1798"


def send_message(message: str, number: str, confirm: bool = False) -> None:
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=message, from_=account_number, to=number)
