from dotenv import load_dotenv
from flask import Flask
import os

# Initialize our Flask app
app = Flask(__name__)

# Load and set our environment variables
load_dotenv()

# TODO: Handle KeyError
app.config.update(
    USER_PHONE_NUMBER=os.environ['USER_PHONE_NUMBER'],
    TWILIO_ACCOUNT_SID=os.environ['TWILIO_ACCOUNT_SID'],
    TWILIO_AUTH_TOKEN=os.environ['TWILIO_AUTH_TOKEN']
)

# Load our views
import anti_voicemail.views
