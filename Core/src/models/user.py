"""
User model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import TINYINT, DATE, VARCHAR, FLOAT, INTEGER
# from helpers.kbn import IntEnum, PaymentPlan
from models.entity_base import EntityBase


class User(EntityBase):
  """
  User model
  """
  id = Column(INTEGER, primary_key=True)
  username = Column(VARCHAR)
  fullname = Column(VARCHAR)
  password = Column(VARCHAR)
  role = Column(INTEGER)
