"""
Setting config
"""

from pydantic import BaseSettings


class Settings(BaseSettings):
  """
  Setting config
  """
  ENVIRONMENT : str
  JWT_SECRET: str
  MYSQL_USER: str
  MYSQL_PASSWORD: str
  MYSQL_HOST_WRITE: str
  MYSQL_HOST_READ: str
  MYSQL_DB: str
  DOMAIN_COOKIE: str
  MYSQL_POOL_SIZE: int
  MYSQL_MAX_OVERFLOW: int
  LOG_GROUP_NAME: str
  LOG_FILE_NAME: str
  NUMBER_LOG_UNENCRYPTED: int
  class Config:
    env_file = ".env"
    env_file_encoding = "utf-8"

settings = Settings()
