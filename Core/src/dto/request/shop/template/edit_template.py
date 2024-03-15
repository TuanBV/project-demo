"""
Edit template request model
"""

from typing import Optional
from pydantic import BaseModel, Field, validator
from core.error import CrmException
from core.message import ERR_MESSAGE
from helpers import kbn

class ActionType(BaseModel):
  id: int
  name: str

class EditTemplateRequest(BaseModel):
  """
  Edit template request
  """
  name: Optional[str] = Field(..., title="Template name", max_length=50)
  content: Optional[str] = Field(title="Template content", max_length=2000)
  comment: Optional[str] = Field(title="Template comment", max_length=50)
  note: Optional[str] = Field(title="Template note", max_length=50)
  title: Optional[str] = Field(title="Template title", max_length=100)
  action_type: ActionType

  @validator("action_type")
  def check_field_required(cls, action_type, values):
    # Template is email, survey title and content must not empty
    if action_type.id in [kbn.ActionType.EMAIL, kbn.ActionType.SURVEY] and values["title"] == "" and values["content"] == "":
      raise CrmException(message = ERR_MESSAGE.ERRMSG0064)

    return action_type

  pdf_flyer_address_size: str
  pdf_flyer_address_type: str
  pdf_flyer_address: str

  pdf_flyer_text_size: str
  pdf_flyer_text_type: str
  pdf_flyer_text: str

  pdf_post_card_size: str
  pdf_post_card_type: str
  pdf_post_card: str
