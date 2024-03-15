"""
Add action request model
"""

from typing import List, Optional
from pydantic import BaseModel, Field, validator
from core.error import CrmException

from core.message import ERR_MESSAGE
from utils.date import get_object_date

class PdfItem(BaseModel):
  pdf_file: str
  pdf_ext: str
  pdf_size: str

class ActionBody(BaseModel):
  action_note: Optional[str] = None
  list_pdf: Optional[List[PdfItem]] = None
  body: Optional[str] = None
  title: Optional[str] = None

class ActionType(BaseModel):
  id: int
  name: str
  color: str

class LoopType(BaseModel):
  freq: str
  interval: str
  by_day: str
  until: str
  count: str

class AddActionRequest(BaseModel):
  """
  Add action request
  """
  name: Optional[str] = Field(..., title="Action name", min_length=1, max_length=100)
  action_body: ActionBody
  action_type: ActionType
  delivery_time: Optional[str] = Field(..., min_length=1, title="Delivery time")

  @validator("delivery_time")
  def check_delivery_time(cls, delivery_time):
    # If the action submission date is in a different format
    # an error will be returned
    try:
      get_object_date(delivery_time, "%Y/%m/%d %H:%M:%S")
    except ValueError as e:
      raise CrmException(message = ERR_MESSAGE.ERRMSG0002) from e

    return delivery_time

  template_id: Optional[int] = None
  condition_filter_id: Optional[int] = None
  customer_tag_id: Optional[int] = None

  @validator("customer_tag_id")
  def must_have_customer_tag_or_condition_filter(cls, customer_tag_id, values):
    # Condition and customer tag
    # both empty will return an error
    if not customer_tag_id and not values["condition_filter_id"]:
      raise CrmException(message = ERR_MESSAGE.ERRMSG0010)

    # Condition and customer tag
    # both have a value will return an error
    elif values["condition_filter_id"] and customer_tag_id:
      raise CrmException(message = ERR_MESSAGE.ERRMSG0011)

    return customer_tag_id

  loop_type: LoopType

  @validator("loop_type")
  def check_loop_type_data(cls, loop_type, values):
    # if the end date is less than the submission
    # date the action will return an error
    if loop_type.until != "" and loop_type.until < values["delivery_time"]:
      raise CrmException(message = ERR_MESSAGE.ERRMSG0007)

    # If the number of iterations not empty
    if loop_type.count != "":
      # the number of iterations smaller than or equal to 1 or interval greater than 1000 will raise error
      if int(loop_type.count) < 1 or int(loop_type.count) > 1000:
        raise CrmException(message = ERR_MESSAGE.ERRMSG0008)

    # If interval not empty
    if loop_type.interval != "":
      # interval smaller than or equal to 1 or interval greater than 1000 will raise error
      if int(loop_type.interval) < 1 or int(loop_type.interval) > 1000:
        raise CrmException(message = ERR_MESSAGE.ERRMSG0009)

    return loop_type
