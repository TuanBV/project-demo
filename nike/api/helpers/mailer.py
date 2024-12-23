"""
Mailer
"""
from typing import List
from setting import settings
from pydantic import EmailStr
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

class Mailer():
  """
      Send mail with Mailer
  """

  def __init__(self, username: str = settings.MAIL_USERNAME, password: str = settings.MAIL_PASSWORD) -> None:
    self._username = username
    self._password = password
    self._port: int = settings.MAIL_PORT
    self._mail_host: str = settings.MAIL_HOST
    self._tls = settings.MAIL_TLS
    self._ssl = settings.MAIL_SSL
    self._body = ""
    self._mail_from = ""
    self._recipients = []
    self._cc = []
    self._bcc = []
    self._reply_to = []
    self._attachments = []
    self._charset = "utf-8"


  def set_port(self, port: int):
    self._port = port
    return self


  def get_port(self) -> int:
    return self._port


  def set_mail_from(self, mail_from: str):
    self._mail_from = mail_from
    return self


  def get_mail_from(self) -> str:
    return self._mail_from


  def set_mail_host(self, mail_host: str):
    self._mail_host = mail_host
    return self


  def get_mail_host(self) -> str:
    return self._mail_host


  def set_tls(self, tls: bool):
    self._tls = tls
    return self


  def tls(self) -> bool:
    return self._tls


  def set_ssl(self, ssl: bool):
    self._ssl = ssl
    return self


  def ssl(self) -> bool:
    return self._ssl


  def subject(self, subject: str):
    self._subject = subject
    return self


  def html(self, body: str):
    self._body = body
    self._subtype = "html"
    return self


  def text_plain(self, body: str):
    self._body = body
    self._subtype = "plain"
    return self


  def recipient(self, *mails: List[EmailStr]):
    self._recipients += mails
    return self


  def remove_recipient(self, mail: EmailStr):
    self._recipients.remove(mail)
    return self


  def cc(self, *mails: List[EmailStr]):
    self._cc += mails
    return self


  def remove_cc(self, mail: EmailStr):
    self._cc.remove(mail)
    return self


  def bcc(self, *mails: List[EmailStr]):
    self._bcc += mails
    return self


  def remove_bcc(self, mail: EmailStr):
    self._bcc.remove(mail)
    return self


  def reply_to(self, mails: List[EmailStr]):
    self._reply_to += mails
    return self


  def remove_reply_to(self, mail: EmailStr):
    self._reply_to.remove(mail)
    return self


  def charset(self, charset: str):
    self._charset = charset
    return self


  def add_attachment(self, path: str, mime_type: str = "", mime_subtype: str = ""):
    """Handle add attachment

    Args:
        path (str): file path
        name (str, optional): file name. Defaults to "".
        mime_type (str, optional): Defaults to "".
        mime_subtype (str, optional): Defaults to "".

    E.g.::
        Mailer().add_attachment("./upload/sample.pdf", "sample.pdf")
        ...

    Returns:
        Mailer
    """
    attachment = { "file": path }

    if mime_type:
      attachment["mime_type"] = mime_type

    if mime_subtype:
      attachment["mime_subtype"] = mime_subtype

    self._attachments.append(attachment)
    return self


  def _connect(self) -> FastMail:
    """Handle connect smtp with FastMail

    Returns:
        FastMail: Fast mail object
    """
    conf = ConnectionConfig(
      MAIL_USERNAME = self._username,
      MAIL_PASSWORD = self._password,
      MAIL_FROM = self._mail_from,
      MAIL_PORT = self._port,
      MAIL_SERVER = self._mail_host,
      MAIL_TLS = self.tls(),
      MAIL_SSL = self.ssl(),
      USE_CREDENTIALS = True,
      VALIDATE_CERTS = True
    )
    return FastMail(conf)


  async def send(self) -> None:
    """Handle send mail
    """

    message = {
      "subject": self._subject,
      "recipients": self._recipients,
      "reply_to": self._reply_to,
      "cc": self._cc,
      "subtype": self._subtype,
      "attachments": self._attachments,
      "charset": self._charset
    }

    if message["subtype"] == "html":
      message["html"] = self._body
    else:
      message["body"] = self._body

    message = MessageSchema(**message)
    await self._connect().send_message(message)

