"""
KBN
"""
import enum
from box import Box
import sqlalchemy as db

# delete flag
DEL_FLG = Box({
  "OFF": 0,
  "ON": 1,
})

# Data cookie name
COOKIE_NAME = Box({
  "SHOP": "__SHOP",
})

# Type database
TYPE_DB = Box({
  "READ": 0,
  "WRITE": 1
})

# Login notify flag of shop account
class LoginNotifyFlg(enum.IntEnum):
  OFF = 0
  ON = 1

# Custom class IntEnum
class IntEnum(db.TypeDecorator):
  """
  Enables passing in a Python enum and storing the enum's *value* in the db.
  The default would have stored the enum's *name* (ie the string).
  """
  impl = db.Integer
  cache_ok = True

  def __init__(self, enumtype, *args, **kwargs):
    super(IntEnum, self).__init__(*args, **kwargs)
    self._enumtype = enumtype

  def process_bind_param(self, value, dialect):
    if isinstance(value, int):
      return value

    return value.value

  def process_result_value(self, value, dialect):
    return self._enumtype(value)
