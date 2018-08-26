import os

import boto3

from src.message.domain.send_message_request import SendMessageRequest


class MessageService:
    sqs = boto3.resource('sqs')
    message_queue_name = os.environ["SEND_SMS_QUEUE_NAME"]
    queue = sqs.get_queue_by_name(QueueName=message_queue_name)

    def send_message(self, request: SendMessageRequest):
        print("Sending message to send sms queue: " + str(request))
        self.queue.send_message(MessageBody=request.to_json())
