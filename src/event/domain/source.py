from enum import Enum


class Source(Enum):
    SMS = 0
    SCHEDULED = 1

    @staticmethod
    def from_str(string):
        for source in Source:
            if str(source) == string:
                return source
        raise NotImplementedError
