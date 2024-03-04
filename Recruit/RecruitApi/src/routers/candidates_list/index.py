"""
Candidate router
"""
from fastapi import APIRouter, Depends
from containers import Container
from dto.response.common import Response
from dto.request.candidates import EditCandidateListRequest, CandidateBlackListRequest
from dto.response.candidates import CandidatesListResponse, CandidateViewResponse
from routers.common import SSVRoute
from dependency_injector.wiring import inject, Provide
from recruit_candidates_list import CandidatesListService
from helpers.response import (ok)
from helpers.kbn import ROLE
from dependencies import authorized_user
from decorators import permission

candidates_routers = APIRouter(route_class=SSVRoute, tags=["candidates"], prefix="/api/v1/candidates",
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
#   @candidates_list_service: Candidates list service
# Output:
#   return: HTTP response
@candidates_routers.get("", tags=["candidates"], responses={200: {"model": Response[CandidatesListResponse]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def get_list(candidates_list_service: CandidatesListService = Depends(Provide(Container.candidates_list_service))):
  result_list_candidates = candidates_list_service.get_list()

  payload = CandidatesListResponse(**result_list_candidates)

  response = ok(data=payload.dict())

  return response


# Get info candidates
# Param:
#   @candidates_list_service: Candidates list service
# Output:
#   return: HTTP response
@candidates_routers.get("/{id_candidate}", tags=["candidates"], responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def get_by_id(id_candidate: str, candidates_list_service: CandidatesListService = Depends(Provide(Container.candidates_list_service))):
  result_candidates = candidates_list_service.get_by_id(id_candidate)

  payload = CandidateViewResponse(**result_candidates)

  response = ok(data=payload.dict())

  return response


# Edit candidates
# Param:
#   @candidates_list_service: Candidates list service
# Output:
#   return: HTTP response
@candidates_routers.put("/{id_candidate}", tags=["candidates_list"], responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def edit(id_candidate: str, body: EditCandidateListRequest, candidates_list_service: CandidatesListService = Depends(Provide(Container.candidates_list_service))):
  candidates_list_service.edit(id_candidate, body.dict())

  return ok()

# Move candidate to black list
# Param:
#   @candidates_list_service: Candidates list service
# Output:
#   return: HTTP response
@candidates_routers.delete("/{id_candidate}", tags=["candidates_list"], responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def delete(id_candidate: str, body: CandidateBlackListRequest, candidates_list_service: CandidatesListService = Depends(Provide(Container.candidates_list_service))):
  candidates_list_service.delete(id_candidate, body.dict())

  return ok()
