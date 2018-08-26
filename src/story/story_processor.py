import json

from src.story.domain.user import User
from src.story.domain.stage import Stage
from src.story.story_service import StoryService
from src.event.domain.message_event import MessageEvent
from src.message.domain.send_message_request import SendMessageRequest
from src.message.message_service import MessageService
from src.event.domain.source import Source


def handle(event, context):
    data = json.loads(event['Records'][0]['body'])
    print('Handling request: ' + json.dumps(data))
    if 'phone' not in data:
        raise Exception('Malformed story processor event, missing phone ' + json.dumps(data))
    processor = StoryProcessor(data['phone'])

    if Source.from_str(data['source']) == Source.SCHEDULED:
        print("Handling scheduled event: " + json.dumps(data))
    elif Source.from_str(data['source']) == Source.SMS:
        print("Handling SMS event: " + json.dumps(data))
    else:
        raise Exception('Malformed story processor event, bad source ' + json.dumps(data))

    for record in event['Records']:
        processor.handle_event(record)


class StoryProcessor:
    story_service = StoryService()
    message_service = MessageService()

    def __init__(self, phone):
        self.user_story: User = self.story_service.get_story(phone)
        self.user_stage: Stage = self.story_service.get_stage(self.user_story.user_state['current_stage'])
        self.user_next_stages = [self.story_service.get_stage(stage) for stage in self.user_stage.children]

    def handle_event(self, data):
        message_event = MessageEvent.from_sqs_message(data)
        self.user_stage = self.get_new_stage(message_event)
        message_request = self.generate_message_request()
        self.message_service.send_message(message_request)

    def get_new_stage(self, message: MessageEvent) -> Stage:
        next_stage = self.story_service.find_stage_by_phrase(self.user_stage, message.message)
        if next_stage is not None:
            print("Found next stage: " + str(next_stage))
            self.user_story = self.story_service.update_stage(self.user_story, next_stage)
            return next_stage
        return self.user_stage  # No update, stage remains the same

    def generate_message_request(self):
        return SendMessageRequest(
            phone=self.user_story.phone,
            message=self.user_stage.message
        )
