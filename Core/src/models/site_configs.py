"""
Site configs model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR
from models.entity_base import EntityBase


class SiteConfigs(EntityBase):
  key = Column(VARCHAR)
  value = Column(VARCHAR)
