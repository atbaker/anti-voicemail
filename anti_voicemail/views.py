from flask import render_template, request, url_for
from twilio.rest import Client
from twilio.twiml.voice_response import Gather, Say, VoiceResponse

from . import app
from .decorators import validate_twilio_request

@app.route('/call', methods=['POST'])
@validate_twilio_request
def answer_incoming_call():
    """
    Receives an incoming call to our Twilio number, which will be missed calls
    from our user's phone number.

    Reads a greeting to the user and gives them a menu of options for what to
    do next.
    """
    # Start our TwiML response
    response = VoiceResponse()

    # If this call wasn't forwarded from our user's phone number, don't answer
    # it
    if request.form['ForwardedFrom'] != app.config['USER_PHONE_NUMBER']:
        response.hangup()
        return str(response)

    # Play a greeting and prompt the user to press a button if they want to
    # leave a voicemail
    gather = Gather(
        num_digits=1,
        timeout=10, # Wait 10 seconds for them to press a number
        action=url_for('record_message')
    )
    gather.say("You have reached the voicemail of Andrew Baker. Press 5 to leave a message.", voice='Polly.Matthew')
    response.append(gather)

    # If they don't press anything, thank the caller and end the call
    response.say('Thank you for calling. Goodbye.', voice='Polly.Matthew')

    return str(response)

@app.route('/record', methods=['POST'])
@validate_twilio_request
def record_message():
    """
    Records a caller's voicemail message after they pressed 5 in the
    answer_incoming_call route.
    """
    # Start our TwiML response
    response = VoiceResponse()

    # Say a quick prompt and then start the recording
    response.say('Please record your message after the beep.', voice='Polly.Matthew')
    response.record(
        max_length=300, # Max length of 5 minutes
        transcribe=True,
        transcribe_callback=url_for('send_transcription')
    )

    # If they hit the five minute limit, say that their time is up
    response.say('Your message has been received. Goodbye.', voice='Polly.Matthew')

    # Return the TwiML response
    return str(response)

@app.route('/send-transcription', methods=['POST'])
@validate_twilio_request
def send_transcription():
    """
    Receives a transcription webhook from Twilio and sends a text message
    notification to our user.
    """
    # Initialize our Twilio REST API client
    client = Client()

    # Render the body of our text message
    body = render_template(
        'new_voicemail.txt',
        from_number=request.form['From'],
        transcription=request.form['TranscriptionText'],
        recording_url=request.form['RecordingUrl']
    )

    # Send the text message
    client.messages.create(
        to=app.config['USER_PHONE_NUMBER'],
        from_=request.form['To'],
        body=body
    )

    return ('', 204)
