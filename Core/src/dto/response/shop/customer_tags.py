"""
Customer tags model
"""
from typing import List
from pydantic import BaseModel

# Save customer tags model
class AddCustomerTagsResponse(BaseModel):
  items: str

# Get customer tags model
class ListCustomerTags(BaseModel):
  shop_no: str
  title: str
  id: int
  count_customer: int

class CustomerTagsResponse(BaseModel):
  item: List[ListCustomerTags]
