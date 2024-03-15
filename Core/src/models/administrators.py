"""
Admin model
"""

from helpers.kbn import IntEnum, UserRole
from models.entity_base import EntityBase
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR


class Administrators(EntityBase):
  email = Column(VARCHAR)
  first_name = Column(VARCHAR)
  last_name = Column(VARCHAR)
  first_name_kana = Column(VARCHAR)
  last_name_kana = Column(VARCHAR)
  avatar = Column(VARCHAR)
  password = Column(VARCHAR)
  role_kbn = Column(IntEnum(UserRole))
