"""
Action type model
"""

from helpers.kbn import ActionType, IntEnum
from models.entity_base import EntityBase
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR


class ActionTypes(EntityBase):
  icon = Column(VARCHAR)
  name = Column(VARCHAR)
  color = Column(VARCHAR)
  comment = Column(VARCHAR)
  sort_order_no = Column(IntEnum(ActionType))
