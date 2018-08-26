from datetime import datetime
from dateutil import parser
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Trigger:
    schedule: Optional[datetime]
    phrase: Optional[List]

    @staticmethod
    def from_dynamo(data: dict):
        schedule = None
        if data['schedule'] is not None:
            schedule = parser.parse(data['schedule'])
        return Trigger(
            schedule=schedule,
            phrase=data['phrase']
        )