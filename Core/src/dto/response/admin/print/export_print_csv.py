"""
Export print csv model
"""
from pydantic import BaseModel


class ExportPrintCsvResponse(BaseModel):
  item: str
