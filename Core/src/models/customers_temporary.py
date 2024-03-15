"""
Customers temporary model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, DATETIME
from models.entity_base import EntityBase


class CustomersTemporary(EntityBase):
  email = Column(VARCHAR)
  shop_no = Column(VARCHAR)
  token = Column(VARCHAR)
  token_expiration_time = Column(DATETIME)
