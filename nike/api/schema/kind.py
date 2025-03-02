from typing import Optional, List
from core import CommonException
from pydantic import BaseModel, Field, root_validator

class KindRequest(BaseModel):
    """
        Model request kind
    """
    name: str = Field(..., title="The username", min_length=1, max_length=256)
    @root_validator(pre=True)
    def validate_kind(cls, value):
        """
            Validate the name
        """
        name = value.get('name')
        # Validate for name of kind
        if not name.strip():
            raise CommonException(message="Name cannot be empty or just whitespace.")
        if not name:
            raise CommonException(message="Name must have at least 1 character.")
        if len(name) > 256:
            raise CommonException(message="Name cannot be longer than 256 characters.")

        return value

class KindResponse(BaseModel):
    """
        Response kind
    """
    id: int
    name: str
    flg_del: int

class ListKindResponse(BaseModel):
    """
        Response list kind
    """
    item: Optional[List[KindResponse]] = None
