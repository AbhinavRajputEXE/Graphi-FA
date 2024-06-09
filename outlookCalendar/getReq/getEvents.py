import requests
import sys
from utils.apiConfig import GET_EVENTS_URL

sys.dont_write_bytecode = True


def get_events(access_token):
    try:
        response = requests.get(
            GET_EVENTS_URL(),
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
