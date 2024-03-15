"""
Initialization Package
"""

from .error import CrmException, CrmUnauthorizedException, CrmNoDataException, CrmPermissionException, CrmAppVersionException
from .message import ERR_MESSAGE, SUCCESS_MESSAGE
from .repository import CommonRepository
from .logger import get_logger
__all__ = [
  "CrmException",
  "CrmUnauthorizedException",
  "CrmNoDataException",
  "ERR_MESSAGE",
  "CommonRepository",
  "get_logger",
  "SUCCESS_MESSAGE",
  "CrmPermissionException",
  "CrmAppVersionException",
]
