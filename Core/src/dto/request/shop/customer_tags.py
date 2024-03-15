"""
Customer tags model
"""
from typing import List
from pydantic import BaseModel

# Check token model
class CustomerTagsRequest(BaseModel):
  title: str
  list_customer_no: List[str]
