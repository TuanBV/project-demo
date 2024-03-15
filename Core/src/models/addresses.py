"""
Address model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR
from models.entity_base import EntityBase


class Addresses(EntityBase):
  zip_code = Column(VARCHAR)
  prefecture = Column(VARCHAR)
  district = Column(VARCHAR)
  address = Column(VARCHAR)
