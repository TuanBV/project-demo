"""
Common models
"""
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import as_declarative, declared_attr
import re

@as_declarative()
class EntityBase:
  """
  Base model
  """
  id = Column(BIGINT, primary_key=True)
  __name__: str
  # Generate __tablename__ automatically
  @declared_attr
  def __tablename__(self) -> str:
    self.__name__ = re.sub(r"(?<!^)(?=[A-Z])", "_", self.__name__).lower()
    return self.__name__.lower()
