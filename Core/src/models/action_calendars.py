"""
Customers model
"""

from sqlalchemy import JSON, Column
from sqlalchemy.dialects.mysql import VARCHAR
from models.entity_base import EntityBase


class ActionCalendars(EntityBase):
  """
  Customers model
  """
  customer_no = Column(VARCHAR)
  shop_no = Column(VARCHAR)
  actions_by_month = Column(JSON)
