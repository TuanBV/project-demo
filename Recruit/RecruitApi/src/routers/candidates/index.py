"""
Candidate router
"""
from fastapi import APIRouter, Depends
from containers import Container
from dto.response.common import Response
from dto.request.candidates import (AddCandidateRequest, AddContactRequest,
  EditStatusCandidateRequest, CandidatesIdRequest, EditStartJoinCandidateRequest, EditFormCandidateRequest, CandidateScoreRequest,
  EliminateTestRequest, EliminateAllTestRequest, ConfirmAllTestRequest, AddInterviewInforRequest, EditInterviewInforRequest,
  AssessmentRequest, AdminEvaluateRequest)
from dto.response.candidates import (ListAddCvResponse, CandidateItemResponse, ListContactCandidateResponse,
  ListInterviewedCandidateResponse, OfferCandidateResponse, AcceptOfferCandidateResponse, FormCandidateResponse, ListInviteInterviewResponse,
  ListConfirmTestResponse, ListInterviewScheduleResponse, ListAssessmentResponse)
from routers.common import SSVRoute
from dependency_injector.wiring import inject, Provide
from recruit_candidates import CandidatesService
from recruit_add_cv import AddCvService
from recruit_contact_candidate import ContactCandidateService
from recruit_result_candidates import ResultCandidatesService
from recruit_offer_candidates import OfferCandidatesService
from recruit_invite_interview import InviteInterviewService
from recruit_accept_offer_candidates import AcceptOfferCandidatesService
from recruit_confirm_test import ConfirmTestService
from recruit_interview_schedule import InterviewScheduleService
from recruit_candidate_assessment import CandidateAssessmentService
from helpers.response import (ok)
from helpers import context
from dependencies import authorized_user

candidate_routers = APIRouter(route_class=SSVRoute, tags=["candidates"], prefix="/api/v1",
    responses={
      200: {
        "model": Response
      },
      401: {
        "model": Response[dict]
      },
      404: {
        "description": "No data",
        "model": Response[dict]
      },
      400: {
        "description": "API ERROR",
        "model": Response[dict]
      },
      500: {
        "description": "SYSTEM ERROR",
        "model": Response[dict]
      },
    },
  )


# Add candidates
# Param:
#   @body: Data request
#   @add_cv_service: Add Cv service
# Output:
#   return: HTTP response
@candidate_routers.post("/candidates/add-cv", tags=["candidates"], responses={200: {"model": Response[CandidateItemResponse]}}, dependencies=[Depends(authorized_user)])
@inject
async def add_cv(body: AddCandidateRequest, add_cv_service: AddCvService = Depends(Provide(Container.add_cv_service))):
  user = context.user.value

  data = {
    "candidate": body.dict(),
    "employee_code": user["employee_code"]
  }

  result_candidate = add_cv_service.add(data)

  payload = CandidateItemResponse(**result_candidate)

  response = ok(data=payload.dict())

  return response


# Get list add cv
# Param:
#   @add_cv_service: Add Cv service
# Output:
#   return: HTTP response
@candidate_routers.get("/candidates/add-cv", tags=["candidates"], responses={200: {"model": Response[ListAddCvResponse]}}, dependencies=[Depends(authorized_user)])
@inject
async def get_list_add_cv(add_cv_service: AddCvService = Depends(Provide(Container.add_cv_service))):

  result_list_candidates = add_cv_service.get_list()

  payload = ListAddCvResponse(**result_list_candidates)
  response = ok(data=payload.dict())

  return response


# Edit candidate status
# Params:
#   @candidates_service: Candidates service
# Output:
#   return: HTTP response
@candidate_routers.put("/candidates/status", tags=["candidates"], responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@inject
async def edit_status(body: EditStatusCandidateRequest, candidates_service: CandidatesService = Depends(Provide(Container.candidates_service))):

  user = context.user.value

  data = {
    "data_request": body.dict(),
    "employee_code": user["employee_code"]
  }

  candidates_service.edit_status(data)

  return ok()


# Get list contact candidate
# Param:
#   @contact_candidate_service: Contact candidate service
# Output:
#   return: HTTP response
@candidate_routers.get("/candidates/contact-candidate", tags=["candidates"], responses={200: {"model": Response[ListContactCandidateResponse]}},
  dependencies=[Depends(authorized_user)])
@inject
async def get_list_contact(contact_candidate_service: ContactCandidateService = Depends(Provide(Container.contact_candidate_service))):
  result_list_candidates = contact_candidate_service.get_list()

  payload = ListContactCandidateResponse(**result_list_candidates)
  response = ok(data=payload.dict())

  return response


# Add contact
# Param:
#   @body: Data request
#   @add_cv_service: Contact candidate service
# Output:
#   return: HTTP response
@candidate_routers.post("/candidates/contact-candidate", tags=["candidates"], responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@inject
async def add_contact(body: AddContactRequest, contact_candidate_service: ContactCandidateService = Depends(Provide(Container.contact_candidate_service))):
  user = context.user.value

  data = {
    "candidate": body.dict(),
    "employee_code": user["employee_code"]
  }

  contact_candidate_service.add(data)

  return ok()


# Get interviewed candidates
# Params:
#   @candidates_service: Candidates service
# Output:
#   return: HTTP response
@candidate_routers.get("/candidates/interviewed/{option_value:int}", tags=["candidates"],
                       responses={200: {"model": Response[ListInterviewedCandidateResponse]}},
                       dependencies=[Depends(authorized_user)])
@inject
async def get_interviewed_candidates(option_value: int, result_candidates_service: ResultCandidatesService = Depends(Provide(Container.result_candidates_service))):
  result_list_candidates = result_candidates_service.get_interviewed_candidates(option_value)
  payload = ListInterviewedCandidateResponse(**result_list_candidates)
  return ok(data=payload.dict())


# Send mail candidates
# Params:
#   @result_candidates_service: Result candidates service
# Output:
#   return: HTTP response
@candidate_routers.post("/candidates/send-result-mails", tags=["candidates"],
                        responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@inject
async def send_mail_candidates(
  body: CandidatesIdRequest,
  result_candidates_service: ResultCandidatesService = Depends(Provide(Container.result_candidates_service))
):
  await result_candidates_service.send_mail_candidates(body.candidates_id)
  return ok()


# Create mail result candidates
# Params:
#   @candidates_service: Candidates service
# Output:
#   return: HTTP response
@candidate_routers.post("/candidates/result-mails", tags=["candidates"],
                        responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@inject
async def create_mail_result_candidates(
  body: CandidatesIdRequest,
  result_candidates_service: ResultCandidatesService = Depends(Provide(Container.result_candidates_service))
):
  mails = result_candidates_service.create_mail_candidates(body.candidates_id)
  return ok(data=mails)


# Create offer candidates
# Params:
#   @candidates_service: Candidates service
# Output:
#   return: HTTP response
@candidate_routers.get("/candidates/offer", tags=["candidates"],
                       responses={200: {"model": Response[OfferCandidateResponse]}}, dependencies=[Depends(authorized_user)])
@inject
async def get_offer_candidates(offer_candidates_service: OfferCandidatesService = Depends(Provide(Container.offer_candidates_service))):
  candidates = offer_candidates_service.get_list()
  candidates = OfferCandidateResponse(**candidates)
  return ok(data=candidates.dict())


# Get list candidate interview
# Param:
#   @invite_interview_service: Invite interview service
# Output:
#   return: HTTP response
@candidate_routers.get("/candidates/invite-interview", tags=["candidates"], responses={200: {"model": Response[ListInviteInterviewResponse]}},
    dependencies=[Depends(authorized_user)])
@inject
async def get_list_invite_interview(invite_interview_service: InviteInterviewService = Depends(Provide(Container.invite_interview_service))):

  result_list_candidates = invite_interview_service.get_list()

  payload = ListInviteInterviewResponse(**result_list_candidates)
  response = ok(data=payload.dict())

  return response


# Create mail invite candidates
# Params:
#   @invite_interview_service: Invite interview service
# Output:
#   return: HTTP response
@candidate_routers.post("/candidates/invite-interview/create-invite-mails", tags=["candidates"], responses={200: {"model": Response[dict]}},
  dependencies=[Depends(authorized_user)])
@inject
async def create_mail_invite_candidates(body: CandidatesIdRequest, invite_interview_service: InviteInterviewService = Depends(Provide(Container.invite_interview_service))):
  mails = invite_interview_service.create_mail_invite_candidates(body.candidates_id)
  return ok(data=mails)


# Send mail candidates
# Params:
#   @result_candidates_service: Result candidates service
# Output:
#   return: HTTP response
@candidate_routers.post("/candidates/invite-interview/send-invite-mails", tags=["candidates"], responses={200: {"model": Response[dict]}},
  dependencies=[Depends(authorized_user)])
@inject
async def send_mail_invite_candidates(body: CandidatesIdRequest, invite_interview_service: InviteInterviewService = Depends(Provide(Container.invite_interview_service))):
  user = context.user.value

  await invite_interview_service.send_mail_candidates(body.candidates_id, user["employee_code"])

  return ok()


# Get accept offer candidates
# Params:
#   @accept_offer_candidates_service: Accept offer candidates service
# Output:
#   return: HTTP response
@candidate_routers.get("/candidates/accept-offer", tags=["candidates"],
                       responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@inject
async def get_received_offer_candidates(
  accept_offer_candidates_service: AcceptOfferCandidatesService = Depends(Provide(Container.accept_offer_candidates_service))
):
  candidates = accept_offer_candidates_service.get_list()
  candidates = AcceptOfferCandidateResponse(**candidates)
  return ok(data=candidates.dict())


# Edit start join candidate
# Params:
#   @accept_offer_candidates_service: Accept offer candidates service
# Output:
#   return: HTTP response
@candidate_routers.put("/candidates/start-join/{candidate_id:int}", tags=["candidates"],
                       responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@inject
async def edit_start_join_candidates(
  candidate_id: int,
  body: EditStartJoinCandidateRequest,
  accept_offer_candidates_service: AcceptOfferCandidatesService = Depends(Provide(Container.accept_offer_candidates_service))
):
  accept_offer_candidates_service.edit_start_join(candidate_id, body.start_join_date)
  return ok()


# Create mail form candidates
# Params:
#   @accept_offer_candidates_service: Candidates service
# Output:
#   return: HTTP response
@candidate_routers.post("/candidates/form-mails", tags=["candidates"],
                        responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@inject
async def create_mail_form_candidates(
  body: CandidatesIdRequest,
  accept_offer_candidates_service: AcceptOfferCandidatesService = Depends(Provide(Container.accept_offer_candidates_service))
):
  mails = accept_offer_candidates_service.create_mail_candidates(body.candidates_id)
  return ok(data=mails)


# Edit start join candidate
# Params:
#   @body: Body
#   @accept_offer_candidates_service: Accept offer candidates service
# Output:
#   return: HTTP response
@candidate_routers.post("/candidates/form/send", tags=["candidates"],
                        responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@inject
async def send_form_candidates(
  body: CandidatesIdRequest,
  accept_offer_candidates_service: AcceptOfferCandidatesService = Depends(Provide(Container.accept_offer_candidates_service))
):
  await accept_offer_candidates_service.send_mails(body.candidates_id)
  return ok()


# Check and get form candiate
# Params:
#   @accept_offer_candidates_service: Accept offer candidates service
# Output:
#   return: HTTP response
@candidate_routers.get("/candidates/form/{token:str}", tags=["candidates"], responses={200: {"model": Response[dict]}})
@inject
async def get_form_candidate(token: str, accept_offer_candidates_service: AcceptOfferCandidatesService = Depends(Provide(Container.accept_offer_candidates_service))):
  candidate = accept_offer_candidates_service.get_candidate_by_token(token)
  candidate = FormCandidateResponse(**candidate)
  return ok(data=candidate.dict())


# Edit form candidate
# Params:
#   @token: Token
#   @candidates_service: Candidates service
# Output:
#   return: HTTP response
@candidate_routers.put("/candidates/form/{token:str}", tags=["candidates"], responses={200: {"model": Response[dict]}})
@inject
async def edit_form_candidate(token: str, body: EditFormCandidateRequest,
                              accept_offer_candidates_service: AcceptOfferCandidatesService = Depends(Provide(Container.accept_offer_candidates_service))):
  accept_offer_candidates_service.edit_candidate_by_token(token, body.dict())
  return ok()


# Get list candidate confirm test
# Param:
#   @invite_interview_service: Invite interview service
# Output:
#   return: HTTP response
@candidate_routers.get("/candidates/test", tags=["candidates"], responses={200: {"model": Response[ListConfirmTestResponse]}},
    dependencies=[Depends(authorized_user)])
@inject
async def get_list_confirm(confirm_test_service: ConfirmTestService = Depends(Provide(Container.confirm_test_service))):

  result_list_candidates = confirm_test_service.get_list()

  payload = ListConfirmTestResponse(**result_list_candidates)
  response = ok(data=payload.dict())

  return response


# Get list candidate assessment
# Param:
#   @candidate_assessment_service: Candidate assessment service
# Output:
#   return: HTTP response
@candidate_routers.get("/candidates/assessment", tags=["candidates"], responses={200: {"model": Response[ListAssessmentResponse]}},
    dependencies=[Depends(authorized_user)])
@inject
async def get_list_assessment(candidate_assessment_service: CandidateAssessmentService = Depends(Provide(Container.candidate_assessment_service))):

  result_list_candidates = candidate_assessment_service.get_list()

  payload = ListAssessmentResponse(**result_list_candidates)
  response = ok(data=payload.dict())

  return response


# Assessment candidate
# Param:
#   @candidate_assessment_service: Candidate assessment service
# Output:
#   return: HTTP response
@candidate_routers.put("/candidates/assessment/{candidate_id:int}", tags=["candidates"], responses={200: {"model": Response[ListAssessmentResponse]}},
    dependencies=[Depends(authorized_user)])
@inject
async def assessment_candidate(candidate_id: int, body: AssessmentRequest, candidate_assessment_service: CandidateAssessmentService = Depends(
    Provide(Container.candidate_assessment_service))):
  user = context.user.value

  data_assessment = body.dict()
  data_assessment["candidate_id"] = candidate_id
  data_assessment["employee_code"] = user["employee_code"]

  candidate_assessment_service.assessment(data_assessment)

  return ok()


# Eliminate candidate in candidate-assessment
# Param:
#   @candidate_assessment_service: Candidate assessment service
# Output:
#   return: HTTP response
@candidate_routers.put("/candidates/assessment/evaluate/{candidate_id:int}", tags=["candidates"], responses={200: {"model": Response[ListAssessmentResponse]}},
    dependencies=[Depends(authorized_user)])
@inject
async def admin_evaluate(candidate_id: int, body: AdminEvaluateRequest, candidate_assessment_service: CandidateAssessmentService = Depends(
    Provide(Container.candidate_assessment_service))):
  user = context.user.value

  data_assessment = body.dict()

  data_assessment["candidate_id"] = candidate_id
  data_assessment["employee_code"] = user["employee_code"]

  candidate_assessment_service.admin_evaluate(data_assessment)

  return ok()



# Save score candidate
# Param:
#   @confirm_test_service: Confirm test service
# Output:
#   return: HTTP response
@candidate_routers.put("/candidates/test/score", tags=["candidates"], responses={200: {"model": Response[dict]}},
    dependencies=[Depends(authorized_user)])
@inject
async def save_score(body: CandidateScoreRequest, confirm_test_service: ConfirmTestService = Depends(Provide(Container.confirm_test_service))):
  user = context.user.value

  data_score = body.dict()
  data_score["employee_code"] = user["employee_code"]

  confirm_test_service.save_score(data_score)

  return ok()


# Eliminate test
# Params:
#   @confirm_test_service: Confirm test service
# Output:
#   return: HTTP response
@candidate_routers.put("/candidates/test/{candidate_id:int}", tags=["candidates"], responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@inject
async def eliminate_test(candidate_id: int, body: EliminateTestRequest, confirm_test_service: ConfirmTestService = Depends(Provide(Container.confirm_test_service))):

  user = context.user.value

  data = {
    "candidate_id": candidate_id,
    "flag_not_test": body.dict()["flag_not_test"],
    "employee_code": user["employee_code"]
  }

  confirm_test_service.eliminate(data)

  return ok()


# Eliminate all test
# Params:
#   @confirm_test_service: Confirm test service
# Output:
#   return: HTTP response
@candidate_routers.put("/candidates/test/eliminate-all", tags=["candidates"], responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@inject
async def eliminate_all_test(body: EliminateAllTestRequest, confirm_test_service: ConfirmTestService = Depends(Provide(Container.confirm_test_service))):

  user = context.user.value

  data =  body.dict()

  data["employee_code"] = user["employee_code"]

  confirm_test_service.eliminate_all(data)

  return ok()


# Confirm all test
# Params:
#   @confirm_test_service: Confirm test service
# Output:
#   return: HTTP response
@candidate_routers.put("/candidates/test/confirm", tags=["candidates"], responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@inject
async def confirm_all_test(body: ConfirmAllTestRequest, confirm_test_service: ConfirmTestService = Depends(Provide(Container.confirm_test_service))):

  user = context.user.value

  data =  body.dict()

  data["employee_code"] = user["employee_code"]

  confirm_test_service.confirm_all(data)

  return ok()


# Get list candidate have interview
# Param:
#   @confirm_test_service: Confirm test service
# Output:
#   return: HTTP response
@candidate_routers.get("/candidates/interview-schedule", tags=["candidates"], responses={200: {"model": Response[ListInterviewScheduleResponse]}},
    dependencies=[Depends(authorized_user)])
@inject
async def get_list_interview_schedule(interview_schedule_service: InterviewScheduleService = Depends(Provide(Container.interview_schedule_service))):
  result_list_candidates = interview_schedule_service.get_list()

  payload = ListInterviewScheduleResponse(**result_list_candidates)
  response = ok(data=payload.dict())

  return response


# Add interview information
# Param:
#   @interview_schedule_service: Interview schedule service
# Output:
#   return: HTTP response
@candidate_routers.post("/candidates/interview-schedule/{candidate_id:int}", tags=["candidates"], responses={200: {"model": Response[dict]}},
    dependencies=[Depends(authorized_user)])
@inject
async def add_interview_infor(candidate_id: int, body: AddInterviewInforRequest,
    interview_schedule_service: InterviewScheduleService = Depends(Provide(Container.interview_schedule_service))):
  user = context.user.value

  data_interview = body.dict()
  data_interview["candidate_id"] = candidate_id
  data_interview["employee_code"] = user["employee_code"]

  await interview_schedule_service.add_interview_infor(data_interview)

  return ok()


# Edit interview information
# Param:
#   @interview_schedule_service: Interview schedule service
# Output:
#   return: HTTP response
@candidate_routers.put("/candidates/interview-schedule/{candidate_id:int}", tags=["candidates"], responses={200: {"model": Response[dict]}},
    dependencies=[Depends(authorized_user)])
@inject
async def edit_interview_infor(candidate_id: int, body: EditInterviewInforRequest,
    interview_schedule_service: InterviewScheduleService = Depends(Provide(Container.interview_schedule_service))):
  user = context.user.value

  data_interview = body.dict()
  data_interview["candidate_id"] = candidate_id
  data_interview["employee_code"] = user["employee_code"]

  await interview_schedule_service.edit_interview_infor(data_interview)

  return ok()
