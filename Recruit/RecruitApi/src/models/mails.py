"""
Mails model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, TEXT, JSON, DATETIME, INTEGER, TINYINT
from models.entity_base import EntityBase

class Mails(EntityBase):
  """
  Mails model
  """
  title = Column(VARCHAR)
  body = Column(TEXT)
  carbon_copy = Column(JSON)
  attached_file = Column(VARCHAR)
  attached_file_name = Column(VARCHAR)
  candidate_id = Column(INTEGER)
  mail_to = Column(VARCHAR)
  sent_time = Column(DATETIME)
  status = Column(TINYINT)
  note = Column(VARCHAR)
