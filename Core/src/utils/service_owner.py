"""
Service owner utils
"""

from copy import deepcopy
import pyotp
from helpers import kbn
import helpers.encryption as encryt
from utils.date import format_date_time, get_current_time_obj
from jinja2 import Template
from sqlalchemy import desc, asc
from models import Shops


# Fill data account of shop function (ADD)
# Param:
#  @data: data account
#  @shop_no: shop no
#  @user: admin information
# Output:
#  return: data acount
def fill_data_add_shop_acc(data, shop_no, user):
  data_acc = deepcopy(data)
  data_acc["email"] = data["email"].lower()
  data_acc["shop_no"] = shop_no
  data_acc["password"] = encryt.hash256(data["password"])
  data_acc["secret_otp"] = ""
  data_acc["token"] = ""

  # if 2-step security is on, it will generate an OTP
  data_acc["two_fa_flg"] = data_acc["two_fa_flg"].value
  if data_acc["two_fa_flg"] == int(kbn.TwoFaFlg.ON.value):
    data_acc["secret_otp"] = pyotp.random_base32()

  data_acc["created_user"] = f"admin: {user}"
  data_acc["role_kbn"] = data_acc["role_kbn"].value
  data_acc["password_change_notification_flg"] = data_acc["password_change_notification_flg"].value
  data_acc["login_notification_flg"] = data_acc["login_notification_flg"].value
  data_acc["two_fa_kbn"] = data_acc["two_fa_kbn"].value
  return data_acc


# Fill data account of shop function (EDIT)
# Param:
#  @data: data account
#  @shop_no: shop no
#  @user: admin information
# Output:
#  return: data account
def fill_data_edit_shop_acc(new_data, old_data, user):
  data_acc = {}
  time_current_obj = get_current_time_obj()
  data_acc["email"] = new_data["email"].lower()
  data_acc["two_fa_flg"] = new_data["two_fa_flg"].value

  # if 2-step security is on
  if data_acc["two_fa_flg"] == kbn.TwoFaFlg.ON.value:
    # If old data not have OTP it will generate an OTP
    if hasattr(old_data, "secret_otp") or old_data.secretOtp == "":
      data_acc["secret_otp"] = pyotp.random_base32()
    # Set old OTP
    else:
      data_acc["secret_otp"] = old_data.secretOtp
  # If 2-step security is off set opt is empty
  else:
    data_acc["secret_otp"] = ""

  data_acc["two_fa_kbn"] = new_data["two_fa_kbn"].value
  data_acc["is_deleted"] = old_data.is_deleted.value
  data_acc["login_notification_flg"] = new_data["login_notification_flg"].value
  # If have new password will encrypt and
  # set date change password

  if new_data["password"] != "":
    data_acc["password"] = encryt.hash256(new_data["password"])
    data_acc["last_changed_password_time"] = format_date_time(time_current_obj, "%Y/%m/%d %H:%M:%S")
  # Set old password
  # set date change password
  else:
    data_acc["password"] = old_data.password
    data_acc["last_changed_password_time"] = old_data.last_changed_password_time

  data_acc["telephone_no"] = new_data["telephone_no"]
  data_acc["password_change_notification_flg"] = new_data["password_change_notification_flg"].value
  data_acc["created_user"] = old_data.created_user
  data_acc["created_date"] = old_data.created_date
  data_acc["role_kbn"] = old_data.role_kbn.value
  data_acc["shop_no"] = old_data.shop_no
  data_acc["token"] = old_data.token
  data_acc["token_expiration_time"] = old_data.token_expiration_time
  data_acc["updated_user"] = f"admin: {user}"

  return data_acc


# Send mail add account shop
# Params:
#   @mail_account: Mail account
#   @list_email_admin: List mail admin
#   @template: Mail template
#   @data_mail: Data mail
#   @subject: Subject of mail
# Output:
#   Return: Data send mail
def send_mail_account(mail_account, list_email_admin, template, data_mail, subject):
  destination = {"ToAddresses": [mail_account], "BccAddresses": list_email_admin}

  template_mail = template

  # Replace keyword in template mail
  for item_template in kbn.DATA_TEMPLATE:
    template_mail.BODY_TEXT = template_mail.BODY_TEXT.replace(item_template, kbn.DATA_TEMPLATE[item_template])

  template_obj = Template(template_mail.BODY_TEXT)
  body_text = template_obj.render(data_mail)

  return {
    "subject": subject,
    "destination": destination,
    "body_mail": body_text
  }


# Set sort value
# Params:
#   @sort_key: Sort key
#   @sort_type: Sort type
# Output:
#   Return: Sort value
def set_sort_value(sort_key, sort_type):
  # Set sort key and sort type to query
  column_name = Shops.created_date

  # Set sort_key
  if sort_key != "":
    column_name = Shops.__table__.c[sort_key]

  if sort_type not in ["asc", "desc"]:
    sort_type = "desc"

  # Set query sort
  if sort_type == "asc":
    sort_value = asc(column_name)
  else:
    sort_value = desc(column_name)

  return sort_value
