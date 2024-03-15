"""
Action delivery status model
"""

from helpers.kbn import SendActionStatus, IntEnum
from models.entity_base import EntityBase
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT


class ActionDeliveryStatusConfirmed(EntityBase):
  """
  Action delivery status model
  """
  action_detail_id = Column(BIGINT)
  shop_no = Column(VARCHAR)
  customer_no = Column(VARCHAR)
  status_kbn = Column(IntEnum(SendActionStatus))
