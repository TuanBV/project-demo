"""
Export shop csv model
"""
from pydantic import BaseModel


class ExportShopCsvResponse(BaseModel):
  item: str
