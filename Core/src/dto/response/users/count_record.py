"""
Count record response model
"""

from pydantic import BaseModel
from typing import Optional


class CountRecordResponse(BaseModel):
  """
    Count record response
  """
  add_cv: Optional[int] = 0
  contact_candidate: Optional[int] = 0
  confirm_test: Optional[int] = 0
  invite_interview: Optional[int] = 0
  interview_schedule: Optional[int] = 0
  candidate_assessment: Optional[int] = 0
  send_results: Optional[int] = 0
  update_offers: Optional[int] = 0
  send_forms: Optional[int] = 0
  candidate_confirm: Optional[int] = 0
  candidate_pass_list: Optional[int] = 0
