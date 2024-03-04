
"""
Offices router
"""

from fastapi import APIRouter, Depends
from containers import Container
from dto.response import Response
from dto.request.offices import EditMailOfficesRequest
from dto.response.offices import ListOfficeResponse, ListMailOfficeResponse
from helpers.response import ok
from helpers.kbn import ROLE
from dependency_injector.wiring import inject, Provide
from recruit_offices import OfficesService
from routers.common import SSVRoute
from dependencies import authorized_user
from decorators import permission

offices_routers = APIRouter(route_class=SSVRoute, tags=["office"], prefix="/api/v1/offices",
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


# Get list office
# Param:
#   @offices_service: office service
# Output:
#   return: HTTP response
@offices_routers.get("", tags=["office"], responses={200: {"model": Response[ListOfficeResponse]}}, dependencies=[Depends(authorized_user)])
@inject
async def get_list_office(offices_service: OfficesService = Depends(Provide(Container.offices_service))):
  # Get list office
  data_office = offices_service.get_list()
  payload = ListOfficeResponse(**data_office)
  response = ok(data=payload.dict())

  return response


# Get mail offices
# Param:
#   @offices_service: office service
# Output:
#   return: HTTP response
@offices_routers.get("/mail", tags=["office"], responses={200: {"model": Response[ListMailOfficeResponse]}},
                     dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def get_mail_offices(offices_service: OfficesService = Depends(Provide(Container.offices_service))):
  # Get mail offices
  mail_offices = offices_service.get_mail_offices()
  payload = ListMailOfficeResponse(**mail_offices)
  response = ok(data=payload.dict())

  return response


# Get mail offices
# Param:
#   @offices_service: office service
# Output:
#   return: HTTP response
@offices_routers.put("/mail", tags=["office"], responses={200: {"model": Response[dict]}},
                     dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def edit_mail_offices(body: EditMailOfficesRequest,
                            offices_service: OfficesService = Depends(Provide(Container.offices_service))):
  offices_service.edit_mail_offices(body.dict())
  return ok()
