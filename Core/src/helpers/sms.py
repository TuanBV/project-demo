"""
SMS
"""
import helpers.const as env
import boto3
from botocore.exceptions import ClientError

def send_sms(telephone_no, content):
  # Create a new SNS resource and specify a region.
  client = boto3.client('sns', region_name=env.AWS_REGION_NAME)
  # Try to send the SMS.
  try:
    # Send your sms message.
    response = client.publish(
        PhoneNumber=telephone_no,
        Message=content
    )
  # Display an error if something goes wrong.
  except ClientError as e:
    print('===============================================')
    print('Send SMS error:')
    print(e.response['Error']['Message'])
  else:
    print('Send SMS sent! Message ID:')
    print(response['MessageId'])

