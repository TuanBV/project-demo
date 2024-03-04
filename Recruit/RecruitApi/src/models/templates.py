"""
Templates model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import declarative_base
from models.entity_base import EntityBase

Base = declarative_base()

class Templates(EntityBase):
  """
  Parameters model
  """
  title = Column(VARCHAR)
  body = Column(VARCHAR)
  key = Column(VARCHAR)
  note = Column(VARCHAR)
