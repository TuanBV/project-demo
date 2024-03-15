"""
Batches model
"""

from sqlalchemy import Enum
from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import VARCHAR, JSON, DATETIME, INTEGER, BIGINT
from sqlalchemy.orm import declarative_base
from helpers import kbn
from utils.date import get_current_time_obj

Base = declarative_base()


class Batches(Base):
  """
  Batches model
  """
  __tablename__ = "batches"
  id = Column(BIGINT, primary_key=True)
  job_name = Column(VARCHAR)
  job_type = Column(VARCHAR)
  job_id = Column(VARCHAR)
  args = Column(JSON)
  status = Column(Enum(kbn.BatchStatus, create_constraint=False))
  retry_count = Column(INTEGER, default=0)
  queue_time = Column(DATETIME)
  start_time = Column(DATETIME)
  end_time = Column(DATETIME)
  payload = Column(JSON)
  updated_date = Column(DATETIME, onupdate=get_current_time_obj())
  created_date = Column(DATETIME, server_default = text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
  shop_no = Column(VARCHAR)
