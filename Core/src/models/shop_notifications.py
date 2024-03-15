"""
Shop notification model
"""

from models.entity_base import EntityBase
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR


class ShopNotifications(EntityBase):
  content = Column(VARCHAR, nullable=True)
