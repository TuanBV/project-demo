"""
Candidate router
"""
from fastapi import APIRouter, Depends
from containers import Container
from dto.response.common import Response
from dto.response.candidates import CandidatesConfirmListResponse, CandidateConfirmResponse
from routers.common import SSVRoute
from dependency_injector.wiring import inject, Provide
from recruit_candidates_confirm import CandidatesConfirmService
from helpers.response import (ok)
from helpers.kbn import ROLE
from dependencies import authorized_user
from core import CommonException, ERR_MESSAGE
from decorators import permission

candidate_confirm_routers = APIRouter(route_class=SSVRoute, tags=["candidates_confirm"], prefix="/api/v1/candidates_confirm",
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


# Get list confirm candidates
# Param:
#   @candidates_confirm_service: Confirm candidate service
# Output:
#   return: HTTP response
@candidate_confirm_routers.get("", tags=["candidates_confirm"],
  responses={200: {"model": Response[CandidatesConfirmListResponse]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def get_list(candidates_confirm_service: CandidatesConfirmService = Depends(Provide(Container.candidates_confirm_service))):
  result_list = candidates_confirm_service.get_list()

  payload = CandidatesConfirmListResponse(**result_list)
  response = ok(data=payload.dict())

  return response


# Get confirm candidate
# Params:
#   @candidates_confirm_service: Confirm candidate service
# Output:
#   return: HTTP response
@candidate_confirm_routers.get("/{candidate_id}", tags=["candidates_confirm"],
    responses={200: {"model": Response[CandidateConfirmResponse]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def get_by_id(candidate_id: int, candidates_confirm_service: CandidatesConfirmService = Depends(Provide(Container.candidates_confirm_service))):
  # Don't have candidate id will raise error
  if not candidate_id:
    raise CommonException(message = ERR_MESSAGE.MISSING_CANDIDATE_ID)

  result = candidates_confirm_service.get_by_id(candidate_id)

  payload = CandidateConfirmResponse(**result)

  response = ok(data=payload.dict())

  return response


# Edit candidate
# Params:
#   @candidates_confirm_service: Confirm candidate service
# Output:
#   return: HTTP response
@candidate_confirm_routers.put("/{candidate_id}", tags=["candidates_confirm"], responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def edit(candidate_id: int, candidates_confirm_service: CandidatesConfirmService = Depends(Provide(Container.candidates_confirm_service))):
  # Don't have candidate id will raise error
  if not candidate_id:
    raise CommonException(message = ERR_MESSAGE.MISSING_CANDIDATE_ID)

  candidates_confirm_service.edit(candidate_id)

  return ok()
