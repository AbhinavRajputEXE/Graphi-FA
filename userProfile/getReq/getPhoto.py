import requests
import sys
from utils.apiConfig import PROFILE_PHOTO_URL

sys.dont_write_bytecode = True


def get_photo(access_token):
    try:
        response = requests.get(
            PROFILE_PHOTO_URL(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
        )
        print("Response", response)
        if not response.ok:
            return response.json(), 500
        else:
            return response.content, 200
    except Exception as e:
        print("Error:", e)
