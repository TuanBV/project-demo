# pylint: disable=broad-except
"""
Common function
"""

import bcrypt as lib_bcrypt
import platform
import os
import uuid
from setting import settings
from helpers import context
from utils.date import get_current_time

# Hash password with bcrypt
# Params:
#   @password: password
# Output:
#   return: Password hashed
def bcrypt(password) -> str:
  return lib_bcrypt.hashpw(password.encode("utf-8"), lib_bcrypt.gensalt())


# Check password
# Params:
#   @password: password
#   @hashed: hashed
# Output:
#   return: Boolean
def checkpw(password, hashed):
  return lib_bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


# Generate request id
# Output:
#   return: request id
def get_request_id():
  return uuid.uuid1()


# Generate log
# Params:
#   @level: log level
#   @user_agent: user agent request
#   @url: url request
#   @request_id: request id
#   @log_type: type request
#   @method: request method
#   @content: content log
# Output:
#   return: Output log
def generate_log(level="INFO", user_agent="", url="", request_id="", log_type="", method="", content=""):
  user_id = ""
  shopcode = ""
  if context.user.value:
    # Get data user from context
    user = context.user.value
    user_id = user["user"]["id"]
    shopcode = user["user"]["shopcode"]
  log = {
    "ec2_name": platform.node(),
    "process_id": os.getpid(),
    "logName": settings.LOG_GROUP_NAME,
    "type": log_type,
    "request_id": request_id,
    "url": url,
    "user_agent": user_agent,
    "method": method,
    "level": level,
    "message": content,
    "user_id": user_id,
    "shopcode": shopcode,
  }
  time = get_current_time()
  if log_type == "RESPONSE":
    log["response_time"] = time
  elif log_type == "REQUEST":
    log["request_time"] = time
  else:
    log["time"] = time
  return log
