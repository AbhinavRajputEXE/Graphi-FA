from flask import Response, jsonify
import sys
from teams.getReq import listChats, listJoinedChats
from utils.getToken import get_token
sys.dont_write_bytecode = True

token = get_token()


def teams(data):
    function = data["function"]
    if (function == "listChats"):
        try:
            res = listChats.list_chats(token)
            return jsonify({"error": False, "data": res, "success": True, "message": res}), 200
        except Exception as e:
            print("Error getting events:", e)
            return jsonify({"error": True, "data": e.args, "success": False, "message": "Failed listing chats"}), 500

    elif (function == "listJoinedChats"):
        try:
            res = listJoinedChats.list_joined_chats(token)
            return jsonify({"error": False, "data": res, "success": True, "message": res}), 200
        except Exception as e:
            print("Error getting events:", e)
            return jsonify({"error": True, "data": e.args, "success": False, "message": "Failed listing joined chats"}), 500

    else:
        try:
            return jsonify({"error": False, "data": "res", "success": True, "message": "Function not available"}), 200
        except Exception as e:
            print("Error", e)
            return jsonify({"error": True, "data": e.args, "success": False, }), 500
