"""
Const environment
"""
from box import Box
from setting import settings
import pytz

CODE = Box({
  "API": {
    "SUCCESS": 0,
    "INVALID_REQUEST": "ERRAPI401",
    "ERROR": "ERRAPI400",
    "NOT_FOUND": "ERRAPI404",
    "SYSTEM_ERROR": "ERRAPI999",
    "NO_CONTENT": "ERRAPI204",
    "SEND_MAIL_FAILED": "ERRAPI500",
    "INVALID_PERMISSION": "ERRAPI403",
    "INVALID_TOKEN": "ERRAPI998",
    "APP_VERSION_ERROR": "ERRAPI503",
  },
  "HTTP_STATUS": {
    "SUCCESS": 200,
    "ERROR": 400,
    "NOT_FOUND": 404,
    "UNAUTHORIZED": 401,
    "NO_CONTENT": 204,
    "SYSTEM_ERROR": 500,
    "APP_VERSION_ERROR": 503,
  },
  "ERROR": {
    "UNAUTHORIZED": 902,
  },
})

# Key authorize
JWT = Box({
  "SECRET": {
    "KEY": settings.JWT_SECRET,
    "ALGORITHM": "HS256",
  },
  "EXPIRED": 7*24*3600 # 30 minute
})

# cookie lifetime
MAX_AGE = 7*24*3600 # 30 minute

# Timezone
TIMEZONE = pytz.timezone("Asia/Ho_Chi_Minh")

# Url doc
URL_DOC = "http://localhost:8081/api/v1/docs"

MAX_LOG_SIZE = 10485760

BACKUP_COUNT = 10

# Size of Cv file
MAX_CV_SIZE = 10*1024*1024

# Patterns
REGEX_TELEPHONE_NO = r"^0(\d{9,10})$"

# Regexp for number only
REGEXP_NUMBER = r"^\d+$"

# Regexp for decimal
REGEXP_DECIMAL = r"^\d{1,5}$|(?=^.{1,5}$)^\d+\.\d{0,1}$"

REGEX_EMAIL = r"^[\w.!#$%&’*+\/=?^`{|}-]+@([\w-]+\.)+[\w-]{2,}$"

REGEX_PASSWORD = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,64}$"

# Password default when create user
PASSWORD_DEFAULT = "Test123@"

INTERVIEW_STATUS = {
  0: "Chuẩn bị PV",
  1: "Pass",
  2: "Trượt",
  8: "Không đến làm bài test",
  9: "Không đến PV",
}

TYPE_KBN = {
  0: "Làm bài test",
  1: "PV vòng 1",
  2: "PV vòng 2",
}

TITLE_CALENDAR = {
  0: "Lịch test ứng viên",
  1: "Phỏng vấn ứng viên vòng 1",
  2: "Phỏng vấn ứng viên vòng 2",
}

# Day of week
DAY_OF_WEEK = {
  0: "Thứ hai",
  1: "Thứ ba",
  2: "Thứ tư",
  3: "Thứ năm",
  4: "Thứ sáu",
  5: "Thứ bảy",
  6: "Chủ nhật",
}

# Max score
MAX_SCORE = 10

# Expire date token (days)
TOKEN_EXPIRED = 7

# Number of experiences
NUMBER_EXPERIENCES = 2

# Max file credentials Google calendar
MAX_CREDENTIALS_FILE = 1024*1024
