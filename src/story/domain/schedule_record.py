from uuid import uuid4

from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from dateutil import parser
from datetime import datetime


@dataclass
class ScheduleRecord(DataClassJsonMixin):
    id: str = str(uuid4())
    phone: str = None
    trigger_timestamp: datetime = None
    message: str = None

    @staticmethod
    def from_dynamo(data: dict):
        return ScheduleRecord(
            id=data['id'],
            phone=data['phone'],
            trigger_timestamp=parser.parse(data['trigger_timestamp']),
            message=data['message']
        )
