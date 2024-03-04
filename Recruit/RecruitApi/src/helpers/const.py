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
TIMEZONE = pytz.timezone("Asia/Tokyo")

# Url doc
URL_DOC = "http://localhost:8000/api/v1/docs"

MAX_LOG_SIZE = 10485760

BACKUP_COUNT = 10
