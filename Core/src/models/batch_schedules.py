"""
Batch schedules model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, DATETIME
from helpers.kbn import BatchStatus, IntEnum
from models.entity_base import EntityBase

class BatchSchedules(EntityBase):
  """
  Properties
  """
  run_time = Column(DATETIME)
  status_kbn = Column(IntEnum(BatchStatus), default=BatchStatus.WAITING.value)
  key = Column(VARCHAR)
  shop_no = Column(VARCHAR)
