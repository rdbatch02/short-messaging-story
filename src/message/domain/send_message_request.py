from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin

@dataclass
class SendMessageRequest(DataClassJsonMixin):
    phone: str
    message: str