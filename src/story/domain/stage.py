from dataclasses import dataclass
from typing import List

from src.story.domain.trigger import Trigger


@dataclass
class Stage:
    id: str = None
    story_id: str = None
    ancestor: List[str] = None
    triggers: Trigger = None
    children: List[str] = None
    message: str = None

    @staticmethod
    def from_dynamo(data: dict):
        return Stage(
            id=data['id'],
            story_id=data['story_id'],
            ancestor=data['ancestor'],
            triggers=Trigger.from_dynamo(data['triggers']),
            children=data['children'],
            message=data['message']
        )