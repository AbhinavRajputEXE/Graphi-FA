import requests
import sys

sys.dont_write_bytecode = True


def get_inbox_rules(access_token):
    try:
        response = requests.get(
            "https://graph.microsoft.com/beta/me/mailFolders/inbox/messagerules",
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
