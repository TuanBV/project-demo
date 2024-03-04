"""
Teams router
"""
from fastapi import APIRouter, Depends
from containers import Container
from dto.response.common import Response
from dto.response.teams import ListTeamsResponse
from routers.common import SSVRoute
from dependency_injector.wiring import inject, Provide
from recruit_teams import TeamsService
from helpers.response import (ok)
from dependencies import authorized_user

team_routers = APIRouter(route_class=SSVRoute, tags=["team"], prefix="/api/v1",
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


# Get list teams
# Param:
#   @teams_service: Teams service
# Output:
#   return: HTTP response
@team_routers.get("/teams", tags=["team"], responses={200: {"model": Response[ListTeamsResponse]}}, dependencies=[Depends(authorized_user)])
@inject
async def get_list(teams_service: TeamsService = Depends(Provide(Container.teams_service))):
  result_list_teams = teams_service.get_list()

  payload = ListTeamsResponse(**result_list_teams)
  response = ok(data=payload.dict())

  return response
