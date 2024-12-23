"""Logger"""

import types
import logging
from logging.handlers import RotatingFileHandler
# import watchtower
from pythonjsonlogger import jsonlogger
from setting import settings
from helpers import common, const

masked_log_patterns = ["mail", "password", "token"]

loggers = {}

def request(self, url="", request_id="", method="", user_agent="", content="") -> None:
  """Handle log request

  Args:
      url (string): request url
      request_id (string): request id
      method (string): request method
      user_agent (string): request user agent
      content (string): log content
  """

  self.setLevel(logging.INFO)
  self.info(common.generate_log(user_agent=user_agent, url=url, request_id=request_id,
                                log_type="REQUEST", method=method, content=content))


def err_response(self, url="", request_id="", method="", user_agent="", content=""):
  """Handle log error response

  Args:
      url (string): request url
      request_id (string): request id
      method (string): request method
      user_agent (string): request user agent
      content (string): log content
  """

  self.setLevel(logging.ERROR)
  self.error(common.generate_log("ERROR", user_agent, url, request_id,
                                 "ERROR", method, content))


def response(self, url="", request_id="", method="", user_agent="", content=""):
  """Handle log response

  Args:
      url (string): request url
      request_id (string): request id
      method (string): request method
      user_agent (string): request user agent
      content (string): log content
  """

  self.setLevel(logging.INFO)
  self.info(common.generate_log(user_agent=user_agent, url=url, request_id=request_id,
                                log_type="RESPONSE", method=method, content=content))


def get_logger():
  formatter = jsonlogger.JsonFormatter()
  logging.basicConfig(level=logging.INFO, filename=settings.LOG_FILE_NAME, filemode="a")
  name = settings.LOG_GROUP_NAME
  global loggers

  if loggers.get(name):
    return loggers.get(name)
  else:
    logger = logging.getLogger(name)

    # Add logger method
    logger.request = types.MethodType(request, logger)
    logger.response = types.MethodType(response, logger)
    logger.err_response = types.MethodType(err_response, logger)

    logger.setLevel(logging.INFO)
    logger.addFilter(RedactingFilter())
    logger.propagate = False
    # handler = watchtower.CloudWatchLogHandler(log_group_name=f"{name}-{settings.ENVIRONMENT}", log_stream_name="Api")
    # handler.setFormatter(formatter)
    rotating_file_handler = RotatingFileHandler(filename=settings.LOG_FILE_NAME, maxBytes=const.MAX_LOG_SIZE,
                                                backupCount=const.BACKUP_COUNT)
    logger.addHandler(rotating_file_handler)
    # logger.addHandler(handler)
    loggers[name] = logger

    return logger


class RedactingFilter(logging.Filter):
  """
    Filter logger need to encode
  """
  def __init__(self):
    super(RedactingFilter, self).__init__()
    self._patterns = masked_log_patterns


  def filter(self, record):
    if isinstance(record.msg, dict):
      for key in record.msg.keys():
        record.msg[key] = self.redact(record.msg[key])
    else:
      record.args = tuple(self.redact(arg) for arg in record.args)
    return True


  def redact(self, msg):
    if isinstance(msg, dict):
      for pattern in self._patterns:
        if "body" in msg and isinstance(msg["body"], dict) and pattern in msg["body"]:
          msg["body"][pattern] = self.msg_decode(msg["body"][pattern])
        elif "payload" in msg and isinstance(msg["payload"], dict) and pattern in msg["payload"]:
          msg["payload"][pattern] = self.msg_decode(msg["payload"][pattern])
    return msg


  def msg_decode(self, msg):
    msg_len = len(msg)
    if msg_len <= settings.NUMBER_LOG_UNENCRYPTED:
      msg = msg[:1] + "*" * (settings.NUMBER_LOG_UNENCRYPTED - 1)
    else:
      msg = msg[:settings.NUMBER_LOG_UNENCRYPTED] + "*" * (msg_len - settings.NUMBER_LOG_UNENCRYPTED)
    return msg
