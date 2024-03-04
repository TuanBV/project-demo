"""
Common models
"""
from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import VARCHAR, DATETIME, INTEGER
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from helpers.kbn import IntEnum, DeleteFlag
import re

@as_declarative()
class EntityBase:
  """
  Base model
  """
  id = Column(INTEGER, primary_key=True)
  created_user = Column(VARCHAR)
  created_date = Column(DATETIME, server_default = text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
  updated_user = Column(VARCHAR)
  updated_date = Column(DATETIME, onupdate=text("CURRENT_TIMESTAMP"))
  is_deleted = Column(IntEnum(DeleteFlag), default = DeleteFlag.OFF.value)
  __name__: str
  # Generate __tablename__ automatically
  @declared_attr
  def __tablename__(self) -> str:
    self.__name__ = re.sub(r"(?<!^)(?=[A-Z])", "_", self.__name__).lower()
    return self.__name__.lower()
