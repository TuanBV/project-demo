"""
Mails router
"""
from fastapi import APIRouter, Depends
from containers import Container
from dto.response.common import Response
from dto.request.mails import MailEditRequest
from dto.response.mails import EditMailResponse
from routers.common import SSVRoute
from dependency_injector.wiring import inject, Provide
from recruit_mails import MailService
from helpers.response import (ok)
from helpers.kbn import ROLE
from dependencies import authorized_user
from decorators import permission

mail_routers = APIRouter(route_class=SSVRoute, tags=["team"], prefix="/api/v1/mails",
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


# Update mail
# Param:
#   @teams_service: Teams service
# Output:
#   return: HTTP response
@mail_routers.put("/{mail_id:int}", tags=["mail"], responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def update_mail(mail_id: int, body: MailEditRequest, mails_service: MailService = Depends(Provide(Container.mails_service))):
  mail = mails_service.update(mail_id, body.__dict__)
  payload = EditMailResponse(**mail)
  return ok(data=payload.dict())
