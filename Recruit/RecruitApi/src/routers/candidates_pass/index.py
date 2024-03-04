"""
Candidate router
"""
from fastapi import APIRouter, Depends
from containers import Container
from dto.response.common import Response
from dto.request.candidates import MailCandidate, EditMailCandidate
from dto.response.candidates import CandidatesPassListResponse, AddMailCandidatesResponse, EditMailCandidatesResponse
from routers.common import SSVRoute
from dependency_injector.wiring import inject, Provide
from recruit_candidates_pass_list import CandidatesPassListService
from helpers.response import (ok)
from helpers.kbn import ROLE
from dependencies import authorized_user
from decorators import permission

candidate_pass_list_routers = APIRouter(route_class=SSVRoute, tags=["candidates_pass_list"], prefix="/api/v1/candidates_pass_list",
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


# Get list candidates
# Param:
#   @candidates_pass_list_service: Candidates pass list service
# Output:
#   return: HTTP response
@candidate_pass_list_routers.get("", tags=["candidates_pass_list"], responses={200: {"model": Response[CandidatesPassListResponse]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def get_list(candidates_pass_list_service: CandidatesPassListService = Depends(Provide(Container.candidates_pass_list_service))):
  result = candidates_pass_list_service.get_list()

  payload = CandidatesPassListResponse(**result)

  response = ok(data=payload.dict())

  return response


# Add mail candidate
# Param:
#   @candidates_pass_list_service: Candidates pass list service
# Output:
#   return: HTTP response
@candidate_pass_list_routers.post("", tags=["candidates_pass_list"], responses={200: {"model": Response[CandidatesPassListResponse]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def add_mail(body: MailCandidate, candidates_pass_list_service: CandidatesPassListService = Depends(Provide(Container.candidates_pass_list_service))):
  result = candidates_pass_list_service.add_mail(body.list_id_candidate)

  payload = AddMailCandidatesResponse(**result)

  response = ok(data=payload.dict())

  return response


# Edit mail candidate
# Param:
#   @candidates_pass_list_service: Candidates pass list service
# Output:
#   return: HTTP response
@candidate_pass_list_routers.put("", tags=["candidates_pass_list"], responses={200: {"model": Response[CandidatesPassListResponse]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def edit_mail(body: EditMailCandidate, candidates_pass_list_service: CandidatesPassListService = Depends(Provide(Container.candidates_pass_list_service))):
  result = candidates_pass_list_service.edit_mail(body)

  payload = EditMailCandidatesResponse(**result)

  response = ok(data=payload.dict())

  return response


# Send mail candidate
# Param:
#   @candidates_pass_list_service: Candidates pass list service
# Output:
#   return: HTTP response
@candidate_pass_list_routers.put("/send-mail", tags=["candidates_pass_list"], responses={200: {"model": Response[CandidatesPassListResponse]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def send_mail(body: MailCandidate, candidates_pass_list_service: CandidatesPassListService = Depends(Provide(Container.candidates_pass_list_service))):
  await candidates_pass_list_service.send_mail(body.list_id_candidate)

  return ok()
