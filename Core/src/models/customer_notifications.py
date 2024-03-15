"""
Customer notification model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, TEXT
from helpers.kbn import CustomerTypeNotify, IntEnum
from models.entity_base import EntityBase

class CustomerNotifications(EntityBase):
  """
  Properties
  """
  shop_no = Column(VARCHAR)
  kbn = Column(IntEnum(CustomerTypeNotify))
  content = Column(TEXT)
