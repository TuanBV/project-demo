# pylint: disable=broad-except
"""
Common function
"""

import re
import bcrypt as lib_bcrypt
import platform
import os
import uuid
from datetime import timedelta
from setting import settings
from helpers import context, kbn
from helpers.const import TITLE_CALENDAR
from utils.date import get_current_time, format_date_time, get_object_date

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
  user_code = ""
  if context.user.value:
    # Get data user from context
    user = context.user.value
    user_code = user["employee_code"]
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
    "user_code": user_code,
  }
  time = format_date_time(get_current_time(), "%Y/%m/%d %H:%M:%S")
  if log_type == "RESPONSE":
    log["response_time"] = time
  elif log_type == "REQUEST":
    log["request_time"] = time
  else:
    log["time"] = time
  return log

# Remove accented
# Params:
#   @candidate_name: Candidate name
# Output:
#   return: String with no accented
def no_accent_vietnamese(candidate_name):
  candidate_name = re.sub("[áàảãạăắằẳẵặâấầẩẫậ]", "a", candidate_name)
  candidate_name = re.sub("[ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬ]", "A", candidate_name)
  candidate_name = re.sub("[éèẻẽẹêếềểễệ]", "e", candidate_name)
  candidate_name = re.sub("[ÉÈẺẼẸÊẾỀỂỄỆ]", "E", candidate_name)
  candidate_name = re.sub("[óòỏõọôốồổỗộơớờởỡợ]", "o", candidate_name)
  candidate_name = re.sub("[ÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢ]", "O", candidate_name)
  candidate_name = re.sub("[íìỉĩị]", "i", candidate_name)
  candidate_name = re.sub("[ÍÌỈĨỊ]", "I", candidate_name)
  candidate_name = re.sub("[úùủũụưứừửữự]", "u", candidate_name)
  candidate_name = re.sub("[ÚÙỦŨỤƯỨỪỬỮỰ]", "U", candidate_name)
  candidate_name = re.sub("[ýỳỷỹỵ]", "y", candidate_name)
  candidate_name = re.sub("[ÝỲỶỸỴ]", "Y", candidate_name)
  candidate_name = candidate_name.replace("đ", "d")
  candidate_name = candidate_name.replace("Đ", "D")
  candidate_name = candidate_name.replace(" ", "_")

  return candidate_name
