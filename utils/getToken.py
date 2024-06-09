import requests
import os
from dotenv import load_dotenv
import sys

sys.dont_write_bytecode = True

load_dotenv()
# EMAIL_ID = os.environ.get("EMAIL_ID")
# EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
# Tenant ID for the App registration
TENANT_ID = os.environ.get("TENANT_ID")
# Client ID for the App registration
CLIENT_ID = os.environ.get("CLIENT_ID")
# Client Secret for the App registration
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

resource_url = "https://graph.microsoft.com"


def get_token():
    form_data = {
        "grant_type": "client_credentials",
        "scope": f"{resource_url}/.default",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    url = f"https://login.microsoftonline.com//{TENANT_ID}/oauth2/v2.0/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # Send the request
    response = requests.post(url, data=form_data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        token_object = response.json()
        access_token = token_object.get("access_token")
        return access_token
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
