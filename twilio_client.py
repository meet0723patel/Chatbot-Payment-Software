from dotenv import load_dotenv
import os
from twilio.rest import Client

load_dotenv()

serv_url = "https://chatbot-payment-software-webhook-dvkieiy6wa-uc.a.run.app"

def get_reg_twiml(phrase, to):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
                <Response>
                <Say>To confirm your identity, please say the phrase "{phrase}" after the bleep. When finished, press star. </Say>
                <Record
                action="{serv_url}/recording_finished"
                maxLength="10"
                finishOnKey="*"
                recordingStatusCallback="{serv_url}/recording_cb/{to}/1"
                recordingStatusCallbackEvent="completed absent"/>
                <Say>Let's confirm that again. Please say "{phrase}". When finished, press star.</Say>
                <Record
                action="{serv_url}/recording_finished"
                maxLength="10"
                finishOnKey="*"
                recordingStatusCallback="{serv_url}/recording_cb/{to}/2"
                recordingStatusCallbackEvent="completed absent"/>
                <Say>To finalize, please say "{phrase}" again. When finished, press star.</Say>
                <Record
                action="{serv_url}/recording_finished"
                maxLength="10"
                finishOnKey="*"
                recordingStatusCallback="{serv_url}/recording_cb/{to}/3"
                recordingStatusCallbackEvent="completed absent"/>
                </Response>
            """

def get_verify_twiml(sender, recipient, amt, phrase):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
                <Response>
                <Say>We recently noticed an attempt to transfer ${amt} to {recipient}. To confirm this transfer, say the phrase {phrase}. When finished, press star. </Say>
                <Record
                action="{serv_url}/recording_finished"
                maxLength="10"
                finishOnKey="*"
                recordingStatusCallback="{serv_url}/transfer/{sender}/{recipient}/{amt}"
                recordingStatusCallbackEvent="completed absent"/>
                </Response>
            """


account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

def SMS(to, message):
    message = client.messages \
        .create(
            body=message,
            from_='+16478761874',
            to=to,
        )

def Call(to):
    client.calls.create(
        twiml=get_reg_twiml('Transfer money to', to),
        to=to,
        from_='+16478761874'
    )

def Verify(sender, recipient, amt):
    client.calls.create(
        twiml=get_verify_twiml(sender, recipient, amt,
                               'Transfer money to'),
        to=sender,
        from_='+16478761874'
    )

if __name__ == "__main__":
    Call('+16478909000')