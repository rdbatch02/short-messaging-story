import json
import logging
import os

from src.message.message_service import MessageService
from src.message.domain.send_message_request import SendMessageRequest

message_service = MessageService()

def send(event, context):
    data = json.loads(event['body'])
    if 'phone' not in data or 'message' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the message.")
        return

    message_request = SendMessageRequest(
        phone=event['phone'],
        message=event['message']
    )

    message_service.send_sms(message_request)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(message_request)
    }

    return response
