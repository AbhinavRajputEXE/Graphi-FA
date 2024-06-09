import sys

sys.dont_write_bytecode = True

mail = None


def setMail(email):
    global mail
    mail = email
    return mail


BASE_URL = "https://graph.microsoft.com/v1.0/users"
BETA_BASE_URL = "https://graph.microsoft.com/beta/users"

# PROFILE URLs


def PROFILE_URL():
    if mail:
        return BASE_URL + f"/{mail}"
    else:
        return "Profile URL not available"


def PROFILE_PHOTO_URL():
    if mail:
        return BASE_URL + f"/{mail}/photo/$value"
    else:
        return "Profile photo URL not available"


# OUTLOOK URLs


def GET_CONFERENCEROOM_URL():
    if mail:
        return BETA_BASE_URL + f"/{mail}/findRooms"
    else:
        return "Conference room URL not available"


def GET_MAIL_URL():
    if mail:
        return BASE_URL + f"/{mail}/messages"
    else:
        return "Get mail URL not available"


def SEND_MAIL_URL():
    if mail:
        return BASE_URL + f"/{mail}/sendMail"
    else:
        return "Send mail URL not available"


# CALENDAR URLs


def SCHEDULE_MEETING_URL():
    if mail:
        return BASE_URL + f"/{mail}/events"
    else:
        return "Events URL not available"


def GET_EVENTS_URL():
    if mail:
        return (
            BASE_URL
            + f"/{mail}/events?$select=subject,body,bodyPreview,organizer,attendees,start,end,location"
        )
    else:
        return "Get events URL not available"


# TEAMS URLs
def LIST_CHATS_URL():
    if mail:
        return BASE_URL + f"/{mail}/chats"
    else:
        return "Chats URL not available"


def LIST_JOINED_TEAMS_URL():
    if mail:
        return BASE_URL + f"/{mail}/joinedTeams"
    else:
        return "Joined teams URL not available"
