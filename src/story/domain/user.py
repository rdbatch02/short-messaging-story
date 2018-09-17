import parser
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    phone: str = None
    name: str = None
    story_id: str = None
    story_label: str = None
    user_state: dict = None
    start_time: datetime = None
    started: bool = False

    @staticmethod
    def from_dynamo(data: dict):
        return User(
            phone=data['phone'],
            name=data['name'],
            story_id=data['story_id'],
            story_label=data['story_label'],
            user_state=data['user_state'],
            start_time=parser.parse(data['start_time']),
            started=data['started']
        )
