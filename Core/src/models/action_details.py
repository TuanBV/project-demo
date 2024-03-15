"""
Action detail model
"""

from helpers.kbn import IntEnum, PrintStatus, HasConditionExclusion
from models.entity_base import EntityBase
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, DATETIME, TEXT, INTEGER


class ActionDetails(EntityBase):
  """
  Action detail model
  """
  action_code = Column(VARCHAR)
  shop_no = Column(VARCHAR)
  delivery_time = Column(DATETIME)
  title = Column(VARCHAR)
  body = Column(TEXT)
  template_id = Column(BIGINT)
  action_note = Column(TEXT)
  pdf_frontside = Column(VARCHAR)
  pdf_backside = Column(VARCHAR)
  print_status = Column(IntEnum(PrintStatus))
  number_of_customer = Column(INTEGER)
  has_condition_exclusion = Column(IntEnum(HasConditionExclusion), default=HasConditionExclusion.NO.value)
