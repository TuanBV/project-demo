"""
Customer tag model
"""

from models.entity_base import EntityBase
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR


class CustomerTags(EntityBase):
  title = Column(VARCHAR)
  shop_no = Column(VARCHAR)
