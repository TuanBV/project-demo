"""
Customer notification status model
"""

from helpers.kbn import IntEnum, OpenStatus
from models.entity_base import EntityBase
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT
from sqlalchemy import Column


class CustomerNotificationStatus(EntityBase):
  shop_no = Column(VARCHAR)
  customer_notification_id = Column(BIGINT)
  customer_no = Column(VARCHAR)
  read_flg = Column(IntEnum(OpenStatus), default=OpenStatus.OFF.value)
