"""
Positions model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR
from models.entity_base import EntityBase


class Positions(EntityBase):
  """
  Positions model
  """
  name = Column(VARCHAR)
