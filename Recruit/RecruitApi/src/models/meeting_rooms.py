"""
Meeting room model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER
from models.entity_base import EntityBase


class MeetingRooms(EntityBase):
  """
  Meeting rooms model
  """
  name = Column(VARCHAR)
  office_id = Column(INTEGER)
