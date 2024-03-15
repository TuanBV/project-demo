"""
Payment methods model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR
from helpers.kbn import IntEnum, PaymentMethod
from models.entity_base import EntityBase

class PaymentMethods(EntityBase):
  """
  Payment methods model
  """
  code = Column(IntEnum(PaymentMethod))
  name = Column(VARCHAR)
  note = Column(VARCHAR)
