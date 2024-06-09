import requests
import sys
from utils.apiConfig import GET_CONFERENCEROOM_URL

sys.dont_write_bytecode = True


def get_conf_room(access_token):
    try:
        response = requests.get(
            GET_CONFERENCEROOM_URL(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            },
        )
        if not response.ok:
            return response.json(), 500
        else:
            return response.json(), 200

    except Exception as e:
        print("Error:", e)
        return e.args, 500
