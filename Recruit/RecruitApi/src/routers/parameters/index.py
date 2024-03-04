
"""
Parameters router
"""

from fastapi import APIRouter, Depends
from containers import Container
from dto.response import Response
from dto.response.parameters import ParameterResponse, ListParameterResponse, ItemParameter
from dto.request.parameters import ParameterAddRequest, ParameterEditRequest
from helpers.response import (ok)
from helpers.kbn import ROLE
from dependency_injector.wiring import inject, Provide
from dependencies import authorized_user
from recruit_parameters.services import ParametersService
from routers.common import SSVRoute
from decorators import permission

parameter_routers = APIRouter(route_class=SSVRoute, tags=["parameters"], prefix="/api/v1/parameters",
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


# List parameter
# Param:
#   @parameters_service: Parameters service
# Output:
#   return: HTTP response
@parameter_routers.get("", tags=["parameters"], responses={200: {"model": Response[ListParameterResponse]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def get_list(parameters_service: ParametersService = Depends(Provide(Container.parameters_service))):
  # Get list parameter
  data_parameter = parameters_service.get_list()
  payload = ListParameterResponse(**data_parameter)
  response = ok(data=payload.dict())

  return response


# Get info of param
# Param:
#   @parameters_service: Parameters service
# Output:
#   return: HTTP response
@parameter_routers.get("/{id_param}", tags=["parameters"], responses={200: {"model": Response[ParameterResponse]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def get_by_id(id_param: str, parameters_service: ParametersService = Depends(Provide(Container.parameters_service))):
  # Get info of parameter
  parameter = parameters_service.get_by_id(id_param)
  payload = ParameterResponse(**parameter)
  response = ok(data=payload.dict())

  return response


# Add parameter new
# Param:
#   @parameters_service: Parameters service
# Output:
#   return: HTTP response
@parameter_routers.post("", tags=["parameters"], responses={200: {"model": Response[ItemParameter]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def add(body: ParameterAddRequest, parameters_service: ParametersService = Depends(Provide(Container.parameters_service))):
  # Get info of parameter
  param = parameters_service.add(body)

  payload = ParameterResponse(**param)
  response = ok(data=payload.dict())

  return response


# Update parameter
# Param:
#   @body: Data request
#   @parameters_service: Parameters service
# Output:
#   return: HTTP response
@parameter_routers.put("/{id_param}", tags=["parameters"], responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def edit(id_param: str, body: ParameterEditRequest, parameters_service: ParametersService = Depends(Provide(Container.parameters_service))):
  # Update info of parameter
  parameters_service.edit(id_param, body)

  return ok()


# Delete parameter
# Param:
#   @parameters_service: Parameters service
# Output:
#   return: HTTP response
@parameter_routers.delete("/{id_param}", tags=["parameters"], responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def delete(id_param: str, parameters_service: ParametersService = Depends(Provide(Container.parameters_service))):
  # Update info of parameter
  parameters_service.delete(id_param)

  return ok()
