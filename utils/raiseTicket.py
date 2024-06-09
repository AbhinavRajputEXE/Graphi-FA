from datetime import datetime, timedelta
import os
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from logger.model import Log
from outlookmail.postReq.sendMail import send_email
from utils.getToken import get_token
from dotenv import load_dotenv

load_dotenv()

# Database configuration
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_url = f"mysql+mysqlconnector://{db_user}:{db_pass}@localhost/graphi"

# Initialize SQLAlchemy engine and session
engine = create_engine(db_url)
Session = scoped_session(sessionmaker(bind=engine))


def raiseTicket():
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)

    session = Session()

    try:
        failure_counts = (
            session.query(Log.service, func.count(Log.id))
            .filter(Log.error == 1, Log.timestamp >= today, Log.timestamp < tomorrow)
            .group_by(Log.service)
            .all()
        )

        for service, count in failure_counts:
            if count >= 3:
                token = get_token()

                subject = f"Failed service: {service} (Count: {count})"

                body = f"The service {service} has failed {count} times.\n\n"

                failed_line_items = (
                    session.query(Log)
                    .filter(
                        Log.service == service,
                        Log.error == 1,
                        Log.timestamp >= today,
                        Log.timestamp < tomorrow,
                    )
                    .all()
                )

                for item in failed_line_items:
                    body += f"ID: {item.id}\nName: {item.name}\nEmail: {item.email}\nTimestamp: {item.timestamp}\nService: {item.service}\nFunction: {item.func}\nError: {item.error}\nSuccess: {item.success}\nError Description: {item.error_description}\nStatus: {item.status}\nApp: {item.app}\n\n"

                payload = {
                    "recipientEmail": os.getenv("kria"),
                    "subject": subject,
                    "content-type": "text",
                    "body": body,
                }

                res = send_email(token, payload)

                if res[1] == 200:
                    print(
                        jsonify(
                            {
                                "error": False,
                                "data": res[0],
                                "success": True,
                                "message": "Successfully sent ticket mail",
                            }
                        ),
                        200,
                    )
                else:
                    print(
                        jsonify(
                            {
                                "error": True,
                                "data": res[0],
                                "success": False,
                                "message": "Failed to send ticket mail",
                            }
                        ),
                        500,
                    )
            else:
                print("No function has failed more than 3 times today.")

        return failure_counts

    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()
