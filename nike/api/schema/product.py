from typing import Optional, List
from core import CommonException
from pydantic import BaseModel, Field, root_validator

class ProductRequest(BaseModel):
    """
        Model request product
    """
    name: str = Field(..., title="The username", min_length=1, max_length=256)
    quantity: int = Field(title="The username", default=0)
    price: str = Field(title="The price")
    weight: str = Field(title="The weight")
    height: str = Field(title="The height")
    images: Optional[List[str]] = Field(None, title="The image list")
    category_id: str = Field(..., title="The category of product")
    kind_id: str = Field(..., title="The kind of product")
    sale_id: str = Field(..., title="The sale")
    info: str = Field(..., title="The info of product")

    @root_validator(pre=True)
    def validate_product(cls, value):
        """
            Validate the name
        """
        return value

class ProductResponse(BaseModel):
    """
        Response product
    """
    id: int
    name: str
    flg_del: int

class ListProductResponse(BaseModel):
    """
        Response list product
    """
    item: Optional[List[ProductResponse]] = None
