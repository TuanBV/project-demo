"""
Shop model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR, DATETIME

from models.entity_base import EntityBase


class Shop(EntityBase):
  """
  Shop model
  """
  status = Column(VARCHAR)
  shopcode = Column(VARCHAR)
  mail = Column(VARCHAR)
  password = Column(VARCHAR)
  token = Column(VARCHAR)
  name = Column(VARCHAR)
  campaign_code = Column(VARCHAR)
  shop_type = Column(TINYINT)
  loginfail = Column(TINYINT)
  locktime = Column(DATETIME)
