"""
Interview detail model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from models.entity_base import EntityBase
from helpers.kbn import IntEnum, Evaluate


class InterviewDetails(EntityBase):
  """
  Interview details model
  """
  interview_id = Column(INTEGER)
  employee_code = Column(VARCHAR)
  comment = Column(VARCHAR)
  evaluate = Column(IntEnum(Evaluate), default=Evaluate.NOT_INTERVIEW_YET.value)
