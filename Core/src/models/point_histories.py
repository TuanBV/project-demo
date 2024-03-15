"""
Customers model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, DATE, FLOAT
from models.entity_base import EntityBase


class PointHistories(EntityBase):
  """
  Point histories model
  """
  changed_date = Column(DATE)
  shop_no = Column(VARCHAR)
  customer_no = Column(VARCHAR)
  payment = Column(FLOAT)
  changed_points = Column(FLOAT)
  points = Column(FLOAT)
  description = Column(VARCHAR)
  note = Column(VARCHAR)
