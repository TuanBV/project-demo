"""
Const environment
"""
from box import Box
from setting import settings
import pytz

AWS_REGION_NAME = "ap-northeast-1"

IS_PROD = True if settings.ENVIRONMENT == "production" else False

S3 = Box({
    "BUCKET": {
        "NAME": "crm-public"
    },
    "DIRECTORY": {
        "EXPORT": "export/csv/",
        "SHOP": {
            "AVATAR": "shop/avatar/",
            "POST_CARD": "shop/post-card/",
            "FLYER": "shop/flyer/",
            "LOGO": "shop/logo/",
        },
        "ADMIN": {
            "ZIP_FILE": "admin/zip-file/",
            "POSTCARD_PDF": "admin/postcard_address_pdf/",
            "FLYER_PDF": "admin/flyer_address_pdf/"
        },
    },
    "EXPIRED": {
        "TIME": 3600  # 1 hour
    }
})
CODE = Box({
    "API": {
        "SUCCESS": 0,
        "INVALID_REQUEST": "ERRAPI401",
        "ERROR": "ERRAPI400",
        "NOT_FOUND": "ERRAPI404",
        "SYSTEM_ERROR": "ERRAPI999",
        "NO_CONTENT": "ERRAPI204",
        "SEND_MAIL_FAILED": "ERRAPI500",
        "INVALID_PERMISSION": "ERRAPI403",
        "INVALID_TOKEN": "ERRAPI998",
        "APP_VERSION_ERROR": "ERRAPI503",
        "ACTION_PENDING": "ERRAPI997",
        "ACTION_SENDED": "ERRAPI996",
        "ACTION_NOT_ALLOW_SENDED": "ERRAPI995"
    },
    "HTTP_STATUS": {
        "SUCCESS": 200,
        "ERROR": 400,
        "NOT_FOUND": 404,
        "UNAUTHORIZED": 401,
        "NO_CONTENT": 204,
        "SYSTEM_ERROR": 500,
        "APP_VERSION_ERROR": 503,
    },
    "ERROR": {
        "UNAUTHORIZED": 902,
    },
})

# Key authorize
JWT = Box({
    "SECRET": {
        "KEY": settings.JWT_SECRET,
        "ALGORITHM": "HS256",
    },
    "EXPIRED": 7*24*3600 # 30 minute
})

# cookie lifetime
MAX_AGE = 7*24*3600 # 30 minute

# Config SMTP
# False: not send, True: Send
MODE_SEND = True
SMTP = Box({
    "CHARSET": "UTF-8",
    "REGION": AWS_REGION_NAME,
    "FROM": {
        "SENDER": "CRM <info@najimi.jp>",
    }
})

# Mode data
MODE_DATA = Box({
    "VALIDATE_NOT_SAVE": "1",
    "VALIDATE_AND_SAVE": "2",
})

# Contact telephone no
SYSTEM_TEL = "03-1234-1234"

# Timezone
TIMEZONE = pytz.timezone("Asia/Tokyo")

# Maximum pdf file size
MAX_SIZE_IMAGE = 3*1024*1024

# Maximum pdf file size
MAX_SIZE_PDF = 10*1024*1024

# Warning of customer no
WARNING_CUSTOMER_NO = 99999000

# Limit of customer no
LIMIT_CUSTOMER_NO = 99999999

# Shop no key
SHOP_KEY = "NJ"

# Service name
SERVICE_NAME = "NAJIMI"

# Url aws
URL_AWS = "https://s3-%s.amazonaws.com/%s/%s"

# Warning of action no
WARNING_ACTION_NO = 999000

# Limit of action no
LIMIT_ACTION_NO = 999999

ONE_HOUR = 3600

# Shop no max
SHOP_NO_MAX = 99999

# Shop no warning
WARNING_SHOP_NO = "NJZ99000"

# Point default
POINT_DEFAULT = 10

# Shop no of default template
SHOP_NO_TEMPLATE_DEFAULT = "0"

FORMAT_DATE = "%Y-%m-%d"

# Tasks
TASK_NAME = Box({
  "PREPARE_DATA_ACTION": "tasks.prepare_data_action",
  "PREPARE_ACTION_ONE_CUSTOMER": "tasks.prepare_action_one_customer",
  "SEND_MAIL_REGISTRATION": "tasks.send_mail_registration",
  "SUBMIT_PREPARE_DATA_ACTION": "tasks.submit_prepare_data_action",
})

# File type
FILE_TYPE = Box({
  "PDF": "application/pdf"
})

# Regexp
REGEXP = Box({
    "YEAR": "^[0-9]{0,4}$|^$",
    "AMOUNT": "^(([1-9](\\d{1,6}))|[\\d]{1})$|^$",
    "VISIT": "^([1-9][0-9][0-9]?|[1-9][0-9]?)$|^$|^[\\d]{1}$",
    "RANGE_DATE": "^([1-9][0-9][0-9]?|[1-9][0-9]?)$|^$",
    "RANK": r"^(([1-9](\d{1,7}))|[\d]{1}|null)$",
})

# Url doc
URL_DOC = "http://localhost:8081/api/v1/docs"

# Header csv
HEADER_CSV = Box({
    "SHOP_NO": "契約者様No.",
    "SHOP_NAME": "契約者様名",
    "TELEPHONE_NO": "電話番号",
    "FULLNAME": "代表者氏名",
    "FULLNAME_KANA": "代表者氏名（カナ）",
    "EMAIL": "メールアドレス",
    "ZIPCODE": "郵便番号",
    "PREFECTURE": "都道府県",
    "ADDRESS": "住所（市区町村）",
    "ADDRESS_1": "住所（以降１）",
    "ADDRESS_2": "住所（以降２）",
    "USING_START_DATE": "利用開始日",
    "CONTRACT_START_DATE": "契約開始年月",
    "CONTRACT_END_DATE": "契約終了年月",
    "FIRST_PAYMENT": "初期費用料金",
    "SHOP_URL": "URL",
    "PAYMENT_METHOD": "支払い方法",
    "PAYMENT_PLAN": "請求タイミング",
    "NOTE": "備考",
    "PRINT_STATUS": "処理状況",
    "ACT_DELIVERY_TIME": "アクションタイミング",
    "ACT_TYPE": "アクション種別",
    "ACT_NAME": "アクション名",
    "TITLE_CONDITION": "リスト設定名",
    "NUMBER_CUSTOMER": "リスト件数",
    "URL_ACT": "アクション表示URL" ,
    "LIST_CUSTOMER_ACT": "お客様一覧表示URL",
    "LAST_NAME": "氏名（姓）",
    "FIRST_NAME": "氏名（名）",
    "LAST_NAME_KANA": "氏名カナ（セイ）",
    "FIRST_NAME_KANA": "氏名カナ（メイ）",
    "BIRTHDAY": "生年月日",
    "GENDER": "性別",
    "REGISTRATION_DATE": "登録日",
    "RANGE_DATE_REGISTERED": "登録経過日数",
    "LAST_VISITED_DATE": "直近来店日",
    "RANGE_DATE_VISITED": "直近来店経過日数",
    "LAST_SENT_ACT_DATE": "直近アクション日",
    "RANGE_DATE_ACT_SENT": "アクション経過日数",
    "AMOUNT_1_MONTH": "購入金額（直近1か月間）",
    "AMOUNT_3_MONTH": "購入金額（直近3か月間）",
    "AMOUNT_6_MONTH": "購入金額（直近6か月間）",
    "AMOUNT_12_MONTH": "購入金額（直近12か月間）",
    "TOTAL_AMOUNT": "購入金額（全期間）",
    "VISITED_1_MONTH": "来店回数（直近1か月間）",
    "VISITED_3_MONTH": "来店回数（直近3か月間）",
    "VISITED_6_MONTH": "来店回数（直近6か月間）",
    "VISITED_12_MONTH": "来店回数（直近12か月間）",
    "TOTAL_VISIT": "来店回数（全期間）",
    "DAY": "日付",
    "POINT": "ポイント",
    "PAYMENT": "金額",
    "POINT_CONTENT": "内容",
    "ACT_TIME": "時刻",
    "ACT_TYPE_2": "種別",
    "LOOP_TYPE": "繰返し",
    "ACT_NAME_2": "アクション名称",
})

# Date format (ex: 2022-11-05)
DATE_FORMAT = "%Y-%m-%d"
