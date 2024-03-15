"""CrmException"""


from helpers.const import CODE


class CrmException(Exception):
  """Exception raised for CRM system errors.

  Attributes:
      code -- code which caused the error
      message -- explanation of the error
  """

  def __init__(self, code=CODE.API.ERROR, message="システムエラーが発生しました。"):
    self.code = code
    self.message = message
    super().__init__(self.message)

  def __str__(self):
    return f"{type(self).__name__}: {self.code} -> {self.message}"


class CrmNoDataException(CrmException):
  """Exception raised for CRM no data errors.

  Attributes:
      code -- code which caused the error
      message -- explanation of the error
  """

  def __init__(self, code=CODE.API.NO_CONTENT, message="データが存在しません。"):
    self.code = code
    self.message = message
    super().__init__(self.code, self.message)

  def __str__(self):
    return f"{type(self).__name__}: {self.code} -> {self.message}"


class CrmUnauthorizedException(CrmException):
  """Exception raised for CRM unauthorized errors.

  Attributes:
      code -- code which caused the error
      message -- explanation of the error
  """

  def __init__(self, code=CODE.API.INVALID_REQUEST, message="認証が失敗しました。", cookie_config=None):
    self.code = code
    self.message = message
    self.cookie_config= cookie_config
    super().__init__(self.code, self.message,)

  def __str__(self):
    return f"{type(self).__name__}: {self.code} -> {self.message}"


class CrmPermissionException(CrmException):
  """Exception raised for CRM permission errors.

  Attributes:
      code -- code which caused the error
      message -- explanation of the error
  """

  def __init__(self, code=CODE.API.INVALID_PERMISSION, message="アクセス権限がありません。"):
    self.code = code
    self.message = message
    super().__init__(self.code, self.message)

  def __str__(self):
    return f"{type(self).__name__}: {self.code} -> {self.message}"


class CrmSendMailException(CrmException):
  """Exception raised for CRM send mail errors.

  Attributes:
      code -- code which caused the error
      message -- explanation of the error
  """

  def __init__(self, code=CODE.API.SEND_MAIL_FAILED, message="メール送信ができません。"):
    self.code = code
    self.message = message
    super().__init__(self.code, self.message)

  def __str__(self):
    return f"{type(self).__name__}: {self.code} -> {self.message}"


class CrmAppVersionException(Exception):
  """Exception raised for CRM app version invalid errors.

  Attributes:
      code -- code which caused the error
      message -- explanation of the error
  """

  def __init__(self, code=CODE.API.APP_VERSION_ERROR, message="システムのパージョンアップのた再ログインをお願いします"):
    super().__init__()
    self.code = code
    self.message = message

  def __str__(self):
    return f"{type(self).__name__}: {self.code} -> {self.message}"
