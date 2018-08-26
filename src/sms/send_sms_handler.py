import json

from src.sms.sms_twilio_client import SmsTwilioClient

twilio_client = SmsTwilioClient()


def handle(event, context):
    print("Processing message: " + json.dumps(event))
    message_request = json.loads(event["Records"][0]["body"])
    print("Message Request: " + str(message_request))
    twilio_client.send_sms(message_request["message"], message_request["phone"])
