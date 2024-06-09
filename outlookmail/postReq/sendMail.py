import requests
import sys
from utils.apiConfig import SEND_MAIL_URL

sys.dont_write_bytecode = True


def send_email(access_token, payload):
    recipient_emails = payload.get("recipientEmails", [])
    cc_emails = payload.get("ccEmails", [])
    bcc_emails = payload.get("bccEmails", [])
    subject = payload["subject"]
    body = payload["body"]
    contentType = payload["content-type"]
    attachments = payload.get("attachments", [])

    to_recipients = [{"emailAddress": {"address": email}} for email in recipient_emails]
    cc_recipients = [{"emailAddress": {"address": email}} for email in cc_emails]
    bcc_recipients = [{"emailAddress": {"address": email}} for email in bcc_emails]

    formatted_attachments = [
        {
            "@odata.type": "#microsoft.graph.fileAttachment",
            "name": attachment["name"],
            "contentBytes": attachment["contentBytes"],
            "contentType": attachment["contentType"],
        }
        for attachment in attachments
    ]

    try:
        response = requests.post(
            SEND_MAIL_URL(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
            json={
                "message": {
                    "subject": subject,
                    "body": {"contentType": contentType, "content": body},
                    "toRecipients": to_recipients,
                    "ccRecipients": cc_recipients,
                    "bccRecipients": bcc_recipients,
                    "attachments": formatted_attachments,
                }
            },
        )
        if not response.ok:
            return response.json(), 500
        else:
            return None, 200
    except Exception as e:
        print("Error:", e)
        return e.args, 500
