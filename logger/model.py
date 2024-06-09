from datetime import datetime
from sqlalchemy import Column, String, DateTime
import uuid
import sys
from database.db import Base, SessionLocal

# Prevent bytecode generation
sys.dont_write_bytecode = True


# Define the Log model
class Log(Base):
    __tablename__ = "log"

    # Define columns for the Log table
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100))
    email = Column(String(100))
    timestamp = Column(DateTime, default=datetime.utcnow)
    service = Column(String(50))
    func = Column(String(50))
    status = Column(String(20))
    error = Column(String(15))
    error_description = Column(String(255))
    success = Column(String(15))
    app = Column(String(255))

    # Define representation of the Log object
    def __repr__(self):
        return f"Log(id={self.id}, name={self.name}, email={self.email}, timestamp={self.timestamp}, service={self.service}, func={self.func}, app={self.app})"


# Function to log data into the database
def log_to_database(
    app, name, email, service, func, error=None, success=None, status=None, errorDes=""
):
    db = SessionLocal()
    try:
        # Create a new Log object with provided data
        new_log = Log(
            id=str(uuid.uuid4()),
            name=name,
            email=email,
            timestamp=datetime.utcnow(),
            service=service,
            func=func,
            error=error,
            success=success,
            status=status,
            error_description=errorDes,
            app=app,
        )
        # Add the new log to the session and commit changes to the database
        db.add(new_log)
        db.commit()
    except Exception as e:
        # Rollback changes if an error occurs
        db.rollback()
        print("Error: ", e)  # Print the error message
    finally:
        # Close the session
        db.close()
