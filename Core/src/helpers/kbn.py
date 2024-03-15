"""
KBN
"""
import enum
from box import Box
import sqlalchemy as db

PREFIX_SUBJECT_MAIL = {
    "develop": " [develop]",
    "staging": "[STG]",
    "production": "",
}

# action status
ACT_STATUS = Box({
    "ALL": 0,
    "SENDED": 1,
    "NOTSEND": 2
})

# delete flag
DEL_FLG = Box({
    "OFF": 0,
    "ON": 1,
})
# type choose when move act to list_customer
TYPE_CHOOSE = Box({
    "TAGS": "tags",
    "CONDITION": "condition",
})
# user role
# 0: Admin service | 1: Shop Owner | 2: Shop Manager
# | 3: Shop Staff | 4: Customer(Member)
USER_ROLE = Box({
    "ADMIN": 0,
    "SHOP_OWNER": 1,
    "SHOP_MANAGER": 2,
    "SHOP_STAFF": 3,
    "CUSTOMER": 4
})
# tmpRegister Flag
TMPREGISTER_FLAG = Box({
    "SUCCESS": 0,
    "TEMPORARY": 1,
})
# Table name
NOTIFY = Box({
    "NONE": 0,
    "ACTIVE": 1,
})
# Rank
RANK_KBN = Box({
    "DEFAULT": 0,
    "CUSTOM": 1,
})

TIME = Box({
    "FIVE_MINUTES": 300
})

ACTION_TYPE = Box({
    "EMAIL": "email",
    "POST_CARD": "post_card",
    "FLYER": "flyer",
    "SURVEY": "survey",
    "STORE": "store"
})

ACTION_TYPE_NAME = Box({
    "EMAIL": "メール",
    "POST_CARD": "はがき",
    "FLYER": "チラシ",
    "SURVEY": "アンケート",
    "STORE": "来店購入"
})

OPEN_STATUS = Box({
    "OFF": 0,
    "ON": 1,
})

STATUS_MAIL =  Box({
    "NOT_SENT":0,
    "SENT": 1,
    "ERROR": 9
})

NOTIFY_CUSTOMER = Box({
    "NOTIFY": 1,
    "CAMPAIGN": 2,
})

NOTIFY_STATUS = Box({
    "NOT_SEEN": 0,
    "SEEN": 1,
})

# Before and After a time
TYPE_SEARCH_DATE = Box({
    "BEFORE": "0",
    "AFTER": "1",
})

# Type of customer notify
TYPE_CUSTOMER_NOTIFY = Box({
    "NOTIFY": "1",
    "INFORMATION": "2"
})

# Payment method code
PAYMENT_METHOD = Box({
    "WITHDRAWAL": 1,
    "CARD": 2,
    "BANKING": 3,
    "OTHER": 4,
})

# Billing cycle
PAYMENT_PLAN = Box({
    "MONTHLY": 1,
    "YEARLY": 2,
})

# Mode check query get list customer
MODE_GET_LIST = Box({
    "DEFAULT" : 1,
    "CONDITION" : 2,
    "CUSTOMER_TAGS" : 3,
    "ERROR" : 4,
})

# Mode check call api get customer by customer no
MODE_GET_CUSTOMER_NO = Box({
    "DASHBOARD" : 1,
    "VISIT_STORE" : 2,
})

# Print status of postcard, flyer
PRINT_STATUS = Box({
    "CONFIRM": {
      "text": "未処理",
      "value": 0
    },
    "DOWNLOAD": {
      "text": "DL済",
      "value": 2
    },
    "SENDED": {
      "text": "発送済",
      "value": 3
    },
})

AUTH_TWO_STEP = Box({
    "OFF": 0,
    "ON": 1
})

AUTH_TWO_STEP_TYPE = Box({
    "GOOGLE": 1,
    "EMAIL": 2,
    "SMS": 3,
})

TIME_OUT_OTP = 60

COUNTRY_CODE="+81"

SYSTEM_NAME="CRM"
# Type calendar
TYPE_CALENDAR = Box({
    "YEAR" : 1,
    "MONTH" : 2,
})

# Notification of receive action
SEND_NOTIFI_ACT = Box({
    "RECEIVE": "0",
    "NO_RECEIVE": "1",
})

# Type of templates
TYPE_TEMPLATES = Box({
    "ACTION": "1",
    "DEFAULT": "2",
    "ACTION_DEFAULT": "6",
})

# Action has send or not
SEND_ACTION_KBN = Box({
    "SEND": "1",
    "NOT_SEND": "2",
})

# Avatar image default
AVATAR_DEFAULT = "shop/avatar/avatar-default.svg"

TYPE_NO = Box({
    "SHOP_NO": "契約者様№",
    "ACTION_NO": "アクションNoの6桁が999000",
    "CUSTOMER_NO": "会員Noの8桁が99999000",
})

# Common rank
RANK_CUSTOMER = Box({
    "RANK_S": 1,
    "RANK_A": 2,
    "RANK_B": 3,
    "RANK_C": 4,
})

# Common gender
GENDER = Box({
    "MALE": {
        "text": "男性",
        "value": 1
    },
    "FEMALE": {
        "text": "女性",
        "value": 2
    },
    "OTHER": {
        "text": "その他",
        "value": 3
    },
})

# Common loop act
LOOP_ACT = Box({
    "WEEK": {
        "text": "毎週",
        "value": "Weekly"
    },
    "MONTH": {
        "text": "毎月",
        "value": "Monthly"
    },
    "DAY": {
        "text": "毎日",
        "value": "Daily"
    },
    "YEAR": {
        "text": "毎年",
        "value": "Yearly"
    },
    "NO_LOOP": {
        "text": "なし",
        "value": ""
    },
})

# Common loop act
LOOP_TYPE_FREQ = {
  "Weekly": "毎週",
  "Monthly": "毎月",
  "Daily": "毎日",
  "Yearly": "毎年",
}

# Color default shop
COLOR_DEFAULT = "rgba(81, 187, 171, 1)"

# logo image default
LOGO_DEFAULT = "shop/logo/logo-default.svg"

# Data template mail
DATA_TEMPLATE = Box({
  "#fullName": "{{ fullName }}",
  "#memberFullName": "{{ fullName }}",
  "#corporateName": "{{ corporateName }}",
  "#shopName": "{{ corporateName }}",
  "#zipCode": "{{ zipCode }}",
  "#fullAddress": "{{ fullAddress }}",
  "#telephoneNo": "{{ telephoneNo }}",
  "#urlMemberTop": "{{ urlMemberTop }}",
  "#urlMemberLogin": "{{ urlMemberLogin }}",
  "#urlResetPassword": "{{ urlResetPassword }}",
  "#customerMailAddress": "{{ customerMailAddress }}",
  "#memberMailAddress": "{{ customerMailAddress }}",
  "#urlRegister": "{{ urlRegister }}",
  "#urlMemberEdit": "{{ urlMemberEdit }}",
  "#urlChangePass": "{{ urlChangePass }}",
  "#password": "{{ password }}",
})

# Data cookie name
COOKIE_NAME = Box({
  "SHOP": "__CRM_S",
  "MEMBER": "__CRM_M",
  "ADMIN": "__CRM_A",
  "TOKEN_TWO_AUTHEN": "__CRM_S_TOKEN_TWO_AUTHEN"
})

# Type database
TYPE_DB = Box({
  "READ": 0,
  "WRITE": 1
})

FLAG_PREPARE_DATA_ACTION = Box({
  "OFF": 0,
  "ON": 1
})

# Password change notify flag of shop account
class PwChangedNotifyFlg(enum.IntEnum):
  OFF = 0
  ON = 1

# Login notify flag of shop account
class LoginNotifyFlg(enum.IntEnum):
  OFF = 0
  ON = 1

# Auth two step flag of shop account
class TwoFaFlg(enum.IntEnum):
  OFF = 0
  ON = 1

# Auth two step type of shop account
class TwoFaType(enum.IntEnum):
  GOOGLE = 1
  MAIL = 2
  SMS = 3

# Setting rank of shop
class SettingRank(enum.IntEnum):
  PURCHASE = 0
  VISIT = 1

# Status of action
class SendActionStatus(enum.IntEnum):
  NOT_SEND = 0
  SENDED = 1
  ERROR = 9

# Payment plan
class PaymentPlan(enum.IntEnum):
  MONTHLY = 1
  YEARLY = 2

# Action type order
class ActionType(enum.IntEnum):
  EMAIL = 1
  POSTCARD = 2
  FLYER = 3
  SURVEY = 4
  STORE = 5
  REGISTRATION_PROCEDURE = 6
  ALL = 0

# Payment method code
class PaymentMethod(enum.IntEnum):
  WITHDRAWAL = 1
  CARD = 2
  BANKING = 3
  OTHER = 4

# Delete flag
class DeleteFlag(enum.IntEnum):
  OFF = 0
  ON = 1

# user role
# 0: Admin service | 1: Shop Owner | 2: Shop Manager
# | 3: Shop Staff | 4: Customer(Member)
class UserRole(enum.IntEnum):
  ADMIN = 0
  SHOP_OWNER = 1
  SHOP_MANAGER = 2
  SHOP_STAFF = 3
  CUSTOMER = 4

# Open notify status
class OpenStatus(enum.IntEnum):
  OFF = 0
  ON = 1

# Print status
class PrintStatusDetails(enum.IntEnum):
  NOT_SEND = 0
  DOWNLOAD = 2
  SENDED = 3

# Type of customer notify
class CustomerTypeNotify(enum.IntEnum):
  NOTIFY = 1
  INFORMATION = 2

# Login notification flag
class LoginNotificationFlag(enum.IntEnum):
  NONE = 0
  ACTIVE = 1

# Change notification flag
class ChangeNotificationFlag(enum.IntEnum):
  NONE = 0
  ACTIVE = 1

# Sex KBN
class SexKBN(enum.IntEnum):
  MALE = 1
  FEMALE = 2
  OTHER = 3
  BLANK = 0

# Subscription Flag
class SubscriptionFlag(enum.IntEnum):
  YES = 0
  NO = 1

# Rank KBN
class RankKBN(enum.IntEnum):
  YES = 0
  NO = 1

# Rank KBN
class Rank(enum.IntEnum):
  BLANK = 9
  S = 1
  A = 2
  B = 3
  C = 4

# Print status
class PrintStatus(enum.IntEnum):
  CONFIRM = 0
  ALL = 1
  DOWNLOAD = 2
  SENDED = 3
  WAITING = 4
  PREPARE_TO_SEND = 5
  ERROR = 6

# Action status
class ActionStatus(enum.IntEnum):
  SENDED = 1
  NOTSEND = 0

class BatchStatus(enum.Enum):
  CREATED = "created"
  RUNNING = "running"
  SUCCESS = "success"
  ERROR = "error"

class TypeTemplates(enum.IntEnum):
  ACTION = 1
  DEFAULT = 2

# Flag exclusions
class HasConditionExclusion(enum.IntEnum):
  NO = 0
  YES = 1


class SettingRankKbn(enum.IntEnum):
  AMOUNT = 0
  VISIT = 1

# Custom class IntEnum
class IntEnum(db.TypeDecorator):
  """
  Enables passing in a Python enum and storing the enum's *value* in the db.
  The default would have stored the enum's *name* (ie the string).
  """
  impl = db.Integer
  cache_ok = True

  def __init__(self, enumtype, *args, **kwargs):
    super(IntEnum, self).__init__(*args, **kwargs)
    self._enumtype = enumtype

  def process_bind_param(self, value, dialect):
    if isinstance(value, int):
      return value

    return value.value

  def process_result_value(self, value, dialect):
    return self._enumtype(value)
