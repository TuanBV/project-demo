"""
Setting config
"""

from pydantic_settings import BaseSettings
from pydantic import EmailStr

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
  DOMAIN_FILE: str
  MYSQL_POOL_SIZE: int
  MYSQL_MAX_OVERFLOW: int
  LOG_GROUP_NAME: str
  LOG_FILE_NAME: str
  NUMBER_LOG_UNENCRYPTED: int
  MAIL_MAILER: str
  MAIL_HOST: str
  MAIL_PORT: int
  MAIL_USERNAME: str
  MAIL_PASSWORD: str
  MAIL_TLS: bool
  MAIL_SSL: bool
  FORM_USER_URL: str
  PASSWORD_RESET_URL: str
  class Config:
    env_file = ".env"
    env_file_encoding = "utf-8"

settings = Settings()
