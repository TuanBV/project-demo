from typing import Optional, List
from core import CommonException
from pydantic import BaseModel, Field, root_validator

class CategoryRequest(BaseModel):
    """
        Model request category
    """
    name: str = Field(..., title="The username", min_length=1, max_length=256)
    @root_validator(pre=True)
    def validate_category(cls, value):
        """
            Validate the name
        """
        name = value.get('name')
        # Validate for name of category
        if not name.strip():
            raise CommonException(message="Name cannot be empty or just whitespace.")
        if not name:
            raise CommonException(message="Name must have at least 1 character.")
        if len(name) > 256:
            raise CommonException(message="Name cannot be longer than 256 characters.")

        return value

class CategoryResponse(BaseModel):
    """
        Response category
    """
    id: int
    name: str
    flg_del: int

class ListCategoryResponse(BaseModel):
    """
        Response list category
    """
    item: Optional[List[CategoryResponse]] = None
