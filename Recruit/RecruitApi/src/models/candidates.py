"""
Candidates model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, DATE, DATETIME, INTEGER, FLOAT
from models.entity_base import EntityBase
from helpers.kbn import IntEnum, CandidateStatus, CandidateResultStatus


class Candidates(EntityBase):
  """
  Candidates model
  """
  fullname = Column(VARCHAR)
  email = Column(VARCHAR)
  birthday = Column(DATE)
  full_address = Column(VARCHAR)
  note = Column(VARCHAR)
  place_of_birth = Column(VARCHAR)
  place_issued_identification = Column(VARCHAR)
  identification_number = Column(VARCHAR)
  date_issued_identification = Column(DATE)
  bank_account = Column(VARCHAR)
  reason = Column(VARCHAR)
  bank_branch = Column(VARCHAR)
  vehicle_number = Column(VARCHAR)
  start_join_date = Column(DATE)
  school = Column(VARCHAR)
  department = Column(VARCHAR)
  class_room = Column(VARCHAR)
  telephone_no = Column(VARCHAR)
  application_date = Column(DATE)
  position_id = Column(INTEGER)
  team_id = Column(INTEGER)
  cv_file_path = Column(VARCHAR)
  office_id = Column(INTEGER)
  recommender_id = Column(INTEGER)
  result_status = Column(IntEnum(CandidateResultStatus), default=CandidateResultStatus.UNSENT.value)
  count_apply = Column(INTEGER, default=0)
  status = Column(IntEnum(CandidateStatus), default=CandidateStatus.RECEIVE_CV.value)
  previous_status = Column(INTEGER, default=None)
  token = Column(VARCHAR)
  expire = Column(DATETIME)
  gender = Column(INTEGER, default=0)
  number_experiences = Column(FLOAT, default=0)
