"""Exception"""


from helpers.const import CODE


class CrmException(Exception):
  """Exception raised for system errors.

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


class NoDataException(Exception):
  """Exception raised for no data errors.

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


class UnauthorizedException(Exception):
  """Exception raised for unauthorized errors.

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


class PermissionException(Exception):
  """Exception raised for permission errors.

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


class SendMailException(Exception):
  """Exception raised for send mail errors.

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


class AppVersionException(Exception):
  """Exception raised for app version invalid errors.

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
