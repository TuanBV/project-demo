
"""
Templates router
"""

from fastapi import APIRouter, Depends
from containers import Container
from dto.response import Response
from dto.response.templates import ListTemplateResponse, TemplateResponse
from dto.request.templates import TemplateEditRequest
from helpers.response import (ok)
from helpers.kbn import ROLE
from dependencies import authorized_user
from decorators import permission
from dependency_injector.wiring import inject, Provide
from recruit_templates.services import TemplatesService
from routers.common import SSVRoute

template_routers = APIRouter(route_class=SSVRoute, tags=["templates"], prefix="/api/v1/templates",
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

# List template mail
# Param:
#   @templates_service: Templates service
# Output:
#   return: HTTP response
@template_routers.get("", tags=["templates"], responses={200: {"model": Response[ListTemplateResponse]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def get_list(templates_service: TemplatesService = Depends(Provide(Container.templates_service))):
  # Get list templates
  data_templates = templates_service.get_list()
  payload = ListTemplateResponse(**data_templates)
  response = ok(data=payload.dict())

  return response


# Get info of template
# Param:
#   @templates_service: Template service
#   @id_template: id of template
# Output:
#   return: HTTP response
@template_routers.get("/{id_template}", tags=["templates"], responses={200: {"model": Response[TemplateResponse]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def get(id_template: str, templates_service: TemplatesService = Depends(Provide(Container.templates_service))):
  # Get info of one user
  data_template = templates_service.get_by_id(id_template)
  payload = TemplateResponse(**data_template)
  response = ok(data=payload.dict())

  return response


# Update template mail
# Param:
#   @body: Data request
#   @id_template: id of template
#   @templates_service: Template service
# Output:
#   return: HTTP response
@template_routers.put("/{id_template}", tags=["templates"], responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def edit(id_template: str, body: TemplateEditRequest, templates_service: TemplatesService = Depends(Provide(Container.templates_service))):
  # Update info of templates
  templates_service.edit(id_template, body)

  return ok()
