"""
Customers tag detail model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR
from models.entity_base import EntityBase

class CustomerTagDetails(EntityBase):
  customer_tag_id = Column(VARCHAR)
  shop_no = Column(VARCHAR)
  customer_no = Column(VARCHAR)
