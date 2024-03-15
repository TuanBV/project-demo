"""
Address router
"""

from containers import Container
from fastapi import APIRouter, Depends
from dto.response import AddressResponse, CRMResponse
from core.message import SUCCESS_MESSAGE
from helpers.response import (ok)
from routers.common import SSVRoute
from crm_address.services import AddressService
from dependency_injector.wiring import inject, Provide


router = APIRouter(
    route_class=SSVRoute,
    tags=["addresses"],
    prefix="/api/v1",
    responses={
      401: {
        "model": CRMResponse[dict]
      },
      404: {
        "description": "No data",
        "model": CRMResponse[dict]
      },
      400: {
        "description": "API ERROR",
        "model": CRMResponse[dict]
      },
      500: {
        "description": "SYSTEM ERROR",
        "model": CRMResponse[dict]
      },
    },
  )

# Get address function
# Param:
#   @zipcode: Zipcode
# Output:
#   return: HTTP response
@router.get(
  "/address/{zip_code}", tags=["addresses"],
  responses={
    200: {
      "model": CRMResponse[AddressResponse]
    },
    404: {
      "description": "No data",
      "model": CRMResponse[dict]
    },
    400: {
      "description": "API ERROR",
      "model": CRMResponse[dict]
    },
  },
)
@inject
async def get_address(zip_code: str, address_service: AddressService = Depends(Provide[Container.address_service])):
  address = address_service.get_address(zip_code)
  if not address:
    return ok(SUCCESS_MESSAGE.SUCMSG0019)
  address = AddressResponse(**address)
  return ok(data=address.dict())
