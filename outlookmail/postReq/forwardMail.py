import requests
import sys

sys.dont_write_bytecode = True


def forward_mail(access_token, payload):
    email_address = payload["recipientEmail"]
    name = payload["name"]
    messageId = payload["mail_id"]

    try:
        response = requests.post(
            f"https://graph.microsoft.com/v1.0/me/messages/{messageId}/forward",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            },
            json={

                "comment": "FYI",
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": email_address,
                            "name": name
                        }
                    }
                ]

            }
        )
        print("Response", response.json())
        if not response.ok:
            raise Exception(f"Error: {response.status_code}")
        return response
    except Exception as e:
        print("Error:", e)
