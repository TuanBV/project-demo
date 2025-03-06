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

class ItemImage(BaseModel):
    """
        Model item image
    """
    id: int
    name: str
    path: str

class ProductResponse(BaseModel):
    """
        Response product
    """
    product_id: int
    quantity: int
    price: float
    height: float
    weight: float
    sale_id: Optional[int] = None
    name: str
    product_kind_id: int
    info: str
    kind_name: Optional[str] = None
    category_name: Optional[str] = None
    info: str
    images: Optional[List[ItemImage]] = None

class ListProductResponse(BaseModel):
    """
        Response list product
    """
    item: Optional[List[ProductResponse]] = None
