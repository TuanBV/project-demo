"""
Context
"""
from contextvars import ContextVar

class ContextWrapper:
  """Context Wrapper"""

  def __init__(self, value):
    self.__value: ContextVar = value

  def set(self, value):
    return self.__value.set(value)

  def reset(self):
    self.__value.set(None)

  def __module__(self):
    return self.__value.get()

  @property
  def value(self):
    return self.__value.get()


user = ContextWrapper = ContextWrapper(ContextVar("user", default=None))
