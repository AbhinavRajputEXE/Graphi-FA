import requests
import sys

sys.dont_write_bytecode = True


def get_mail_from_address(access_token, payload):
    mail = payload['mail']
    try:
        response = requests.get(
            f"https://graph.microsoft.com/v1.0/me/messages?$filter=(from/emailAddress/address) eq '{mail}'",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            },
        )
        print("Response", response.json())
        if not response.ok:
            raise Exception(f"Error: {response.status_code}")
        return response.json()
    except Exception as e:
        print("Error:", e)
