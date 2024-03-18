"""Logger"""

import logging
from logging.handlers import RotatingFileHandler
import watchtower
from pythonjsonlogger import jsonlogger
from helpers.const import IS_PROD

from setting import settings
from utils.date import get_current_time_obj


masked_log_patterns = ["email", "password", "token", "otp"]

loggers = {}



def get_logger():
  formatter = jsonlogger.JsonFormatter()
  if not IS_PROD:
    logging.basicConfig(level=logging.INFO, filename="./logs/app.log", filemode="a")
  name = "Product"
  global loggers

  if loggers.get(name):
    return loggers.get(name)
  else:
    logger = logging.getLogger("Product")
    logger.setLevel(logging.INFO)
    logger.addFilter(RedactingFilter())
    logger.propagate = False
    handler = watchtower.CloudWatchLogHandler(log_group_name=f"Product-{settings.ENVIRONMENT}", log_stream_name="Product-API")
    handler.setFormatter(formatter)
    if not IS_PROD:
      rotating_file_handler = RotatingFileHandler(filename="./logs/app.log", maxBytes=10485760, backupCount=50)
    logger.addHandler(rotating_file_handler)
    logger.addHandler(handler)
    loggers[name] = logger

    return logger


def rotation_filename():
  now = get_current_time_obj()
  return "app.log"+now.strftime("%Y-%m-%d")


class RedactingFilter(logging.Filter):
  """
    Filter logger need to encode
  """
  def __init__(self):
    super(RedactingFilter, self).__init__()
    self._patterns = masked_log_patterns

  def filter(self, record):
    if isinstance(record.msg, dict):
      for k in record.msg.keys():
        record.msg[k] = self.redact(record.msg[k])
    else:
      record.args = tuple(self.redact(arg) for arg in record.args)
    return True


  def redact(self, msg):
    if isinstance(msg, dict):
      for pattern in self._patterns:
        if pattern in msg:
          msg[pattern] = "<<TOP SECRET!>>"

    return msg
