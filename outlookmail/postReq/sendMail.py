import requests
import sys
from utils.apiConfig import SEND_MAIL_URL

sys.dont_write_bytecode = True


def send_email(access_token, payload):
    recipient_email = payload["recipientEmail"]
    subject = payload["subject"]
    body = payload["body"]
    contentType = payload["content-type"]
    try:
        response = requests.post(
            SEND_MAIL_URL(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            },
            json={
                "message": {
                    "subject": subject,
                    "body": {
                        "contentType": contentType,
                        "content": body
                    },
                    "toRecipients": [
                        {
                            "emailAddress": {
                                "address": recipient_email
                            }
                        }
                    ]
                }
            }
        )
        if not response.ok: 
            return response.json(), 500
        else:
            return None, 200
    except Exception as e:
        print("Error:", e)
        return e.args, 500