"""
Database session
"""

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from setting import settings
from helpers.kbn import TYPE_DB


Base = declarative_base()

class Database:
  """
  Class Database session
  """
  def __init__(self, db_kbn: int):
    sql_host = settings.MYSQL_HOST_READ if db_kbn == TYPE_DB.READ else settings.MYSQL_HOST_WRITE
    self.db_url = f"mysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{sql_host}/{settings.MYSQL_DB}?charset=utf8mb4"
    self.engine = create_engine(self.db_url, pool_pre_ping=True, pool_size=settings.MYSQL_POOL_SIZE, max_overflow=settings.MYSQL_MAX_OVERFLOW)
    self.session_factory = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))

  @contextmanager
  def session(self):
    session: Session = self.session_factory()
    try:
      yield session
    except Exception as e:
      session.rollback()
      raise e
    finally:
      session.close()
