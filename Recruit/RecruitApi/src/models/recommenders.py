"""
Recommenders model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, DATE
from models.entity_base import EntityBase


class Recommenders(EntityBase):
  """
  Recommenders model
  """
  fullname = Column(VARCHAR)
  email = Column(VARCHAR)
  birthday = Column(DATE)
  full_address = Column(VARCHAR)
  place_issued_identification = Column(VARCHAR)
  identification_number = Column(VARCHAR)
  date_issued_identification = Column(DATE)
  telephone_no = Column(VARCHAR)
