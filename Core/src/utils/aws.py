"""
AWS Function
"""
import base64
import boto3
import helpers.const as env
from crm_batch.tasks import app as celery_client
import time as time_

# Upload file to S3
# Param:
#   @data: Data request
#   @directory: Directory of file
#   @content_type: File content type
#   @encoding: Encoding type
# Output:
#   return: Url of file in s3
def upload_file_to_s3(file_name, data, directory, content_type, encoding=None):
  s3 = boto3.resource("s3")
  s3_obj = s3.Object(env.S3.BUCKET.NAME, directory + file_name)
  kwargs = {
      "Body": data,
      "ContentType": content_type,
  }
  if encoding is not None:
    kwargs["ContentEncoding"] = encoding

  s3_obj.put(**kwargs)
  s3_file_key = f"{directory + file_name}"
  return s3_file_key


# Generate presigned url
# Param:
#   @key: path of file
# Output:
#   return: presigned url of file
def create_presigned_url(key):
  s3_client = boto3.client("s3")
  response_url = s3_client.generate_presigned_url(
    "get_object",
    Params={
        "Bucket": env.S3.BUCKET.NAME,
        "Key": key
    }, ExpiresIn=env.S3.EXPIRED.TIME)

  return response_url


# Apply task celery to queue
# Params:
#   @job_id: Job id
#   @task_name: Tasks name
#   @data_msg: Data send to tasks
# Output:
#   return: Void
def apply_task(job_id, task_name, data_msg):
  celery_client.signature(task_name,kwargs=data_msg, options={"task_id":job_id}).apply_async(countdown=5)


# Validate image avatar
# Params:
#   @image: Avatar
#   @image_ext: Avatar ext
#   @image_size: Avatar size
#   @default_avatar: Default avatar
# Output:
#   return: S3 file key
def validate_avatar(image, image_ext, image_size, default_avatar):
  s3_file_key = default_avatar
  ext_allow = ["png", "jpg", "jpeg"]
  # Check upload file or not
  if image and image_ext:
    # file extension not in png, jpg, jpeg will return an error
    if image_ext.lower() not in ext_allow or int(image_size) > env.MAX_SIZE_IMAGE:
      return False

    file_name = "avatar_" + str(time_.time()) + "." + image_ext
    # convert file data to base64
    imgdata = base64.b64decode(image)
    # Send file to s3 and set reponse path of file in s3
    s3_file_key = upload_file_to_s3(file_name, imgdata, env.S3.DIRECTORY.SHOP.AVATAR, "image/jpeg")

  return s3_file_key
