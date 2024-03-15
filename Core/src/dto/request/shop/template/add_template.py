"""
Add template request model
"""

from typing import List, Optional
from pydantic import BaseModel, Field, validator
from core.error import CrmException
from core.message import ERR_MESSAGE
from helpers import kbn
from utils.service_template import check_file_pdf_template

class ActionType(BaseModel):
  id: int
  name: str

class AddTemplateRequest(BaseModel):
  """
  Add template request
  """
  id: Optional[int] = None
  name: Optional[str] = Field(..., title="Template name", max_length=50)
  content: Optional[str] = Field(title="Template content", max_length=2000)
  comment: Optional[str] = Field(title="Template comment", max_length=50)
  note: Optional[str] = Field(title="Template note", max_length=50)
  title: Optional[str] = Field(title="Template title", max_length=100)
  pdf: Optional[List[str]] = None
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


  @validator("pdf_flyer_address")
  def check_flyer_address_file(cls, pdf_file, values):
    # Validate file pdf_backside of flyer
    pdf_file = pdf_file.strip()

    if pdf_file != "":
      flag_check = check_file_pdf_template(values["id"], pdf_file, values["pdf_flyer_address_size"], values["pdf_flyer_address_type"])

      # File invalid will raise error
      if not flag_check:
        raise CrmException(message = ERR_MESSAGE.ERRMSG0168)

    return pdf_file

  pdf_flyer_text_size: str
  pdf_flyer_text_type: str
  pdf_flyer_text: str

  @validator("pdf_flyer_text")
  def check_flyer_text_file(cls, pdf_file, values):
    # Validate file pdf_frontside of flyer
    pdf_file = pdf_file.strip()

    if pdf_file != "":
      flag_check = check_file_pdf_template(values["id"], pdf_file, values["pdf_flyer_text_size"], values["pdf_flyer_text_type"])

      # File invalid will raise error
      if not flag_check:
        raise CrmException(message = ERR_MESSAGE.ERRMSG0167)

    return pdf_file

  pdf_post_card_size: str
  pdf_post_card_type: str
  pdf_post_card: str

  @validator("pdf_post_card")
  def check_post_card_file(cls, pdf_file, values):
    # Validate file pdf_frontside of flyer
    pdf_file = pdf_file.strip()

    if pdf_file != "":
      flag_check = check_file_pdf_template(values["id"], pdf_file, values["pdf_post_card_size"], values["pdf_post_card_type"])

      # File invalid will raise error
      if not flag_check:
        raise CrmException(message = ERR_MESSAGE.ERRMSG0166)

    return pdf_file
