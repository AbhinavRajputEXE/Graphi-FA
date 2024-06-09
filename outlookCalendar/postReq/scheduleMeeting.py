import requests
import sys
from utils.apiConfig import SCHEDULE_MEETING_URL

sys.dont_write_bytecode = True


def schedule_meeting(access_token, payload):
    subject = payload["subject"]
    content = payload["content"]
    startDateTime = payload["startDateTime"]
    endDateTime = payload["endDateTime"]
    emailAddress = payload["emailAddress"]
    name = payload["name"]
    Type = payload["Type"]
    allowNewTimeProposals = payload["allowNewTimeProposals"]
    location = payload["location"]
    try:
        response = requests.post(
            SCHEDULE_MEETING_URL(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            },
            json={
                "subject": subject,
                "body": {
                    "contentType": "HTML",
                    "content": content
                },
                "start": {
                    "dateTime": startDateTime,
                    "timeZone": "Pacific Standard Time"
                },
                "end": {
                    "dateTime": endDateTime,
                    "timeZone": "Pacific Standard Time"
                },
                "location": {
                    "displayName": location
                },
                "attendees": [
                    {
                        "emailAddress": {
                            "address": emailAddress,
                            "name": name
                        },
                        "type": Type
                    }
                ],
                "isOnlineMeeting": True,
                "onlinemeetingprovider": "teamsForBusiness",
                "allowNewTimeProposals": allowNewTimeProposals
            }
        )
        print("Response", response.json())
        if not response.ok:
            raise Exception(f"Error: {response.status_code}")
        return ("Response", response.json())
    except Exception as e:
        return (e)
