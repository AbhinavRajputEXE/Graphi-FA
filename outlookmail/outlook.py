from flask import jsonify
from outlookmail.postReq import sendMail, forwardMail
from outlookmail.getReq import getMail, getHighImpMail, getMailFromAdd, getMailWithWord, getEmailChanges, getInboxRules, getMyMailCategory, getMailHeader, getConferenceRoom

from utils.getToken import get_token
import sys

sys.dont_write_bytecode = True

token = get_token()


def outlook(data):
    function = data["function"]

    # SEND MAIL

    if (function == "sendMail"):
        payload = data["payload"]
        try:
            res = sendMail.send_email(token, payload)
            if res[1] == 200:
                return jsonify({"error": False, "data": res[0], "success": True, "message": "Successfully sent mail"}), 200
            else:
                return jsonify({"error": True, "data": res[0], "success": False, "message": "Failed to send mail"}), 500
        except Exception as e:
            print("Error sending email:", e)
            return jsonify({"error": True, "data": e.args, "success": False, "message": "Failed to send email"}), 500
        
    # FORWARD MAIL

    elif (function == "forwardMail"):
        payload = data["payload"]
        try:
            res = forwardMail.forward_mail(token, payload)
            return jsonify({"error": False, "data": res, "success": True, "message": "Email forwarded successfully"}), 200
        except Exception as e:
            print("Error forwarding email:", e)
            return jsonify({"error": True, "data": e.args, "success": False, "message": "Failed to forward email"}), 500
        
    # GET HIGH IMPORTANT MAIL

    elif (function == "getHighImpMail"):
        try:
            res = getHighImpMail.get_high_important_mail(token)
            return jsonify({"error": False, "data": res, "success": True, "message": "Got your high importance email successfully"}), 200
        except Exception as e:
            print("Error getting you high importance email:", e)
            return jsonify({"error": True, "data": e.args, "success": False, "message": "Failed to get your high importance email"}), 500
        
    # GET MAIL

    elif (function == "getMail"):
        try:
            res = getMail.get_mail(token)
            if res[1] == 200:
                return jsonify({"error": False, "data": res[0], "success": True, "message": "Successfully fetched mail"}), 200
            else:
                return jsonify({"error": True, "data": res[0], "success": False, "message": "Failed to get mails"}), 500
        except Exception as e:
            print("Error getting mail:", e)
            return jsonify({"error": True, "data": e.args, "success": False, "message": "Failed to get mail"}), 500
        
    # GET MAIL FROM A SPECIFIED ADDRESS

    elif (function == "getMailFromAdd"):
        payload = data["payload"]
        try:
            res = getMailFromAdd.get_mail_from_address(token, payload)
            return jsonify({"error": False, "data": res, "success": True, "message": res}), 200
        except Exception as e:
            print("Error getting mail from the specified email address:", e)
            return jsonify({"error": True, "data": e.args, "success": False, "message": "Failed to get mail from the specified email address"}), 500
        
    # GET MAIL WITH A SPECIFIC WORD

    elif (function == "getMailWithWord"):
        payload = data['payload']
        try:
            res = getMailWithWord.get_mail_with_word(token, payload)
            return jsonify({"error": False, "data": res, "success": True, "message": res}), 200
        except Exception as e:
            print("Error getting word with a specific word:", e)
            return jsonify({"error": True, "data": e.args, "success": False, "message": "Failed to get mail with a specific word"}), 500
        
    # GET MAIL CHANGES

    elif (function == "getMailChanges"):

        try:
            res = getEmailChanges.get_mail_changes(token)
            return jsonify({"error": False, "data": res, "success": True, "message": res}), 200
        except Exception as e:
            print("Error getting changes in your email:", e)
            return jsonify({"error": True, "data": e.args, "success": False, "message": "Failed to track changes in you mail"}), 500
        
    # GET INBOX RULES

    elif (function == "getInboxRules"):

        try:
            res = getInboxRules.get_inbox_rules(token)
            return jsonify({"error": False, "data": res, "success": True, "message": res}), 200
        except Exception as e:
            print("Error getting inbox rules:", e)
            return jsonify({"error": True, "data": e.args, "success": False, "message": "Failed to inbox rule"}), 500
        
    # GET MAIL CATEGORY

    elif (function == "getMailCategory"):

        try:
            res = getMyMailCategory.get_mail_category(token)
            return jsonify({"error": False, "data": res, "success": True, "message": res}), 200
        except Exception as e:
            print("Error getting mail category:", e)
            return jsonify({"error": True, "data": e.args, "success": False, "message": "Failed to get mail category"}), 500
        
    # GET MAIL HEADER

    elif (function == "getMailHeader"):

        try:
            res = getMailHeader.get_mail_headers(token)
            return jsonify({"error": False, "data": res, "success": True, "message": res}), 200
        except Exception as e:
            print("Error getting mail headers:", e)
            return jsonify({"error": True, "data": e.args, "success": False, "message": "Failed to get your mail headers"}), 500
        
    # GET CONFERENCE ROOMS

    elif (function == "getConfRoom"):

        try:
            res = getConferenceRoom.get_conf_room(token)

            if res[1] == 200:
                return jsonify({"error": False, "data": res[0], "success": True, "message": "Successfully fetched conf rooms"}), 200
            else:
                return jsonify({"error": True, "data": res[0], "success": False, "message": "Failed to get conf room"}), 500

        except Exception as e:
            print("Error getting list of conf room:", e)
            return jsonify({"error": True, "data": e.args, "success": False, "message": "Failed to get conf room"}), 500
        
    # DEFAULT STATE

    else:
        try:
            return jsonify({"error": False, "success": True, "message": "Function didn't match"}), 200
        except Exception as e:
            print("Error:", e)
            return jsonify({"error": True, "data": e.args, "success": False}), 500
