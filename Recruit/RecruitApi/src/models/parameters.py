"""
Parameters model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, DATE
from sqlalchemy.orm import declarative_base
from models.entity_base import EntityBase

Base = declarative_base()

class Parameters(EntityBase):
  """
  Parameters model
  """
  name = Column(VARCHAR)
  table = Column(VARCHAR)
  column = Column(DATE)
  note = Column(VARCHAR)
