from dataclasses import dataclass


@dataclass
class Story:
    id: str = None
    label: str = None

    @staticmethod
    def from_dynamo(data: dict):
        return Story(
            id=data['id'],
            label=data['label']
        )
