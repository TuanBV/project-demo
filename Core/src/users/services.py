"""
Users Service
"""
from core import CommonException, ERR_MESSAGE
import helpers.jwt as jwt
from helpers.common import checkpw, bcrypt
from helpers.const import CODE
from helpers.mailer import Mailer
from users import UsersRepository
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timedelta

class UsersService:
  """
    Users service
  """
  def __init__(self, users_repository: UsersRepository):
    self.users_repo: UsersRepository = users_repository



  # Handle login user
  # Param:
  #   @data: Data request
  # Return: User information and token
  def login(self, data):
    payload = {}

    # Execute query
    user_account = self.users_repo.get_user_data(email = data["email"].lower())

    # Check data user and password is correct or not
    if user_account:
      if user_account.login_failed_count > 5:
        # Contact admin
        raise CommonException(message=ERR_MESSAGE.CONTACT_ADMIN)

      if checkpw(data["password"].strip(), user_account.password):
        user_account = jsonable_encoder(user_account)

        del user_account["password"]
        del user_account["login_failed_count"]

        # Reset login failed count
        self.users_repo.update_login_failed_count(data["email"].lower(), 0)

        payload["token"] = jwt.hash_token(user_account)

        payload["user"] = user_account

        return payload

      # Update login failed count
      self.users_repo.update_login_failed_count(data["email"].lower(), user_account.login_failed_count + 1)

    # Invalid email or password
    raise CommonException(message=ERR_MESSAGE.INVALID_EMAIL_OR_PASSWORD)


  # # Get info of one user
  # # Param:
  # # office_id: id of office
  # # Output:
  # #  return: data count record
  # def count_record(self, office_id):
  #   data = self.users_repo.count_record(office_id)

  #   return data


  # # Get info of one user
  # # Param:
  # #  @employee_code: Employee code
  # # Output:
  # #  return: data admin
  # def get_user_me(self):
  #   payload = {}
  #   # Execute query
  #   user_account = self.users_repo.get_user_data()

  #   # Check data user in DB
  #   if user_account:
  #     user_account = jsonable_encoder(user_account)

  #     del user_account["password"]

  #     payload["token"] = jwt.hash_token(user_account)

  #     payload["user"] = user_account

  #     return payload


  # # Check data of admin function
  # # Param:
  # #  @employee_code: Employee code
  # # Output:
  # #  return: data admin
  # def get_user(self, employee_code):
  #   payload = {}
  #   # Execute query
  #   payload = self.users_repo.get_user_by_employee_code(employee_code)
  #   return jsonable_encoder(payload)


  # # List user
  # # Param: None
  # # Return: None
  # def get_list(self):
  #   data_user = self.users_repo.get_list()

  #   return {
  #     "list_user": jsonable_encoder(data_user),
  #   }


  # # Edit info of user
  # # Param:
  # #   @data: Data request
  # # Return: None
  # def edit(self, employee_code, data):
  #   # Update info of user

  #   self.users_repo.edit(employee_code, data)


  # # Register user new
  # # Param:
  # #   @data: Data request
  # # Return: None
  # def add(self, data):
  #   # Add customer new
  #   self.users_repo.add(data.dict())


  # # Delete user
  # # Param:
  # #   @employee_code: employee code of user
  # # Return: None
  # def delete(self, employee_code):
  #   # Get user by employee_code
  #   user = self.users_repo.get_user_by_employee_code(employee_code)
  #   # Check user has exist
  #   if not user:
  #     raise CommonException(message=ERR_MESSAGE.MSG_0004)

  #   # Delete user
  #   self.users_repo.delete(employee_code)


  # # Send mail forgot password
  # # Param:
  # #   @email: Email
  # # Return: None
  # async def send_mail_forgot_password(self, email: str):
  #   user = self.users_repo.get_user_data(email.lower())

  #   if not user:
  #     raise CommonException(code=CODE.API.NOT_FOUND, message=ERR_MESSAGE.EMAIL_EXIST)

  #   user = jsonable_encoder(user)
  #   # Get template forgot password
  #   template = self.templates_repo.get_template_by_key("forgot_password")
  #   # Get params in db
  #   params = self.parameters_repo.get_by_params_name(template["params"])
  #   # Get value params
  #   values = self.parameters_repo.get_key_value_by_params(params, employee_code=user["employee_code"])
  #   self.users_repo.edit(user["employee_code"], {
  #     "token": values["$LinkFogotPassword"]["token"],
  #     "expire": datetime.now() + timedelta(hours=1)
  #   })

  #   # Replace param in body and title
  #   for key in values:
  #     if key == "$LinkFogotPassword" or key == "$LinkForm":
  #       template["body"] = template["body"].replace(key, str(values[key]["link"]))
  #       template["title"] = template["title"].replace(key, str(values[key]["link"]))
  #     else:
  #       template["body"] = template["body"].replace(key, str(values[key]))
  #       template["title"] = template["title"].replace(key, str(values[key]))

  #   # Get user office
  #   office = self.offices_repo.find(user["office_id"])

  #   # Handle send mail
  #   mailer = Mailer(username=office.mail_admin, password=office.password_mail)
  #   await mailer.set_mail_from(office.mail_admin).subject(template["title"]) \
  #     .html(template["body"]).recipient(user["email"]).send()

  #   # Handle create mail
  #   mail = {
  #     "title": template["title"],
  #     "body": template["body"],
  #     "mail_to": user["email"],
  #     "status": 1
  #   }
  #   self.mails_repo.create_mail(mail)


  # # Handle change password
  # # Params:
  # #   @data: Data
  # # Output:
  # #   return: None
  # def change_password(self, data):
  #   if data["new_password"] != data["confirm_password"]:
  #     raise CommonException(message=ERR_MESSAGE.CONFIRM_PASSWORD)
  #   self.users_repo.change_password(data)


  # # Check token forgot password
  # # Param:
  # #   @token: Token
  # # Return: None
  # def check_token_forgot_password(self, token: str):
  #   user = self.users_repo.get_user_by_token(token)
  #   if not user:
  #     raise CommonException(message=ERR_MESSAGE.LINK_RESET_PASSWORD_EXPIRED)


  # # Reset password
  # # Param:
  # #   @token: Token
  # #   @data: Data
  # # Return: None
  # def reset_password(self, token: str, data: dict):
  #   user = self.users_repo.get_user_by_token(token)
  #   if not user:
  #     raise CommonException(message=ERR_MESSAGE.LINK_RESET_PASSWORD_EXPIRED)

  #   if data["new_password"] != data["confirm_password"]:
  #     raise CommonException(message=ERR_MESSAGE.CONFIRM_PASSWORD)

  #   self.users_repo.edit(user.employee_code, {
  #     "token": "",
  #     "expire": "1970-01-01 00:00:00",
  #     "password": bcrypt(data["new_password"])
  #   })


  # # Get list interviewer
  # # Params: None
  # # Output:
  # #   return: List data employee
  # def get_list_interviewer(self):
  #   data_user = self.users_repo.get_list_interviewer()
  #   return {
  #       "item": jsonable_encoder(data_user)
  #     }
