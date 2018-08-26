from enum import Enum


class Direction(Enum):
    OUTGOING = 0
    INCOMING = 1

    @staticmethod
    def from_str(string):
        for direction in Direction:
            if str(direction) == string:
                return direction
        raise NotImplementedError
