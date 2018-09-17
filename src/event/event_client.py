import logging
import os
import boto3

from src.event.domain.message_event import MessageEvent


class EventClient:
    dynamodb = boto3.resource('dynamodb')
    event_table = dynamodb.Table(os.environ["EVENT_TABLE"])

    def save(self, event: MessageEvent):
        if event.id is None:
            logging.error("Failed to save event, missing SID")
            raise Exception("Failed to save event, missing SID")
            return

        self.event_table.put_item(Item=event.to_json())
