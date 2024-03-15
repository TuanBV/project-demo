"""
Actions model
"""

from models.entity_base import EntityBase
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, JSON, DATETIME, INTEGER, TINYINT


class Actions(EntityBase):
  """
  Actions model
  """
  name = Column(VARCHAR)
  code = Column(VARCHAR)
  shop_no = Column(VARCHAR)
  action_type_id = Column(BIGINT)
  condition_filter_id = Column(BIGINT)
  customer_tag_id = Column(BIGINT)
  loop_type = Column(JSON)
  first_delivery_time = Column(DATETIME)
  number_of_customer = Column(INTEGER)
  action_status = Column(TINYINT)
