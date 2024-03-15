"""
Setting ranks model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR, INTEGER
from models.entity_base import EntityBase


class SettingRanks(EntityBase):
  shop_no = Column(VARCHAR)
  kbn = Column(TINYINT)
  range_date = Column(INTEGER)
  rank_s = Column(INTEGER)
  rank_a = Column(INTEGER)
  rank_b = Column(INTEGER)
  rank_c = Column(INTEGER)
  