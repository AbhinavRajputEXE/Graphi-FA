import requests
import sys

sys.dont_write_bytecode = True


def get_mail_with_word(access_token, payload):
    word = payload['word']
    try:
        response = requests.get(
            f"https://graph.microsoft.com/v1.0/me/messages?$search={word}",
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
