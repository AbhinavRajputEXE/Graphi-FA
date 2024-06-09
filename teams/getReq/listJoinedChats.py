import requests
import sys
from utils.apiConfig import LIST_JOINED_TEAMS_URL

sys.dont_write_bytecode = True


def list_joined_chats(access_token):
    try:
        response = requests.get(
            LIST_JOINED_TEAMS_URL(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
        )
        print("Response", response)
        if not response.ok:
            raise Exception(f"Error: {response}")
        return response.content
    except Exception as e:
        print("Error:", e)
