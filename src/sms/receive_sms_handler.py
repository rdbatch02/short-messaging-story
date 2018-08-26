import json
import os
from urllib.parse import parse_qs
from datetime import datetime
from twilio.twiml.messaging_response import MessagingResponse
import boto3

from src.event.domain.message_event import MessageEvent
from src.event.event_client import EventClient
from src.event.domain.direction import Direction
from src.event.domain.source import Source

event_client = EventClient()


def handle(event, context):
    print("Incoming message: " + str(event))
    handler = IncomingSmsHandler()
    return handler.handle(event)


class IncomingSmsHandler:
    event_client = EventClient()
    sqs = boto3.resource('sqs')
    processor_queue_name = os.environ['STORY_PROCESSOR_QUEUE_NAME']

    def handle(self, event):
        inbound_message_params = parse_qs(event["body"])
        print("Inbound message params: " + str(inbound_message_params))
        event = self.create_inbound_message_event(inbound_message_params)
        event_client.save(event)
        self.handoff_to_processor(event)
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/xml"
            },
            "body": self.create_twiml_response()
        }
        return response

    def create_twiml_response(self):
        resp = MessagingResponse()
        return str(resp)

    def create_inbound_message_event(self, inbound_message) -> MessageEvent:
        return MessageEvent(
            id=self.get_message_attr(inbound_message, 'MessageSid'),
            phone=self.get_message_attr(inbound_message, 'From'),
            direction=Direction.INCOMING,
            message=self.get_message_attr(inbound_message, 'Body'),
            timestamp=datetime.now(),
            source=Source.SMS
        )

    def handoff_to_processor(self, message_event: MessageEvent):
        queue = self.sqs.get_queue_by_name(QueueName=self.processor_queue_name)
        queue.send_message(MessageBody=json.dumps(message_event.to_json_dict()))

    def get_message_attr(self, message, attr):
        return message[attr][0]
