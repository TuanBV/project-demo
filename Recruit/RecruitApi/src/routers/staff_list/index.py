"""
Candidate router
"""
from fastapi import APIRouter, Depends
from containers import Container
from dto.response.common import Response
from dto.response.candidates import CandidatesListResponse
from routers.common import SSVRoute
from dependency_injector.wiring import inject, Provide
from recruit_staff_list import StaffListService
from helpers.response import (ok)
from helpers.kbn import ROLE
from dependencies import authorized_user
from decorators import permission

staff_routers = APIRouter(route_class=SSVRoute, tags=["staff"], prefix="/api/v1/staff",
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


# Get list staff
# Param:
#   @staff_list_service: Staff list service
# Output:
#   return: HTTP response
@staff_routers.get("", tags=["staff"], responses={200: {"model": Response[CandidatesListResponse]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def get_list(staff_list_service: StaffListService = Depends(Provide(Container.staff_list_service))):
  result_list_candidates = staff_list_service.get_list()

  payload = CandidatesListResponse(**result_list_candidates)

  response = ok(data=payload.dict())

  return response

# Delete staff
# Param:
#   @staff_list_service: Staff list service
# Output:
#   return: HTTP response
@staff_routers.delete("/{id_candidate}", tags=["staff"], responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def delete(id_candidate: int, staff_list_service: StaffListService = Depends(Provide(Container.staff_list_service))):
  # Delete staff
  staff_list_service.delete(id_candidate)

  return ok()

