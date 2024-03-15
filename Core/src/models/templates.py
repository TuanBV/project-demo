"""
Templates model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, INTEGER, TEXT
from models.entity_base import EntityBase

class Templates(EntityBase):
  """
  Template model
  """
  name = Column(VARCHAR)
  title = Column(VARCHAR)
  shop_no = Column(VARCHAR)
  action_type_id = Column(BIGINT)
  content = Column(TEXT)
  pdf_frontside = Column(VARCHAR)
  pdf_backside = Column(VARCHAR)
  used_count = Column(INTEGER)
  comment = Column(VARCHAR)
  note = Column(VARCHAR)
  key = Column(VARCHAR)
  thumbnail = Column(VARCHAR)
