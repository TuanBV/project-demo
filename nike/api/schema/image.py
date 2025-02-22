import re
from datetime import datetime
from typing import Optional, List
from core import CommonException
from pydantic import BaseModel, Field, model_validator


class ImageRequest(BaseModel):
    """
        Model request image
    """
    file: Optional[str] = Field(..., title="The image file")
    file_ext: Optional[str] = Field(..., title="The ext file")
    file_size: Optional[int] = Field(..., title="The size file")

    @model_validator(mode='after')
    def validate_model(self):
        """
            Validate the data request
        """
        return self

class ImageResponse(BaseModel):
    """
        Response image
    """
    id: int
    name: str
    path: str

class ListImageResponse(BaseModel):
    """
        Response list image
    """
    item: Optional[List[ImageResponse]] = None
