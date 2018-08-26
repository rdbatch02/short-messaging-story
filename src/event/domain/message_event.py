import json
from dateutil import parser
from datetime import datetime
from dataclasses import dataclass

from twilio.rest.api.v2010.account.message import MessageInstance

from src.event.domain.direction import Direction
from src.event.domain.source import Source


@dataclass
class MessageEvent:
    id: str = None
    phone: str = None
    direction: Direction = None
    message: str = None
    timestamp: datetime = None
    source: Source = None

    @staticmethod
    def from_twilio_sms_event(message: MessageInstance):
        if message.direction == Direction.INCOMING:
            phone = message.from_
        else:
            phone = message.to

        event = MessageEvent(
            id=message.sid,
            phone=phone,
            direction=message.direction,
            message=message.body,
            timestamp=datetime.now(),
            source=Source.SMS
        )
        return event

    @staticmethod
    def from_sqs_message(sqs_message: str):
        sqs_data = json.loads(sqs_message['body'])
        print("Creating MessageEvent from SQS Message Body: " + str(sqs_data))
        return MessageEvent(
            id=sqs_data['id'],
            phone=sqs_data['phone'],
            direction=Direction.from_str(sqs_data['direction']),
            message=sqs_data['message'],
            timestamp=parser.parse(sqs_data['timestamp']),
            source=Source.from_str(sqs_data['source'])
        )

    def to_json_dict(self):
        return {
            'id': self.id,
            'phone': self.phone,
            'direction': str(self.direction),
            'message': self.message,
            'timestamp': str(self.timestamp),
            'source': str(self.source)
        }