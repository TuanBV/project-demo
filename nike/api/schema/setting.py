# import re
from typing import Optional, List
# from core import CommonException
from pydantic import BaseModel, Field, model_validator


class SettingRequest(BaseModel):
    """
        Model request setting
    """
    email: Optional[str] = Field(..., title="The email contact")
    number_phone: Optional[str] = Field(..., title="The number phone")
    address: Optional[str] = Field(..., title="The address")
    info: Optional[str] = Field(..., title="The info about company")
    fb_link: Optional[str] = Field(..., title="The facebook link")
    ig_link: Optional[str] = Field(..., title="The instagram link")
    tt_link: Optional[str] = Field(..., title="The tik tok link")
    tw_link: Optional[str] = Field(..., title="The twitter link")

    @model_validator(mode='after')
    def validate_model(self):
        """
            Validate the data request
        """
        return self

class SettingResponse(BaseModel):
    """
        Response setting
    """
    id: int
    email: str
    number_phone: str
    address: str
    info: str
    fb_link: str
    ig_link: str
    tt_link: str
    tw_link: str
    created_user: str
    created_date: str



class ListSettingResponse(BaseModel):
    """
        Response setting list
    """
    item: Optional[List[SettingResponse]] = None
