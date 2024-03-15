"""
SHOP Service
"""
import pyotp
import base64
from core import CrmException, CrmUnauthorizedException, ERR_MESSAGE
import helpers.encryption as encrypt
import helpers.jwt as jwt
import helpers.const as env
from helpers import kbn
import helpers.sms as sms
import mail_template.auth_two_step as mail_auth_two_step
import sms_template.shop_auth_2_step as shop_auth_2_step
from datetime import (datetime, timedelta)
from mail_template import (shop_login_notify, shop_forgot_password, shop_reset_password)
from jinja2 import Template
from utils.date import get_current_time_obj
from utils.aws import create_presigned_url, apply_task
from fastapi.encoders import jsonable_encoder
from crm_shop import ShopRepository
from setting import settings
from celery.utils import uuid

class ShopService:
  """
    Service shop
  """
  def __init__(self, shop_repository: ShopRepository):
    self.shop_repo: ShopRepository = shop_repository

  # Set data time of otp
  # Params:
  #   @shop_account: Data shop account
  # Output:
  #   Return: Data otp
  def __set_data_time_otp(self, shop_account):
    otp_ret = {}
    # Auth 2 step by email
    if shop_account["two_fa_kbn"] == kbn.TwoFaType.MAIL.value:
      # Send Otp
      otp_ret = self.send_mail_otp(shop_account)

    # Auth 2 step by SMS
    elif shop_account["two_fa_kbn"] == kbn.TwoFaType.SMS.value:
      # Send Otp
      otp_ret = self.send_sns_otp(shop_account)

    return otp_ret


  # Get data login authentication
  # Params:
  #   @dict_shop_account: Dict of data shop account
  #   @data: Data request
  #   @response_shop_account: Data shop account
  # Output:
  #   return: Data login
  def __get_data_login_auth(self, dict_shop_account, data, response_shop_account):
    # Two-step authentication with google
    if dict_shop_account["two_fa_kbn"] == kbn.TwoFaType.GOOGLE.value:
      otp = pyotp.TOTP(dict_shop_account["secret_otp"])
      # Valid OTP code
      if otp.verify(data["otp"]):

        return self.get_data_login(dict_shop_account)

    # Two-step authentication with sms or mail
    else:
      for_time = datetime.fromtimestamp(int(data["time_now"] + data["time_remaining"]))
      otp = pyotp.TOTP(dict_shop_account["secret_otp"], interval=kbn.TIME_OUT_OTP)
      now = get_current_time_obj().timestamp()

      # Valid OTP code
      if now < (data["time_now"] + kbn.TIME_OUT_OTP):
        if otp.verify(data["otp"], for_time=for_time) and data["otp"] == response_shop_account.otp:
          return self.get_data_login(dict_shop_account)

    return None


  # Create unique token and add to token
  # Param:
  #   @dict_shop_account: Dict of data shop account
  # Output:
  #   Return: jwt token
  def create_unique_token(self, dict_shop_account):
    # set time expired
    expired = get_current_time_obj() + timedelta(seconds=env.ONE_HOUR)
    token = {
        "email": dict_shop_account["email"],
        "two_fa_flg": dict_shop_account["two_fa_flg"],
        "two_fa_kbn": dict_shop_account["two_fa_kbn"],
        "exp": expired.timestamp()
    }

    # hash token & result token
    return jwt.hash_token(token)


  # Handle login shop
  # Param:
  #   @data: Data request
  # Return: Shop information and shop account information
  def login(self, data):
    email = data["email"].lower()
    # Execute query
    response_shop_account = self.shop_repo.get_shop_account_by_email(email)
    if response_shop_account and response_shop_account.password == encrypt.hash256(data["password"]):
      dict_shop_account = response_shop_account.__dict__
      # Turn on two-factor authentication
      if response_shop_account.two_fa_flg.value == kbn.AUTH_TWO_STEP.ON:
        # Setting secret otp
        if "secret_otp" not in dict_shop_account or not dict_shop_account["secret_otp"]:
          dict_shop_account.secret_otp = pyotp.random_base32()

        # Create token
        auth_2_token = self.create_unique_token(dict_shop_account)
        return {
          "two_fa_kbn": response_shop_account.two_fa_kbn.value,
          "two_fa_flg": kbn.AUTH_TWO_STEP.ON,
          "otp_token": auth_2_token
        }

      # Set data login in cookie
      return self.get_data_login(dict_shop_account)

    # Shop not exist
    raise CrmException(message=ERR_MESSAGE.ERRMSG0038)


  # Check token verify
  # Param:
  #   @data: Data request
  # Return: Email shop or False
  def verify_token(self, data):
    result = False

    # Execute database
    response_shop_account = self.shop_repo.get_shop_account(data["id"])

    # Have a shop account
    if response_shop_account and response_shop_account.token == data["token"]:
      # Get token expiration time
      token_expiration_time = response_shop_account.token_expiration_time

      # remove timezone
      now = get_current_time_obj().replace(tzinfo=None)

      # Token expiration time is greater than current time
      if token_expiration_time > now:
        result = response_shop_account.email
    # Data return
    return result


  # Handle reset password
  # Param:
  #   @data: data request
  # Return: Boolean
  def reset_password(self, data):
    # Execute query
    response_shop_account = self.shop_repo.get_shop_account(data["id"])
    # Have a shop account
    if response_shop_account:
      # Hash password
      password = encrypt.hash256(data["password"]["password_new"])

      # Update data shop account
      user_update = response_shop_account.id

      # Update password new
      self.shop_repo.update_password(data["id"], password, user_update)


      # Account has notify when do change password
      if response_shop_account.password_change_notification_flg == kbn.ChangeNotificationFlag.ACTIVE.value:
        # Start send mail
        shop_no = response_shop_account.shop_no
        # Get shop information
        email = response_shop_account.email
        response_shop = self.shop_repo.get_shop(shop_no)

        full_name_owner = response_shop.last_name + response_shop.first_name
        # Set content for mail
        data_mail = {
            "shopNo": shop_no,
            "corporateName": response_shop.corporate_name,
            "fullNameOwner": full_name_owner,
            "mailAddress": email,
            "urlResetPassword": "",
            "systemTel": env.SYSTEM_TEL
        }

        # Set subject mail
        subject_template = Template(f"【{env.SERVICE_NAME}】パスワード変更手続き完了のお知らせ")
        subject = subject_template.render(data_mail)

        # Template mail
        template_mail = shop_reset_password
        # Replace keyword in template mail
        for item_template in kbn.DATA_TEMPLATE:
          template_mail.BODY_TEXT = template_mail.BODY_TEXT.replace(item_template, kbn.DATA_TEMPLATE[item_template])

        # Set body mail
        template_obj = Template(template_mail.BODY_TEXT)
        body_text = template_obj.render(data_mail)

        # Get config mail admin
        mail_admin = self.shop_repo.get_site_config()

        # Set destination of mail
        destination = {"ToAddresses": [response_shop_account.email], "BccAddresses": mail_admin}

        data_msg = {
          "subject": subject,
          "destination": destination,
          "body_mail": body_text
        }

        job_id_send_mail = uuid()

        # Add item of batches table
        self.shop_repo.add_batches(job_id_send_mail, settings.QUEUE_SEND_MAIL_REGISTRATION, "send_mail_registration", {"data_msg": data_msg}, shop_no)

        # Push message to RabbitMQ
        apply_task(job_id_send_mail, env.TASK_NAME.SEND_MAIL_REGISTRATION, {"data_msg": data_msg})

        # End send mail
      return True

    # Don't have a shop account
    else:
      return False


  # Handle sending, generate url to shop email to reset password
  # Param:
  #   @mail_address: mail of account
  # Return: Url to reset password
  def mail_reset_password(self, mail_address):
    email = mail_address.lower()

    # Execute query
    response_shop_account = self.shop_repo.get_shop_account_by_email(email)

    ts_now = str(get_current_time_obj().timestamp()).replace(".", "")
    token = encrypt.hash256(ts_now)
    token_expiration_time = get_current_time_obj() + timedelta(hours=1)

    # Update token and token_expiration_time of shop account
    self.shop_repo.update_shop_account_forgot_pw(email, token, token_expiration_time)

    # Generate url to reset password
    url_reset_pass = f"{settings.DOMAIN_CLIENT}shop/" + "forgot-password/reset-password" + f"?said={response_shop_account.id}" + f"&tk={token}"

    # Get shop_no of shop
    shop_no = response_shop_account.shop_no

    # Get shop information
    response_shop = self.shop_repo.get_shop(shop_no)
    full_name_owner = response_shop.last_name + response_shop.first_name

    # Set content of mail
    data_mail = {
        "shopNo": shop_no,
        "corporateName": response_shop.corporate_name,
        "fullNameOwner": full_name_owner,
        "mailAddress": email,
        "urlResetPassword": url_reset_pass,
        "systemTel": env.SYSTEM_TEL
    }

    # Set subject mail
    subject_template = Template(f"【{env.SERVICE_NAME}】パスワード再設定のお手続き")
    subject = subject_template.render(data_mail)

    # Template mail
    template_mail = shop_forgot_password
    # Replace keyword in template mail
    for item_template in kbn.DATA_TEMPLATE:
      template_mail.BODY_TEXT = template_mail.BODY_TEXT.replace(item_template, kbn.DATA_TEMPLATE[item_template])

    # Set body mail
    template_obj = Template(template_mail.BODY_TEXT)
    body_text = template_obj.render(data_mail)

    # Get config mail admin
    response_table_config = self.shop_repo.get_data_configs("MAIL_ADMIN")
    list_mail_admin = []
    for item in response_table_config:
      list_mail_admin.append(item.value)

    # Set destination of mail
    destination = {"ToAddresses": [email], "BccAddresses": list_mail_admin}

    data_msg = {
      "subject": subject,
      "destination": destination,
      "body_mail": body_text
    }

    job_id_send_mail = uuid()

    # Add item of batches table
    self.shop_repo.add_batches(job_id_send_mail, settings.QUEUE_SEND_MAIL_REGISTRATION, "send_mail_registration", {"data_msg": data_msg}, shop_no)

    # Push message to RabbitMQ
    apply_task(job_id_send_mail, env.TASK_NAME.SEND_MAIL_REGISTRATION, {"data_msg": data_msg})


  # Get information of shop account
  # Param:
  #   @shop_account_id: id of shop account
  # Return: Information of shop account
  def get_user_me(self, shop_account_id):
    # Execute data template by shop_no data["id"]
    response_shop_account = self.shop_repo.get_shop_account(shop_account_id)

    # Check shop exist
    if response_shop_account:
      # Convert model to dict
      dict_shop_account = response_shop_account.__dict__

      # Execute query
      response_shop = self.shop_repo.get_shop(response_shop_account.shop_no)

      # Don't have secret code generate otp
      if "secret_otp" not in dict_shop_account or not dict_shop_account["secret_otp"]:
        dict_shop_account["secret_otp"] = pyotp.random_base32()
        # Update secret otp of shop
        self.shop_repo.update(dict_shop_account)

      # Execute data setting rank by shop_no
      response_setting_rank = self.shop_repo.get_setting_rank(response_shop_account.shop_no)

      # Get action type
      response_action_type = self.shop_repo.get_action_types()

      # Get templates of shop
      data_templates = self.shop_repo.get_template_by_id(response_shop_account.shop_no)

      # Get setting shop
      result_flag_prepare_data_act = self.shop_repo.find_setting_shop_by_shop_no(response_shop_account.shop_no, "flag_prepare_data_action")

      # Encode response_shop
      shop = jsonable_encoder(response_shop)

      # Get payment method
      response_payment = self.shop_repo.get_payment_method(shop["payment_method_code"])

      # Get link full of image avatar
      arr_image = shop["avatar"].split("/")
      key_file = env.S3.DIRECTORY.SHOP.AVATAR + arr_image[-1]

      # Get URL of file csv in s3
      response_image = create_presigned_url(key_file)
      shop["avatar"] = response_image

      # Set value for shop
      if "logo" in shop.keys() and shop["logo"]:
        logo_image = shop["logo"].split("/")
        logo_file = env.S3.DIRECTORY.SHOP.LOGO + logo_image[-1]
        shop["logo"] = create_presigned_url(logo_file)
      else:
        shop["logo"] = ""
      if shop.get("name") is None: shop["name"] = ""
      if shop.get("slogan") is None: shop["slogan"] = ""
      if shop.get("color") is None: shop["color"] = kbn.COLOR_DEFAULT

      # Get uri to generate otp code
      uri = pyotp.totp.TOTP(dict_shop_account["secret_otp"]).provisioning_uri(name=dict_shop_account["email"], issuer_name=kbn.SYSTEM_NAME)
      dict_shop_account["uri_qr_code_otp"] = base64.b64encode(uri.encode("ascii"))

      shop["url"] = f"{settings.DOMAIN_CLIENT}{shop['url']}"
      dict_shop_account["shop"] = shop
      dict_shop_account["shop"]["payment_method_code"] = response_payment.code.value
      dict_shop_account["shop"]["action_type"] = response_action_type
      dict_shop_account["shop"]["template_mail"] = data_templates
      dict_shop_account["shop"]["setting_rank"] = jsonable_encoder(response_setting_rank)
      dict_shop_account["shop"]["flag_prepare_data_action"] = result_flag_prepare_data_act.value

      payload = {
          "user": dict_shop_account,
          "role": dict_shop_account["role_kbn"].value
      }

      # Preparing data cookie
      user_key = {
        "id": payload["user"]["id"],
        "shop_no": payload["user"]["shop_no"],
        "email": payload["user"]["email"],
      }

      user_key["shop"] = {}
      user_key["shop"]["template_mail"] = {
        "customer_register_success": payload["user"]["shop"]["template_mail"]["customer_register_success"],
        "customer_edit_success": payload["user"]["shop"]["template_mail"]["customer_edit_success"],
        "member_unsubscribe_success": payload["user"]["shop"]["template_mail"]["member_unsubscribe_success"],
      }
      user_key["shop"]["id"] = payload["user"]["shop"]["id"]
      user_key["shop"]["url"] = payload["user"]["shop"]["url"]
      user_key["shop"]["address1"] = payload["user"]["shop"]["address1"]
      user_key["shop"]["address2"] = payload["user"]["shop"]["address2"]
      user_key["shop"]["address3"] = payload["user"]["shop"]["address3"]
      user_key["shop"]["telephone_no"] = payload["user"]["shop"]["telephone_no"]
      user_key["shop"]["zip_code"] = payload["user"]["shop"]["zip_code"]
      user_key["shop"]["corporate_name"] = payload["user"]["shop"]["corporate_name"]
      user_key["shop"]["setting_rank"] = jsonable_encoder(response_setting_rank)

      # set data for jwt of token
      data_cookie = {
        "user": user_key,
        "role": payload["role"]
      }

      # Hash data cookie
      payload["token"] = jwt.hash_token(data_cookie)

      # The result
      return jsonable_encoder(payload)

    # Shop not exist
    raise CrmUnauthorizedException(message=ERR_MESSAGE.ERRMSG0038)



  # Check two step authentication
  # Param:
  #   @data: Data request
  #   @token_two_auth: Token two step authentication
  # Return: Information of shop account
  def auth_two_step(self, data, token_two_auth):
    # Decode token
    data_token = jwt.verify(token_two_auth)

    # time current
    current = get_current_time_obj()
    # Validate token
    if current.timestamp() > data_token["exp"]:
      raise CrmUnauthorizedException(message=ERR_MESSAGE.ERRMSG0180)

    # Email in token data
    if "email" in data_token:
      email = data_token["email"].lower()
      # Get shop account by email
      response_shop_account = self.shop_repo.get_shop_account_by_email(email)
      dict_shop_account = response_shop_account.__dict__

      # Have a shop account
      if response_shop_account:
        data_login = self.__get_data_login_auth(dict_shop_account, data, response_shop_account)
        if data_login:
          return data_login

        # Invalid OTP code
        raise CrmException(message=ERR_MESSAGE.ERRMSG0060)

      # Don't have a shop account
      else:
        raise CrmUnauthorizedException(message=ERR_MESSAGE.ERRMSG0061)

    # Email not in token data
    else:
      raise CrmUnauthorizedException(message=ERR_MESSAGE.ERRMSG0180)


  # Get data login
  # Param:
  #   @dict_shop_account: information of shop account
  # Return: Information of shop account
  def get_data_login(self, dict_shop_account):
    # Get shop_account_id of shop
    shop_account_id = dict_shop_account["id"]

    # Get data of shop
    payload = self.get_user_me(shop_account_id)

    # Check flag login notification has ACTIVE
    if dict_shop_account["login_notification_flg"] == kbn.LoginNotificationFlag.ACTIVE.value:
      # Start send mail
      data_mail = {
        "corporateName": payload["user"]["shop"]["corporate_name"],
        "shopOwnerFullName": payload["user"]["shop"]["last_name"] + payload["user"]["shop"]["first_name"],
        "mailAddress": dict_shop_account["email"],
        "loginTime": get_current_time_obj().strftime("%Y.%m.%d %H:%M:%S"),
      }
      # Get all shop account
      lst_account_manager = self.shop_repo.get_manager_owner(dict_shop_account["shop_no"])
      subject_template = Template("【{{ corporateName }} 管理者】ログイン通知")
      subject = subject_template.render(data_mail)

      # Template mail
      template_mail = shop_login_notify
      # Replace keyword in template mail
      for item_template in kbn.DATA_TEMPLATE:
        template_mail.BODY_TEXT = template_mail.BODY_TEXT.replace(item_template, kbn.DATA_TEMPLATE[item_template])

      # Set body mail
      template_obj = Template(template_mail.BODY_TEXT)
      body_text = template_obj.render(data_mail)

      # Get config mail admin
      mail_admin = self.shop_repo.get_data_configs("mail_admin")
      list_mail_admin = []
      for item in mail_admin:
        list_mail_admin.append(item.value)

      # Set destination of mail
      for account in lst_account_manager:
        # Destination
        destination = {"ToAddresses": [account["email"]], "BccAddresses": list_mail_admin}

        data_msg = {
          "subject": subject,
          "destination": destination,
          "body_mail": body_text
        }

        job_id_send_mail = uuid()

        # Add item of batches table
        self.shop_repo.add_batches(job_id_send_mail, settings.QUEUE_SEND_MAIL_REGISTRATION, "send_mail_registration", {"data_msg": data_msg})

        # Push message to RabbitMQ
        apply_task(job_id_send_mail, env.TASK_NAME.SEND_MAIL_REGISTRATION, {"data_msg": data_msg})

        # End send mail

    # Data return
    return payload


  # Send otp code to account email
  # Param:
  #   @account: Data account
  # Return: Current time and remaining time of otp code
  def send_mail_otp(self, account):
    email = account["email"]
    totp = pyotp.TOTP(account["secret_otp"], interval=kbn.TIME_OUT_OTP)

    # get the remaining time of the otp code
    time_remaining = totp.interval - get_current_time_obj().timestamp() % totp.interval
    time_now = get_current_time_obj().timestamp()
    time_at = time_now + time_remaining

    # Create new OTP
    otp = totp.at(for_time=time_at)
    account["otp"] = otp

    # Update data shop account
    self.shop_repo.update_otp_shop_account(account["email"], otp)


    title = f"【{env.SERVICE_NAME}】２段階認証"
    data_mail = {"otp": otp}
    result = {
      "time_remaining": time_remaining,
      "time_now": time_now
    }

    # Template mail
    template_mail = mail_auth_two_step
    # Replace keyword in template mail
    for item_template in kbn.DATA_TEMPLATE:
      template_mail.BODY_TEXT = template_mail.BODY_TEXT.replace(item_template, kbn.DATA_TEMPLATE[item_template])

    template_obj = Template(template_mail.BODY_TEXT)
    body_text = template_obj.render(data_mail)

    # Send mail otp to shop account
    destination = {"ToAddresses": [email]}

    data_msg = {
      "subject": title,
      "destination": destination,
      "body_mail": body_text
    }

    job_id_send_mail = uuid()

    # Add item of batches table
    self.shop_repo.add_batches(job_id_send_mail, settings.QUEUE_SEND_MAIL_REGISTRATION, "send_mail_registration", {"data_msg": data_msg}, account["shop_no"])

    # Push message to RabbitMQ
    apply_task(job_id_send_mail, env.TASK_NAME.SEND_MAIL_REGISTRATION, {"data_msg": data_msg})
    # End send mail

    return result


  # Send otp code to account phone number
  # Param:
  #   @account: Data account
  # Return: Current time and remaining time of otp code
  def send_sns_otp(self, account):
    telephone_no = account["telephone_no"]
    totp = pyotp.TOTP(account["secret_otp"], interval=kbn.TIME_OUT_OTP)

    # get the remaining time of the otp code
    time_remaining = totp.interval - get_current_time_obj().timestamp() % totp.interval
    time_now = get_current_time_obj().timestamp()
    time_at = time_now + time_remaining

    # Create new OTP
    otp = totp.at(for_time=time_at)
    account["otp"] = otp

    # Update otp of shop account
    self.shop_repo.update_otp_shop_account(account["email"], otp)

    # Get config country code
    response_country_code = self.shop_repo.get_country_code()

    # Send SMS otp to shop account
    temp = Template(shop_auth_2_step.BODY_TEXT)

    body_text = temp.render(account)
    # Get international phone number
    phone_number = telephone_no.replace("0", response_country_code.value, 1)

    ret = {
      "time_remaining": time_remaining,
      "time_now": time_now
    }

    # Send SMS
    sms.send_sms(phone_number, body_text)
    return ret


  # Resend the otp code by email or sms
  # Param:
  #   @token_two_auth: Token two step authentication
  # Return: Message, current time and remaining time of otp code
  def send_otp(self, token_two_auth):
    # Decode token
    data_token = jwt.verify(token_two_auth)

    # time current
    current = get_current_time_obj()
    messages = ""
    # Validate token
    if current.timestamp() > data_token["exp"]:
      messages = ERR_MESSAGE.ERRMSG0180
      raise CrmUnauthorizedException(message=messages)

    # Email in token data
    if "email" in data_token:
      # Get data shop account by email
      response_shop_account =self.shop_repo.get_shop_account_by_email(data_token["email"])

      # Have a shop account
      if response_shop_account:
        shop_account = response_shop_account.__dict__
        # Turn on two-factor authentication
        if shop_account["two_fa_flg"].value == kbn.TwoFaFlg.ON.value:
          # Create token
          auth_2_token = self.create_unique_token(jsonable_encoder(response_shop_account))

          # Auth 2 step by google
          if shop_account["two_fa_kbn"] == kbn.TwoFaType.GOOGLE.value:
            messages = ERR_MESSAGE.ERRMSG0062
            raise CrmUnauthorizedException(message=messages)

          otp_ret = self.__set_data_time_otp(shop_account)

          return {
            "message": "認証コードは成功に送信しました。",
            "time_remaining": otp_ret["time_remaining"],
            "time_now": otp_ret["time_now"],
            "otp_token": auth_2_token
          }

        # Turn off two-factor authentication
        else:
          messages = ERR_MESSAGE.ERRMSG0063

      # Don't have a shop account
      else:
        messages = ERR_MESSAGE.ERRMSG0061

    # Email not in token data
    else:
      messages = ERR_MESSAGE.ERRMSG0180

    # raise message error
    raise CrmUnauthorizedException(message=messages)


  # Check allow otp confirm
  # Param:
  #   @token_two_auth: Token two step authentication
  # Return: State auth two step and auth two step type
  def check_allow_otp_confirm(self, token_two_auth):
    # Decode token
    data_token = jwt.verify(token_two_auth)
    # time current
    current = get_current_time_obj()

    # Validate token
    if current.timestamp() > data_token["exp"]:
      raise CrmUnauthorizedException(message=ERR_MESSAGE.ERRMSG0180)

    # Email in token data
    if "email" in data_token:
      response_shop_account = self.shop_repo.get_shop_account_by_email(data_token["email"])
      # Have a shop account
      if response_shop_account:
        shop_account = response_shop_account.__dict__

        return {
          "two_fa_flg": shop_account["two_fa_flg"],
          "two_fa_kbn": shop_account["two_fa_kbn"]
        }

      # Don't have a shop account
      else:
        raise CrmUnauthorizedException(message=ERR_MESSAGE.ERRMSG0063)

    # Email not in token data
    else:
      raise CrmUnauthorizedException(message=ERR_MESSAGE.ERRMSG0180)


  # Update security
  # Param:
  #   @data_security: data update
  #   @shop_no: shop_no of shop
  #   @shop_account_id: id of shop
  # Return: State auth two step and auth two step type
  def update_security(self, shop_no, data_security, shop_account_id):
    payload = {}

    # Check shop exist
    if self.shop_repo.get_shop(shop_no):
      shop_account = self.shop_repo.get_shop_account(shop_account_id)
      otp = pyotp.TOTP(shop_account.secret_otp)
      # Check otp
      if data_security["otp"] and not otp.verify(data_security["otp"]):
        raise CrmException(message=ERR_MESSAGE.ERRMSG0060)

      # Set data update
      data_security["updated_user"] = f"shop_account: {shop_account_id}"

      # Update security
      self.shop_repo.update_security(shop_account_id, data_security)
      payload = data_security
      return payload

    # Shop not exist
    raise CrmException(message=ERR_MESSAGE.ERRMSG0038)
