"""
Candidate router
"""
from fastapi import APIRouter, Depends
from containers import Container
from dto.response.common import Response
from dto.response.candidates import CandidatesListResponse, CandidateViewResponse
from routers.common import SSVRoute
from dependency_injector.wiring import inject, Provide
from recruit_black_list import BlackListService
from helpers.response import (ok)
from helpers.kbn import ROLE
from dependencies import authorized_user
from decorators import permission

black_list_routers = APIRouter(route_class=SSVRoute, tags=["black_list"], prefix="/api/v1/black_list",
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


# Get black list candidate
# Param:
#   @black_list_service: Black list service
# Output:
#   return: HTTP response
@black_list_routers.get("", tags=["candidates_list"], responses={200: {"model": Response[CandidatesListResponse]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def get_list(black_list_service: BlackListService = Depends(Provide(Container.black_list_service))):
  result_list_candidates = black_list_service.get_list()

  payload = CandidatesListResponse(**result_list_candidates)

  response = ok(data=payload.dict())

  return response


# Get info candidates
# Param:
#   @black_list_service: Black list service
# Output:
#   return: HTTP response
@black_list_routers.get("/{id_candidate}", tags=["candidates_list"], responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def get_by_id(id_candidate: str, black_list_service: BlackListService = Depends(Provide(Container.black_list_service))):
  result_candidates = black_list_service.get_by_id(id_candidate)

  payload = CandidateViewResponse(**result_candidates)

  response = ok(data=payload.dict())

  return response
