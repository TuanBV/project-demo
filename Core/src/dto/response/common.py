"""
Common model
"""
from typing import Generic, TypeVar
from pydantic.generics import GenericModel


DataPayload = TypeVar("DataPayload")

class CRMResponse(GenericModel, Generic[DataPayload]):
  code: str
  message: str
  payload: DataPayload
