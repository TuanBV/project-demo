
"""
Users router
"""

from fastapi import APIRouter, Depends
from containers import Container
from dto.response import Response
from dto.request.users import UsersLoginRequest, UserRegisterRequest, UserEditRequest, \
  ForgotPasswordRequest, ChangePasswordRequest, ResetPasswordRequest
from dto.response.users import UsersLoginResponse, ListUserResponse, UserResponse, ListLeaderResponse, CountRecordResponse
from helpers.cookie import get_user_cookie
from helpers.response import (ok, make_cookie)
from helpers import context
from helpers.kbn import ROLE
from dependencies import authorized_user
from dependency_injector.wiring import inject, Provide
from recruit_users import UsersService
from routers.common import SSVRoute
from decorators import permission

user_routers = APIRouter(route_class=SSVRoute, tags=["user"], prefix="/api/v1/users",
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

# User Login
# Param:
#   @body: Data request
#   @users_service: User service
# Output:
#   return: HTTP response
@user_routers.post("/login", tags=["user"], responses={200: {"model": Response[UsersLoginResponse]}})
@inject
async def login_users(body: UsersLoginRequest, users_service: UsersService = Depends(Provide(Container.users_service))):
  # parse data json on body event
  opt = body.dict()
  result_login = users_service.login(opt)

  cookie_config = make_cookie(get_user_cookie(), result_login["token"])

  payload = UsersLoginResponse(**result_login["user"])
  response = ok(data=payload.dict())

  # Set cookie
  response.set_cookie(**cookie_config)

  return response


# Logout
# Output:
#   return: HTTP response
@user_routers.post("/logout", tags=["user"], dependencies=[Depends(authorized_user)])
async def logout():
  context.user.reset()
  response = ok()

  cookie_config = make_cookie(get_user_cookie(), max_age=0)
  # Set cookie
  response.set_cookie(**cookie_config)

  return response


# Check data admin function
# Param:
#   @users_service: User service
# Output:
#   return: HTTP response
@user_routers.get("/me", tags=["user"], responses={200:{"model": Response[UsersLoginResponse]}}, dependencies=[Depends(authorized_user)])
@inject
def get_me(users_service: UsersService = Depends(Provide(Container.users_service))):
  # remake token
  data_user = users_service.get_user_me()

  # Set cookie
  cookie_config = make_cookie(get_user_cookie(), data_user["token"])

  payload = UsersLoginResponse(**data_user["user"])
  response = ok(data=payload.dict())

  response.set_cookie(**cookie_config)

  return response


# Count record of page
# Param:
#   @users_service: User service
# Output:
#   return: HTTP response
# @user_routers.get("/count-record", tags=["user"], responses={200:{"model": Response[CountRecordResponse]}}, dependencies=[Depends(authorized_user)])
@user_routers.get("/count-record", tags=["user"], responses={200:{"model": Response[CountRecordResponse]}}, dependencies=[Depends(authorized_user)])
@inject
def count_record(users_service: UsersService = Depends(Provide(Container.users_service))):
  # remake token
  data_user = users_service.get_user_me()
  data = users_service.count_record(data_user["user"]["office_id"])
  payload = CountRecordResponse(**data)
  response = ok(data=payload.dict())

  return response


# List user
# Param:
#   @users_service: User service
# Output:
#   return: HTTP response
@user_routers.get("", tags=["user"], responses={200: {"model": Response[ListUserResponse]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def get_list(users_service: UsersService = Depends(Provide(Container.users_service))):
  # Get list user
  data_user = users_service.get_list()
  payload = ListUserResponse(**data_user)
  response = ok(data=payload.dict())

  return response


# List user interviewer
# Param:
#   @users_service: User service
# Output:
#   return: HTTP response
@user_routers.get("/interviewer", tags=["user"], responses={200: {"model": Response[ListLeaderResponse]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def get_list_interviewer(users_service: UsersService = Depends(Provide(Container.users_service))):
  # Get list user
  data_user = users_service.get_list_interviewer()
  payload = ListLeaderResponse(**data_user)
  response = ok(data=payload.dict())

  return response



# Get info of one user
# Param:
#   @users_service: User service
# Output:
#   return: HTTP response
@user_routers.get("/{employee_code}", tags=["user"], responses={200: {"model": Response[UserResponse]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def get_user(employee_code: str, users_service: UsersService = Depends(Provide(Container.users_service))):
  # Get info of one user
  data_user = users_service.get_user(employee_code)
  payload = UserResponse(**data_user)
  response = ok(data=payload.dict())

  return response


# Register user
# Param:
#   @body: Data request
#   @users_service: User service
# Output:
#   return: HTTP response
@user_routers.post("", tags=["user"], responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def add(body: UserRegisterRequest, users_service: UsersService = Depends(Provide(Container.users_service))):
  # Add user new
  users_service.add(body)

  return ok()


# Change password
# Param:
#   @body: Data request
#   @users_service: User service
# Output:
#   return: HTTP response
@user_routers.put("/password", tags=["user"], responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@inject
async def change_password(body: ChangePasswordRequest, users_service: UsersService = Depends(Provide(Container.users_service))):
  users_service.change_password(body.dict())
  return ok()


# Update user
# Param:
#   @body: Data request
#   @users_service: User service
# Output:
#   return: HTTP response
@user_routers.put("/{employee_code}", tags=["user"], responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@inject
async def edit(employee_code: str, body: UserEditRequest, users_service: UsersService = Depends(Provide(Container.users_service))):
  # Update info of user
  users_service.edit(employee_code, body.dict())

  return ok()


# Delete user
# Param:
#   @employee_code: employee code of user
#   @users_service: User service
# Output:
#   return: HTTP response
@user_routers.delete("/{employee_code}", tags=["user"], responses={200: {"model": Response[dict]}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN, ROLE.LEADER, ROLE.MANAGER])
@inject
async def delete(employee_code: str, users_service: UsersService = Depends(Provide(Container.users_service))):
  # Delete user
  users_service.delete(employee_code)

  return ok()


# Send mail forgot password
# Param:
#   @body: Data request
#   @users_service: User service
# Output:
#   return: HTTP response
@user_routers.post("/forgot-password", tags=["user"], responses={200: {"model": Response[dict]}})
@inject
async def send_mail_forgot_password(body: ForgotPasswordRequest, users_service: UsersService = Depends(Provide(Container.users_service))):
  await users_service.send_mail_forgot_password(body.email)

  return ok()


# Send mail forgot password
# Param:
#   @body: Data request
#   @users_service: User service
# Output:
#   return: HTTP response
@user_routers.get("/forgot-password/{token:str}", tags=["user"], responses={200: {"model": Response[dict]}})
@inject
async def check_token_forgot_password(token: str, users_service: UsersService = Depends(Provide(Container.users_service))):
  users_service.check_token_forgot_password(token)

  return ok()


# Reset password
# Param:
#   @body: Data request
#   @users_service: User service
# Output:
#   return: HTTP response
@user_routers.put("/reset-password/{token:str}", tags=["user"], responses={200: {"model": Response[dict]}})
@inject
async def reset_password(token: str, body: ResetPasswordRequest, users_service: UsersService = Depends(Provide(Container.users_service))):
  users_service.reset_password(token, body.dict())

  return ok()
