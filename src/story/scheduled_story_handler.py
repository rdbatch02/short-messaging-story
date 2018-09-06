import datetime
from uuid import uuid4

from src.event.domain.message_event import MessageEvent
from src.event.domain.source import Source
from src.message.message_service import MessageService
from src.story.story_service import StoryService
from src.story.domain.schedule_record import ScheduleRecord


def handle(event, context):
    processor = ScheduledStoryHandler()
    processor.check_schedules()


class ScheduledStoryHandler:
    story_service = StoryService()
    message_service = MessageService()

    def check_schedules(self):
        scheduled_records = self.story_service.get_scheduled_records()
        lapsed_schedules = [schedule for schedule in scheduled_records if schedule.trigger_timestamp <= datetime.datetime.now()]
        for lapsed_schedule in lapsed_schedules:
            print("Triggering scheduled message: " + str(lapsed_schedule))
            message_event = self.generate_message_event(lapsed_schedule)
            self.message_service.send_story_message(message_event)
            self.story_service.delete_schedule_record(message_event.id)

    def generate_message_event(self, schedule_record: ScheduleRecord):
        return MessageEvent(
            id=schedule_record.id,
            phone=schedule_record.phone,
            message=schedule_record.message,
            timestamp=datetime.datetime.now(),
            source=Source.SCHEDULED
        )
