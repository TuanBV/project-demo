"""
Initialization Package
"""

from .list_add_cv import ListAddCvResponse
from .interviewed_candidates import ListInterviewedCandidateResponse
from .offer_candidates import OfferCandidateResponse
from .accept_offer_candidates import AcceptOfferCandidateResponse
from .candidate import CandidateItemResponse, CandidateConfirmResponse
from .candidates_confirm import CandidatesConfirmListResponse
from .candidates_list import CandidatesListResponse
from .list_contact_candidate import ListContactCandidateResponse
from .list_invite_interview import ListInviteInterviewResponse
from .form_candidate import FormCandidateResponse
from .candidates_list_view import CandidateViewResponse
from .candidates_pass_list import CandidatesPassListResponse
from .add_mail_candidates import AddMailCandidatesResponse
from .edit_mail_candidates import EditMailCandidatesResponse
from .list_confirm import ListConfirmTestResponse
from .list_interview_schedule import ListInterviewScheduleResponse
from .list_assessment import ListAssessmentResponse

__all__ = [
  "ListAddCvResponse",
  "CandidateItemResponse",
  "ListInterviewedCandidateResponse",
  "OfferCandidateResponse",
  "AcceptOfferCandidateResponse",
  "CandidateConfirmResponse",
  "CandidatesConfirmListResponse",
  "CandidatesListResponse",
  "ListContactCandidateResponse",
  "ListInviteInterviewResponse",
  "FormCandidateResponse",
  "CandidateViewResponse",
  "CandidatesPassListResponse",
  "AddMailCandidatesResponse",
  "EditMailCandidatesResponse",
  "ListConfirmTestResponse",
  "ListInterviewScheduleResponse",
  "ListAssessmentResponse",
]
