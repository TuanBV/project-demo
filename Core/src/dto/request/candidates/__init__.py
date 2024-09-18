"""
Initialization Package
"""

from .add import AddCandidateRequest
from .edit import EditCandidateRequest
from .edit_status import EditStatusCandidateRequest
from .add_contact import AddContactRequest
from .mail import CandidatesIdRequest
from .edit_start_join import EditStartJoinCandidateRequest
from .edit_form import EditFormCandidateRequest
from .edit_candidate_list import EditCandidateListRequest
from .mail_candidate import MailCandidate
from .edit_mail import EditMailCandidate
from .score import CandidateScoreRequest
from .eliminate_all_test import EliminateAllTestRequest
from .eliminate_test import EliminateTestRequest
from .confirm_all_test import ConfirmAllTestRequest
from .interview_infor import AddInterviewInforRequest
from .interview_infor import EditInterviewInforRequest
from .assessment import AssessmentRequest, AdminEvaluateRequest
from .candidate_black_list import CandidateBlackListRequest

__all__ = [
  "AddCandidateRequest",
  "EditCandidateRequest",
  "EditStatusCandidateRequest",
  "AddContactRequest",
  "CandidatesIdRequest",
  "EditStartJoinCandidateRequest",
  "EditFormCandidateRequest",
  "EditCandidateListRequest",
  "MailCandidate",
  "EditMailCandidate",
  "CandidateScoreRequest",
  "EliminateAllTestRequest",
  "EliminateTestRequest",
  "ConfirmAllTestRequest",
  "AddInterviewInforRequest",
  "EditInterviewInforRequest",
  "AssessmentRequest",
  "AdminEvaluateRequest",
  "CandidateBlackListRequest",
]
