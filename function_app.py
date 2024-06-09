import logging
import os
import json
import azure.functions as func
from flask import Flask
from utils.authAD import is_valid_email_ad
from utils.apiConfig import setMail
from utils.raiseTicket import raiseTicket
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from logger.model import log_to_database
from outlookmail import outlook
from userProfile import profile
from outlookCalendar import calendar
from teams import teams
import jwt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
flask_app = Flask(__name__)

# Initialize Azure Function app
app = func.FunctionApp()

# Database configuration
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_url = f"mysql+mysqlconnector://{db_user}:{db_pass}@localhost/graphi"

# Initialize SQLAlchemy engine and session
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)


# Home route for the Graphi service
@app.function_name(name="graphi")
@app.route(route="graphi", methods=["POST"])
def home_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing request for /graphi")

    try:
        with flask_app.app_context():
            # Extract JSON data from request
            data = req.get_json()

            # Check for Authorization header
            auth_header = req.headers.get("Authorization")
            if not auth_header:
                return func.HttpResponse(
                    json.dumps({"error": "Authorization header is missing"}),
                    status_code=401,
                    mimetype="application/json",
                )

            # Extract JWT token from Authorization header
            token_parts = auth_header.split()
            if len(token_parts) != 2 or token_parts[0] != "Bearer":
                return func.HttpResponse(
                    json.dumps({"error": "Authorization header is malformed"}),
                    status_code=401,
                    mimetype="application/json",
                )

            jwt_data = token_parts[1]
            decoded_token = jwt.decode(jwt_data, options={"verify_signature": False})

            # Extract user information from decoded token
            name = f"{decoded_token['given_name']} {decoded_token['family_name']}"
            email = decoded_token["unique_name"]
            app_name = data["app"]

            # Set email based on application
            setMail(os.getenv(app_name))

            # Check if user is valid in Active Directory
            if not is_valid_email_ad(email):
                return func.HttpResponse(
                    json.dumps({"error": "User not found in AD"}),
                    status_code=401,
                    mimetype="application/json",
                )

            # Extract service and function from request data
            service = data["service"]
            func_name = data["function"]
            raiseTicket()

            # Process request based on service
            if service == "outlook":
                return process_outlook(data, app_name, name, email, service, func_name)
            elif service == "profile":
                return process_profile(data, app_name, name, email, service, func_name)
            elif service == "calendar":
                return process_calendar(data, app_name, name, email, service, func_name)
            elif service == "teams":
                return process_teams(data, app_name, name, email, service, func_name)
            else:
                return func.HttpResponse(
                    json.dumps({"error": "Unknown service"}),
                    status_code=400,
                    mimetype="application/json",
                )

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse(
            json.dumps({"error": "Internal Server Error"}),
            status_code=500,
            mimetype="application/json",
        )


def process_outlook(data, app_name, name, email, service, func_name):
    temp = outlook.outlook(data)
    response_content = temp[0].get_data(as_text=True)
    json_data = json.loads(response_content)
    log_result(app_name, name, email, service, func_name, json_data, temp[1])
    return func.HttpResponse(
        json.dumps(json_data), status_code=temp[1], mimetype="application/json"
    )


def process_profile(data, app_name, name, email, service, func_name):
    temp = profile.profile(data)
    if func_name == "getPhoto":
        response_content = temp[1].get_data(as_text=True)
        json_data = json.loads(response_content)
        log_result(app_name, name, email, service, func_name, json_data, temp[2])
        return func.HttpResponse(
            temp[0], status_code=temp[2], mimetype="application/json"
        )

    response_content = temp[0].get_data(as_text=True)
    json_data = json.loads(response_content)
    log_result(app_name, name, email, service, func_name, json_data, temp[1])
    return func.HttpResponse(
        json.dumps(json_data), status_code=temp[1], mimetype="application/json"
    )


def process_calendar(data, app_name, name, email, service, func_name):
    temp = calendar.calendar(data)
    response_content = temp[0].get_data(as_text=True)
    json_data = json.loads(response_content)
    log_result(app_name, name, email, service, func_name, json_data, temp[1])
    return func.HttpResponse(
        json.dumps(json_data), status_code=temp[1], mimetype="application/json"
    )


def process_teams(data, app_name, name, email, service, func_name):
    temp = teams.teams(data)
    response_content = temp[0].get_data(as_text=True)
    json_data = json.loads(response_content)
    log_result(app_name, name, email, service, func_name, json_data, temp[1])
    return func.HttpResponse(
        json.dumps(json_data), status_code=temp[1], mimetype="application/json"
    )


def log_result(app_name, name, email, service, func_name, json_data, status):
    error_des = json_data["data"]["error"]["message"] if status != 200 else None
    log_to_database(
        app=app_name,
        name=name,
        email=email,
        service=service,
        func=func_name,
        error=json_data["error"],
        success=json_data["success"],
        status=status,
        errorDes=error_des,
    )
