"""
Service owner router
"""
from fastapi import APIRouter, Depends
from containers import Container
# from crm_print.services import PrintService
from decorators import permission
from dto.request.admin.edit_print import EditPrintStatusRequest
from dto.response import CRMResponse
from dto.response.admin import (ExportPrintCsvResponse, ExportPrintPdfResponse, GetActionDetailPrintResponse, ListActionDetailsResponse)
from core.message import ERR_MESSAGE
from core.error import CommonException
from helpers.kbn import UserRole
from helpers import context
from helpers.response import (ok)
from routers.common import SSVRoute
from dependencies import authorized_admin
from dependency_injector.wiring import inject, Provide


print_routers = APIRouter(
  route_class=SSVRoute,
)


# # Get list action details function
# # Param:
# #   @search_key: Text of user want to search
# #   @limit: Limit item per page
# #   @offset: Number of page
# #   @sort_key: Column of user want to sort
# #   @sort_type: Sort asc or desc
# #   @extended_search: Search condition
# #   @print_service: Print service
# # Output:
# #   return: HTTP response
# @print_routers.get("/print/list", tags=["print"], responses={200:{"model": CRMResponse[ListActionDetailsResponse]}},dependencies=[Depends(authorized_admin)])
# @permission([UserRole.ADMIN])
# @inject
# async def get_list(search_key: str = "", limit: int = 20, offset: int = 1, sort_key: str = "", sort_type: str = "",
#     extended_search: str = "", print_service: PrintService = Depends(Provide[Container.print_service])):

#   # Set data for function in service
#   data = {
#     "search_key": search_key,
#     "limit": limit,
#     "offset": offset,
#     "sort_key": sort_key,
#     "sort_type": sort_type,
#     "extended_search": extended_search
#   }

#   # Call function
#   payload = print_service.get_list(data)

#   payload = ListActionDetailsResponse(**payload)

#   # Success
#   return ok(data=payload.dict())


# # Export csv in list print
# # Params:
# #   @search_key: Text of user want to search
# #   @limit: Limit item per page
# #   @offset: Number of page
# #   @sort_key: Column of user want to sort
# #   @sort_type: Sort asc or desc
# #   @extended_search: Search condition
# #   @print_service: Print service
# # Output:
# #   return: HTTP response
# @print_routers.get("/print/list-print-csv", tags=["print"], responses={200:{"model": CRMResponse[ExportPrintCsvResponse]}}, dependencies=[Depends(authorized_admin)])
# @permission([UserRole.ADMIN])
# @inject
# async def export_print_csv(search_key: str = "", limit: int = 20, offset: int = 1, sort_key: str = "", sort_type: str = "", extended_search: str = "",
#     print_service: PrintService = Depends(Provide[Container.print_service])):

#   data = {
#     "search_key": search_key,
#     "extended_search": extended_search,
#     "limit": limit,
#     "offset": offset,
#     "sort_key": sort_key,
#     "sort_type": sort_type,
#   }

#   payload = print_service.export_print_csv(data)

#   payload = ExportPrintCsvResponse(**payload)

#   return ok(data=payload.dict())


# # Export pdf in list print
# # Params:
# #   @search_key: Text of user want to search
# #   @limit: Limit item per page
# #   @offset: Number of page
# #   @sort_key: Column of user want to sort
# #   @sort_type: Sort asc or desc
# #   @extended_search: Search condition
# #   @print_service: Print service
# # Output:
# #   return: HTTP response
# @print_routers.get("/print/list-print-pdf", tags=["print"], responses={200:{"model": CRMResponse[ExportPrintPdfResponse]}}, dependencies=[Depends(authorized_admin)])
# @permission([UserRole.ADMIN])
# @inject
# async def export_print_pdf(search_key: str = "", limit: int = 20, offset: int = 1, sort_key: str = "", sort_type: str = "", extended_search: str = "",
#     print_service: PrintService = Depends(Provide[Container.print_service])):
#   user = context.user.value

#   data = {
#     "search_key": search_key,
#     "extended_search": extended_search,
#     "limit": limit,
#     "offset": offset,
#     "sort_key": sort_key,
#     "sort_type": sort_type,
#     "user": user["user"]["id"]
#   }

#   payload = print_service.export_print_pdf(data)
#   payload = ExportPrintPdfResponse(**payload)

#   return ok(data=payload.dict())


# # Get data action detail
# # Params:
# #   @action_detail_id: Action detail id
# #   @print_service: Print service
# # Output:
# #   return: HTTP response
# @print_routers.get("/print/detail-print/{action_detail_id}", tags=["print"], responses={200:{"model": CRMResponse[GetActionDetailPrintResponse]}},
#     dependencies=[Depends(authorized_admin)])
# @permission([UserRole.ADMIN])
# @inject
# async def get_detail_print(action_detail_id: int, print_service: PrintService = Depends(Provide[Container.print_service])):

#   # Don't have action detail id will raise error
#   if not action_detail_id:
#     raise CrmException(message = ERR_MESSAGE.ERRMSG0017)

#   payload = print_service.get_detail_print(action_detail_id)
#   payload = GetActionDetailPrintResponse(**payload)

#   return ok(data=payload.dict())


# # Edit action detail print status
# # Params:
# #   @action_detail_id: Action detail id
# #   @print_service: Print service
# # Output:
# #   return: HTTP response
# @print_routers.put("/print/detail-print/{action_detail_id}", tags=["print"], responses={200:{"model": CRMResponse[dict]}},
#     dependencies=[Depends(authorized_admin)])
# @permission([UserRole.ADMIN])
# @inject
# async def update_print_status(action_detail_id: int, body: EditPrintStatusRequest, print_service: PrintService = Depends(Provide[Container.print_service])):
#   user = context.user.value

#   # Don't have action detail id will raise error
#   if not action_detail_id:
#     raise CrmException(message = ERR_MESSAGE.ERRMSG0017)

#   data = {
#     "user": user["user"]["id"],
#     "action_detail_id": action_detail_id,
#     "body": body.dict()
#   }

#   print_service.update_print_status(data)

#   return ok()


# # Export pdf backside action detail
# # Params:
# #   @action_detail_id: Action detail id
# #   @print_service: Print service
# # Output:
# #   return: HTTP response
# @print_routers.get("/print/detail-print/{action_detail_id}/customer-pdf", tags=["print"], responses={200:{"model": CRMResponse[ExportPrintPdfResponse]}},
#     dependencies=[Depends(authorized_admin)])
# @permission([UserRole.ADMIN])
# @inject
# async def export_pdf_backside(action_detail_id: int, print_service: PrintService = Depends(Provide[Container.print_service])):
#   user = context.user.value

#   # Don't have action detail id will raise error
#   if not action_detail_id:
#     raise CrmException(message = ERR_MESSAGE.ERRMSG0017)

#   data = {
#     "user": user["user"]["id"],
#     "action_detail_id": action_detail_id,
#   }

#   payload = print_service.export_pdf_backside(data)

#   payload = ExportPrintPdfResponse(**payload)

#   return ok(data=payload.dict())


# # Export csv customer in detail print function
# # Params:
# #   @action_detail_id: Action detail id
# #   @print_service: Print service
# # Output:
# #   return: HTTP response
# @print_routers.get("/print/detail-print/{action_detail_id}/customer-csv", tags=["print"], responses={200:{"model": CRMResponse[ExportPrintCsvResponse]}},
#     dependencies=[Depends(authorized_admin)])
# @permission([UserRole.ADMIN])
# @inject
# async def export_csv_customer(action_detail_id: int, print_service: PrintService = Depends(Provide[Container.print_service])):
#   # Don't have action detail id will raise error
#   if not action_detail_id:
#     raise CrmException(message = ERR_MESSAGE.ERRMSG0017)

#   payload = print_service.export_csv_customer(action_detail_id)

#   payload = ExportPrintCsvResponse(**payload)

#   return ok(data=payload.dict())
