"""
SMTP Mail SES
"""
import helpers.const as env
from helpers import kbn
import boto3
from core.error import CrmSendMailException
from core import get_logger
from botocore.exceptions import ClientError
from jinja2 import Template
from setting import settings

logger = get_logger()

def sendmail_text(destination, subject, template, data, throw_except = False):
  if not env.MODE_SEND:
    return

  # Create a new SES resource and specify a region.
  client = boto3.client('ses', region_name=env.SMTP.REGION)

  # genarel data to content
  for item_template in kbn.DATA_TEMPLATE:
    template.BODY_TEXT = template.BODY_TEXT.replace(item_template, kbn.DATA_TEMPLATE[item_template])

  tm1 = Template(template.BODY_TEXT)
  body_text = tm1.render(data)
  # Try to send the email.
  try:
    # Provide the contents of the email.
    client.send_email(
        Destination=destination,
        Message={
            'Body': {
                'Text': {
                    'Charset': env.SMTP.CHARSET,
                    'Data': body_text,
                },
            },
            'Subject': {
                'Charset': env.SMTP.CHARSET,
                'Data': kbn.PREFIX_SUBJECT_MAIL[settings.ENVIRONMENT] + subject,
            },
        },
        Source=env.SMTP.FROM.SENDER,
        # If you are not using a configuration set, comment or delete the
        # following line
        #ConfigurationSetName=env.SMTP.CONFIGURATION_SET,
    )
  # Display an error if something goes wrong.
  except ClientError as e:
    if throw_except:
      raise CrmSendMailException() from e


def sendmail_html(destination, subject, template, data):
  if not env.MODE_SEND:
    return

  # Create a new SES resource and specify a region.
  client = boto3.client('ses', region_name=env.SMTP.REGION)
  # genarel data to content
  tm2 = Template(template.BODY_HTML)
  body_html = tm2.render(data)
  # Try to send the email.
  try:
    # Provide the contents of the email.
    client.send_email(
        Destination=destination,
        Message={
            'Body': {
                'Html': {
                    'Charset': env.SMTP.CHARSET,
                    'Data': body_html,
                },
            },
            'Subject': {
                'Charset': env.SMTP.CHARSET,
                'Data': kbn.PREFIX_SUBJECT_MAIL[settings.ENVIRONMENT] + subject,
            },
        },
        Source=env.SMTP.FROM.SENDER,
        # If you are not using a configuration set, comment or delete the
        # following line
        #ConfigurationSetName=env.SMTP.CONFIGURATION_SET,
    )
  # Display an error if something goes wrong.
  except ClientError as e:
    logger.info('===============================================')
    logger.info('Email error:')
    logger.info(e.response['Error']['Message'])
