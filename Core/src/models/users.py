"""
Users model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, DATETIME
from .entity_base import EntityBase

class Users(EntityBase):
  """
  Users model
  """
  fullname = Column(VARCHAR)
  email = Column(VARCHAR)
  username = Column(VARCHAR)
  password = Column(VARCHAR)
  role = Column(VARCHAR)
  # token = Column(VARCHAR)
  # expire = Column(DATETIME)

