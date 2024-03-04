
"""
Meeting rooms router
"""

from fastapi import APIRouter, Depends
from containers import Container
from dto.response import Response
from dto.response.meeting_rooms import ListMeetingRoomsResponse
from helpers.response import ok
from helpers.kbn import ROLE
from dependency_injector.wiring import inject, Provide
from recruit_meeting_rooms import MeetingRoomsService
from routers.common import SSVRoute
from dependencies import authorized_user
from decorators import permission

meeting_room_routers = APIRouter(route_class=SSVRoute, tags=["meeting_room"], prefix="/api/v1",
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
#   @meeting_rooms_service: office service
# Output:
#   return: HTTP response
@meeting_room_routers.get("/meeting-rooms", tags=["meeting_rooms"], responses={200: {"model": Response[ListMeetingRoomsResponse]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def get_list_meeting_room(meeting_rooms_service: MeetingRoomsService = Depends(Provide(Container.meeting_rooms_service))):
  # Get list office
  data_rooms = meeting_rooms_service.get_list()
  payload = ListMeetingRoomsResponse(**data_rooms)
  response = ok(data=payload.dict())

  return response
