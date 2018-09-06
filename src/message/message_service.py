import os
import json

import boto3

from src.message.domain.send_message_request import SendMessageRequest
from src.event.domain.message_event import MessageEvent


class MessageService:
    sqs = boto3.resource('sqs')
    message_queue_name = os.environ["SEND_SMS_QUEUE_NAME"]
    processor_queue_name = os.environ['STORY_PROCESSOR_QUEUE_NAME']
    queue = sqs.get_queue_by_name(QueueName=message_queue_name)

    def send_sms(self, request: SendMessageRequest):
        print("Sending message to send sms queue: " + str(request))
        self.queue.send_sms(MessageBody=request.to_json())

    def send_story_message(self, message_event: MessageEvent):
        queue = self.sqs.get_queue_by_name(QueueName=self.processor_queue_name)
        queue.send_message(MessageBody=json.dumps(message_event.to_json_dict()))
