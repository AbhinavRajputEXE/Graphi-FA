import json
import requests
from utils.getToken import get_token
import sys

sys.dont_write_bytecode = True

token = get_token()

CONST_EMAIL_SEARCH_URL = 'https://graph.microsoft.com/v1.0/users?$top=3&$search="mail:{email}"&$select=mail,id'

# Checks if a given email address is valid by querying an email search URL.

# Args: email (str): A string representing an email address to be validated.

# Returns: bool: True if the email address is valid, False otherwise.

# Raises: Exception: If the response status code is not in the range of 200-202, an exception is raised containing the error message from the response.


def is_valid_email_ad(email):
    r = requests.get(
        CONST_EMAIL_SEARCH_URL.format(email=email),
        headers={"Authorization": f"Bearer {token}",
                 "ConsistencyLevel": "eventual"})
    if r.status_code in (200, 201, 202):
        user_list = json.loads(r.content).get('value', None)
        return len(user_list) > 0
    else:
        raise Exception(json.loads(r.content))
