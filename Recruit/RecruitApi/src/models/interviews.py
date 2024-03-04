"""
Interview model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import TIME, INTEGER, VARCHAR, DATE
from models.entity_base import EntityBase
from helpers.kbn import IntEnum, InterviewStatus, InterviewForm, InterviewType


class Interviews(EntityBase):
  """
  Interviews model
  """
  time = Column(TIME)
  meeting_room_id = Column(INTEGER)
  type_kbn = Column(IntEnum(InterviewType))
  candidate_id = Column(INTEGER)
  test_score = Column(INTEGER)
  note = Column(VARCHAR)
  link_interview = Column(VARCHAR)
  status = Column(IntEnum(InterviewStatus), default=InterviewStatus.PREPARE_INTERVIEW.value)
  note = Column(VARCHAR)
  link_interview = Column(VARCHAR)
  date = Column(DATE)
  interview_form = Column(IntEnum(InterviewForm))
