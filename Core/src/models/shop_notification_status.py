"""
Shop notification status model
"""

from helpers.kbn import IntEnum, OpenStatus
from models.entity_base import EntityBase
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT
from sqlalchemy import Column, ForeignKey


class ShopNotificationStatus(EntityBase):
  """
    Shop Notification Status Model
  """
  shop_no = Column(VARCHAR)
  shop_notification_id = Column(BIGINT, ForeignKey('shop_notifications.id'))
  shop_account_id = Column(BIGINT)
  read_flg = Column(IntEnum(OpenStatus))
