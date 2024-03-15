"""
Edit print status request
"""

from pydantic import BaseModel, Field
from helpers.kbn import PrintStatus

class EditPrintStatusRequest(BaseModel):
  print_status: PrintStatus = Field(..., title="Action print status")
