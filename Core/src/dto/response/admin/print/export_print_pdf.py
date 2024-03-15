"""
Export print pdf model
"""
from pydantic import BaseModel


class ExportPrintPdfResponse(BaseModel):
  item: str
