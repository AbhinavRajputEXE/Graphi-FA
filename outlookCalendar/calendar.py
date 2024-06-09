from flask import jsonify
from outlookCalendar.getReq import getEvents
from outlookCalendar.postReq import scheduleMeeting
import sys
from utils.getToken import get_token
from utils.getToken import get_token

sys.dont_write_bytecode = True

token = get_token()


def calendar(data):
    function = data["function"]

    if (function == "getEvents"):
        try:
            res = getEvents.get_events(token)
            return jsonify({"error": False, "data": res, "success": True, "message": "Got Events successfully"}), 200
        except Exception as e:
            print("Error getting events:", e)
            return jsonify({"error": True, "data": e.args, "success": False, "message": "Failed getting events"}), 500

    elif (function == "scheduleMeeting"):
        payload = data["payload"]
        try:
            res = scheduleMeeting.schedule_meeting(token, payload)
            return jsonify({"error": False, "data": res, "success": True, "message": "Scheduled meeting successfully"}), 200
        except Exception as e:
            print("Error scheduling meeting:", e)
            return jsonify({"error": True, "data": e.args, "success": False, "message": "Failed to schedule a meeting"}, e), 500
    
    else:
        try:
            return jsonify({"error": False, "data": "res", "success": True, "message": "Function not available"}), 200
        except Exception as e:
            print("Error", e)
            return jsonify({"error": True, "data": e.args, "success": False, }), 500
