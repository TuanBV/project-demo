"""
Condition filters model
"""

from sqlalchemy import JSON, Column
from sqlalchemy.dialects.mysql import VARCHAR, TINYINT
from models.entity_base import EntityBase


class ConditionFilters(EntityBase):
  title = Column(VARCHAR)
  shop_no = Column(VARCHAR)
  customer_filters = Column(JSON)
  has_condition_exclusion = Column(TINYINT)
