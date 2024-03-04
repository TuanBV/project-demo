"""
Teams model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR
from models.entity_base import EntityBase


class Teams(EntityBase):
  """
  Teams model
  """
  name = Column(VARCHAR)
