import requests
import sys

sys.dont_write_bytecode = True


def get_high_important_mail(access_token):
    try:
        response = requests.get(
            "https://graph.microsoft.com/v1.0/me/messages?$filter=importance eq 'high'",
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
