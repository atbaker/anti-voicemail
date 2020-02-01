from flask import abort, request
from functools import wraps
from twilio.request_validator import RequestValidator

from . import app


def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Create an instance of the RequestValidator class
        validator = RequestValidator(app.config['TWILIO_AUTH_TOKEN'])

        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            request.url,
            request.form,
            request.headers.get('X-TWILIO-SIGNATURE', '')
        )

        # Some services, like Glitch or ngrok, don't maintain the `https` scheme
        # when proxying requests to our app. So if the request seemed invalid
        # on our first try, try again with an https version of the URL
        if not request_valid:
            request_valid = validator.validate(
                request.url.replace('http://', 'https://'),
                request.form,
                request.headers.get('X-TWILIO-SIGNATURE', '')
            )

        # Continue processing the request if it's valid (or we're in development
        # or testing). Otherwise, return a 403 error if it's not
        if request_valid or app.config['TESTING']
            return f(*args, **kwargs)
        else:
            return abort(403)
    return decorated_function
