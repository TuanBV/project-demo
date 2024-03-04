"""
Users model
"""

from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import VARCHAR, DATE, INTEGER, DATETIME
from sqlalchemy.orm import declarative_base
from helpers.kbn import IntEnum, DeleteFlag, RecommenderFlag

Base = declarative_base()

class Users(Base):
  """
  Users model
  """
  employee_code = Column(VARCHAR, primary_key=True)
  fullname = Column(VARCHAR)
  email = Column(VARCHAR)
  birthday = Column(DATE)
  full_address = Column(VARCHAR)
  place_issued_identification = Column(VARCHAR)
  identification_number = Column(VARCHAR)
  date_issued_identification = Column(DATE)
  telephone_no = Column(VARCHAR)
  registered_date = Column(DATE)
  position_id = Column(INTEGER)
  office_id = Column(INTEGER)
  password = Column(VARCHAR)
  login_failed_count = Column(INTEGER, default=0)
  token = Column(VARCHAR)
  expire = Column(DATETIME)
  created_user = Column(VARCHAR)
  created_date = Column(DATETIME, server_default = text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
  updated_user = Column(VARCHAR)
  updated_date = Column(DATETIME, onupdate=text("CURRENT_TIMESTAMP"))
  is_deleted = Column(IntEnum(DeleteFlag), default = DeleteFlag.OFF.value)
  recommender_flag = Column(IntEnum(RecommenderFlag), default = DeleteFlag.OFF.value)
  gender = Column(INTEGER, default=0)
  __tablename__ = "users"
