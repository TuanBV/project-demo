"""
Positions router
"""
from fastapi import APIRouter, Depends
from containers import Container
from dto.response.common import Response
from dto.response.positions import ListPositionsReponse
from routers.common import SSVRoute
from dependency_injector.wiring import inject, Provide
from recruit_positions import PositionsService
from helpers.response import (ok)
from dependencies import authorized_user

position_routers = APIRouter(route_class=SSVRoute, tags=["position"], prefix="/api/v1",
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


# Get list positions
# Param:
#   @positions_service: Positions service
# Output:
#   return: HTTP response
@position_routers.get("/positions", tags=["position"], responses={200: {"model": Response[ListPositionsReponse]}}, dependencies=[Depends(authorized_user)])
@inject
async def get_list(positions_service: PositionsService = Depends(Provide(Container.positions_service))):
  result_list_positions = positions_service.get_list()

  payload = ListPositionsReponse(**result_list_positions)
  response = ok(data=payload.dict())

  return response
