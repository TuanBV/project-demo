from enum import Enum, IntEnum
import sqlalchemy as db

class FlgDelete(Enum):
    OFF = 0
    ON = 1

class StatusPost(Enum):
    POST = 0
    SAVE = 1

class ROLE(IntEnum):
    USER = 0
    ADMIN = 1

# Custom class IntEnum
class IntEnum(db.TypeDecorator):
    """
    Enables passing in a Python enum and storing the enum's *value* in the db.
    The default would have stored the enum's *name* (ie the string).
    """
    impl = db.Integer
    cache_ok = True

    def __init__(self, enumtype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, int):
            return value

        return value.value

    def process_result_value(self, value, dialect):
        # A LEFT OUTER JOIN to an unmatched row yields NULL for every one of
        # its columns, including this one — that is not an invalid enum value.
        if value is None:
            return None
        return self._enumtype(value)
