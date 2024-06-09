import requests
import sys
from utils.apiConfig import PROFILE_URL

sys.dont_write_bytecode = True


def get_profile(access_token):
    try:
        response = requests.get(
            PROFILE_URL(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
        )
        if response.ok: 
            return response.json(), 200
        else:
            return response.json(), 500
    except Exception as e:
        print("Error:", e)
