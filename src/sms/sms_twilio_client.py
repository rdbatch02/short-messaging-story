import os

from twilio.rest import Client

from src.event.domain.message_event import MessageEvent
from src.event.event_client import EventClient


class SmsTwilioClient:
    twilio_sid = os.environ["TWILIO_SID"]
    twilio_auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    source_phone = os.environ["TWILIO_SOURCE_PHONE"]
    event_client = EventClient()

    def __init__(self):
        self.client = Client(self.twilio_sid, self.twilio_auth_token)

    def send_sms(self, message, phone):
        message = self.client.messages.create(
            to=phone,
            from_=self.source_phone,
            body=message
        )

        message_event: MessageEvent = MessageEvent().from_twilio_sms_event(message)
        self.event_client.save(message_event)
