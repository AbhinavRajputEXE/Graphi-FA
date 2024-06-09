import base64
from flask import Response, jsonify
from userProfile.getReq import getPhoto, getProfile
import sys
from utils.getToken import get_token

sys.dont_write_bytecode = True

token = get_token()


def profile(data):
    function = data["function"]

    if function == "getPhoto":
        try:
            pic = getPhoto.get_photo(token)
            if pic[1] == 200:
                return Response(pic[0], mimetype="image/jpeg"), 200
            else:
                return (
                    jsonify(
                        {
                            "error": True,
                            "data": pic[0],
                            "success": False,
                            "message": "Failed to get pic",
                        }
                    ),
                    500,
                )
        except Exception as e:
            print("Error getting photo:", e)
            return (
                jsonify(
                    {
                        "error": True,
                        "data": e.args,
                        "success": False,
                        "message": "Failed to get pic",
                    }
                ),
                500,
            )

    elif function == "getProfile":
        try:
            res = getProfile.get_profile(token)
            if res[1] == 200:
                return (
                    jsonify(
                        {
                            "error": False,
                            "data": res[0],
                            "success": True,
                            "message": "Successfully fetched profile",
                        }
                    ),
                    200,
                )
            else:
                return (
                    jsonify(
                        {
                            "error": True,
                            "data": res[0],
                            "success": False,
                            "message": "Failed to fetch profile",
                        }
                    ),
                    500,
                )
        except Exception as e:
            print("Error fetching profile:", e)
            return (
                jsonify(
                    {
                        "error": True,
                        "data": e.args,
                        "success": False,
                        "message": "Failed to fetch profile",
                    }
                ),
                500,
            )

    else:
        return (
            jsonify(
                {
                    "error": True,
                    "data": "Function not available",
                    "success": False,
                    "message": "Function not available",
                }
            ),
            400,
        )
