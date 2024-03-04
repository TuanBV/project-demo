"""
Offices model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR
from models.entity_base import EntityBase


class Offices(EntityBase):
  """
  Offices model
  """
  name = Column(VARCHAR)
  full_address = Column(VARCHAR)
  telephone_no = Column(VARCHAR)
  mail_admin = Column(VARCHAR)
  password_mail = Column(VARCHAR)
