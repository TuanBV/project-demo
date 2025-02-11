from typing import Optional, List
from core import CommonException
from pydantic import BaseModel, Field, root_validator

class SaleRequest(BaseModel):
    """
        Model request sale
    """
    name: str = Field(..., title="The username", min_length=1, max_length=256)
    discount: int = Field(..., title="The discount")
    start_date: str = Field(..., title="Start date")
    end_date: str = Field(..., title="End date")
    @root_validator(pre=True)
    def validate_sale(cls, value):
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

class SaleResponse(BaseModel):
    """
        Response sale
    """
    id: int
    name: str
    discount: int
    start_date: str
    end_date: str
    flg_del: int

class ListSaleResponse(BaseModel):
    """
        Response list sale
    """
    item: Optional[List[SaleResponse]] = None
