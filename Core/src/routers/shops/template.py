"""
Template router
"""

from containers import Container
from fastapi import APIRouter, Depends
from core import CrmException, CrmNoDataException, ERR_MESSAGE
from crm_template import TemplateService
from decorators import permission
from dependencies import authorized_shop
from dto.request.shop import AddTemplateRequest, EditTemplateRequest
from dto.response import CRMResponse
from dto.response.shop import ListTemplatesResponse, GetTemplatesResponse, AddTemplateResponse
from helpers.const import CODE
from helpers.kbn import UserRole, ACTION_TYPE_NAME
from helpers.response import ok
from helpers import context
from routers.common import SSVRoute
from dependency_injector.wiring import inject, Provide

from utils.service_template import validate_flyer_in_edit, validate_postcard_in_edit

router = APIRouter(
  route_class=SSVRoute,
)


# Get list template of shop
# Param:
#   @search_key: Text of user want to search
#   @limit: Limit item per page
#   @offset: Number of page
#   @sort_key: Column of user want to sort
#   @sort_type: Sort asc or desc
#   @template_type: Type of template
#   @action_type_name: Name action type
#   @template_service: Template service
# Output:
#   return: HTTP response
@router.get("/template", tags=["shop"], responses={200:{"model": CRMResponse[ListTemplatesResponse]}},dependencies=[Depends(authorized_shop)])
@permission([UserRole.SHOP_OWNER, UserRole.SHOP_MANAGER])
@inject
async def get_by_shop(search_key: str = "", limit: int = 20, offset: int = 1, sort_key: str = "", sort_type: str = "",
    template_type: int = 1, action_type_name: str = "", template_service: TemplateService = Depends(Provide[Container.template_service])):
  user = context.user.value
  data = {
    "shop_no": user["user"]["shop_no"],
    "search_key": search_key,
    "limit": limit,
    "offset": offset,
    "sort_key": sort_key,
    "sort_type": sort_type,
    "type": template_type,
    "action_type_name" : action_type_name
  }

  # Get data list template of shop
  payload = template_service.get_list(data)
  payload = ListTemplatesResponse(**payload)
  response = ok(data=payload.dict())
  # Success
  return response


# Add new template
# Param:
#   @body: Data request
#   @template_service: Template service
# Output:
#   return: HTTP response
@router.post("/template", tags=["shop"], responses={200:{"model": CRMResponse[AddTemplateResponse]}},dependencies=[Depends(authorized_shop)])
@permission([UserRole.SHOP_OWNER, UserRole.SHOP_MANAGER])
@inject
async def add(body: AddTemplateRequest, template_service: TemplateService = Depends(Provide[Container.template_service])):
  # Preparing data
  user = context.user.value
  data = {
    "data_template": body.dict(),
    "shop_no": user["user"]["shop_no"],
    "user": user["user"],
  }

  # Add new template
  payload = template_service.add(data)
  payload = AddTemplateResponse(**payload)
  response = ok(data=payload.dict())
  # Success
  return response


# Get data template by Id
# Param:
#   @template_id: Id of template
#   @template_service: Template service
# Output:
#   return: HTTP response
@router.get("/template/{template_id}", tags=["shop"], responses={200:{"model": CRMResponse[GetTemplatesResponse]}},dependencies=[Depends(authorized_shop)])
@permission([UserRole.SHOP_OWNER, UserRole.SHOP_MANAGER])
@inject
async def get_by_id(template_id: int,  template_service: TemplateService = Depends(Provide[Container.template_service])):
  # Preparing data
  user = context.user.value
  data = {
    "shop_no": user["user"]["shop_no"] ,
    "template_id": template_id
  }
  # Get data template by id
  payload = template_service.get(data)
  payload = GetTemplatesResponse(**payload)
  response = ok(data=payload.dict())
  # Success
  return response


# Delete template
# Param:
#   @template_id: Id of template
#   @template_service: Template service
# Output:
#   return: HTTP response
@router.delete("/template/{template_id}", tags=["shop"], responses={200:{"model": CRMResponse[dict]}},dependencies=[Depends(authorized_shop)])
@permission([UserRole.SHOP_OWNER, UserRole.SHOP_MANAGER])
@inject
async def delete(template_id: int, template_service: TemplateService = Depends(Provide[Container.template_service])):
  # Preparing data
  user = context.user.value
  data = {
    "shop_no": user["user"]["shop_no"],
    "template_id": template_id,
    "user": user["user"]
  }

  # Delete template
  template_service.delete(data)
  return ok()


# Update data template
# Param:
#   @body: Data request
#   @template_id: Id template
#   @template_service: Template service
# Output:
#   return: HTTP response
@router.put("/template/{template_id}", tags=["shop"], responses={200:{"model": CRMResponse[dict]}},dependencies=[Depends(authorized_shop)])
@permission([UserRole.SHOP_OWNER, UserRole.SHOP_MANAGER])
@inject
async def edit(body: EditTemplateRequest, template_id: int,  template_service: TemplateService = Depends(Provide[Container.template_service])):
  # Preparing data
  user = context.user.value
  # Get data old template
  # Excute query
  data_get_template = {
    "shop_no": user["user"]["shop_no"] ,
    "template_id": template_id
  }
  result_template = template_service.get(data_get_template)
  # Validation
  valid = []
  # Template type is Post card
  if result_template["action_type"]["name"] == ACTION_TYPE_NAME.POST_CARD:
    # Validate data
    body.pdf_post_card = body.pdf_post_card.strip()
    body.pdf_post_card_size = body.pdf_post_card_size.strip()
    body.pdf_post_card_type = body.pdf_post_card_type.strip()
    valid = validate_postcard_in_edit(body, result_template)

  # Template type is Flyer
  elif result_template["action_type"]["name"] == ACTION_TYPE_NAME.FLYER:
    # Validate data
    body.pdf_flyer_text = body.pdf_flyer_text.strip()
    body.pdf_flyer_text_size = body.pdf_flyer_text_size.strip()
    body.pdf_flyer_text_type = body.pdf_flyer_text_type.strip()
    body.pdf_flyer_address = body.pdf_flyer_address.strip()
    body.pdf_flyer_address_size = body.pdf_flyer_address_size.strip()
    body.pdf_flyer_address_type = body.pdf_flyer_address_type.strip()
    valid = validate_flyer_in_edit(body, result_template)

  # Check error validate exist
  if valid:
    raise CrmException(CODE.API.ERROR, valid)

  # Check old template is not exists
  if not result_template["template"]:
    return CrmNoDataException(message = ERR_MESSAGE.ERRMSG0163)

  # Update data template
  data = {
    "shop_no": user["user"]["shop_no"],
    "template_id": template_id,
    "data_template": body.dict(),
    "user": user["user"]
  }

  template_service.update(data)

  return ok()
