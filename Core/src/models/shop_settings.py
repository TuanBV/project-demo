"""
Shop settings model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR
from models.entity_base import EntityBase


class ShopSettings(EntityBase):
  shop_no = Column(VARCHAR)
  key = Column(VARCHAR)
  value = Column(VARCHAR)
