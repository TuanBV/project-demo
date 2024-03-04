"""
Recommen
"""
from fastapi import APIRouter, Depends
from containers import Container
from dto.response.common import Response
from dto.request.recommenders import AddRecommenderRequest, EditRecommenderRequest
from dto.response.recommenders import ListRecommendersResponse, RecommenderItemResponse
from routers.common import SSVRoute
from dependency_injector.wiring import inject, Provide
from recruit_recommenders import RecommendersService
from helpers.response import (ok)
from helpers import context
from helpers.kbn import ROLE
from dependencies import authorized_user
from core import CommonException, ERR_MESSAGE
from decorators import permission

recommender_routers = APIRouter(route_class=SSVRoute, tags=["recommender"], prefix="/api/v1",
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


# Get list recommenders
# Param:
#   @recommenders_service: Recommenders service
# Output:
#   return: HTTP response
@recommender_routers.get("/recommenders", tags=["recommender"], responses={200: {"model": Response[ListRecommendersResponse]}}, dependencies=[Depends(authorized_user)])
@inject
async def get_list(recommenders_service: RecommendersService = Depends(Provide(Container.recommenders_service))):
  result_list_recommenders = recommenders_service.get_list()

  payload = ListRecommendersResponse(**result_list_recommenders)
  response = ok(data=payload.dict())

  return response


# Add recommenders
# Param:
#   @body: Data request
#   @recommenders_service: Recommenders service
# Output:
#   return: HTTP response
@recommender_routers.post(
  "/recommenders", tags=["recommender"],
  responses={200: {"model": Response[RecommenderItemResponse]}},
  dependencies=[Depends(authorized_user)]
)
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def add(body: AddRecommenderRequest, recommenders_service: RecommendersService = Depends(Provide(Container.recommenders_service))):
  user = context.user.value

  data = {
    "recommender": body.dict(),
    "employee_code": user["employee_code"]
  }

  recommender = recommenders_service.add(data)
  payload = RecommenderItemResponse(**recommender)

  return ok(data=payload.dict())


# Get recommender
# Params:
#   @recommenders_service: Recommenders service
# Output:
#   return: HTTP response
@recommender_routers.get(
  "/recommenders/{recommender_id}", tags=["recommender"],
  responses={200: {"model": Response[RecommenderItemResponse]}},
  dependencies=[Depends(authorized_user)]
)
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def get_recommender(recommender_id: int, recommenders_service: RecommendersService = Depends(Provide(Container.recommenders_service))):
  # Don't have recommender id will raise error
  if not recommender_id:
    raise CommonException(message = ERR_MESSAGE.MISSING_RECOMMENDER_ID)

  result_recommender = recommenders_service.get_recommender(recommender_id)

  payload = RecommenderItemResponse(**result_recommender)

  response = ok(data=payload.dict())

  return response


# Edit recommender
# Params:
#   @recommenders_service: Recommenders service
#   @body: Data request
# Output:
#   return: HTTP response
@recommender_routers.put("/recommenders/{recommender_id}", tags=["recommender"], responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def edit(recommender_id: int, body: EditRecommenderRequest, recommenders_service: RecommendersService = Depends(Provide(Container.recommenders_service))):
  # Don't have recommender id will raise error
  if not recommender_id:
    raise CommonException(message = ERR_MESSAGE.MISSING_RECOMMENDER_ID)

  user = context.user.value

  data = {
    "recommender": body.dict(),
    "recommender_id": recommender_id,
    "employee_code": user["employee_code"]
  }

  recommenders_service.edit(data)

  return ok()


# Delete recommender
# Params:
#   @recommenders_service: Recommenders service
#   @body: Data request
# Output:
#   return: HTTP response
@recommender_routers.delete("/recommenders/{recommender_id}", tags=["recommender"], responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def delete(recommender_id: int, recommenders_service: RecommendersService = Depends(Provide(Container.recommenders_service))):
  # Don't have recommender id will raise error
  if not recommender_id:
    raise CommonException(message = ERR_MESSAGE.MISSING_RECOMMENDER_ID)

  user = context.user.value

  data = {
    "recommender_id": recommender_id,
    "employee_code": user["employee_code"]
  }

  recommenders_service.delete(data)

  return ok()
