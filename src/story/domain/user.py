from dataclasses import dataclass


@dataclass
class User:
    phone: str = None
    name: str = None
    story_id: str = None
    story_label: str = None
    user_state: dict = None

    @staticmethod
    def from_dynamo(data: dict):
        return User(
            phone=data['phone'],
            name=data['name'],
            story_id=data['story_id'],
            story_label=data['story_label'],
            user_state=data['user_state']
        )
