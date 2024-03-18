"""
Common repository
"""


from copy import deepcopy
from . import Exception, ERR_MESSAGE
from models import Shops, ShopAccounts, ShopSettings, SiteConfigs, ActionTypes, Batches, Actions
from helpers import kbn
import helpers.const as env
from fastapi.encoders import jsonable_encoder
from utils.date import get_current_time_obj


class CommonRepository():
  """
  Common of Repository
  """
  def __init__(self, session_factory, session_factory_read):
    self.session_factory = session_factory
    self.session_factory_read = session_factory_read


  # Get shop by shop no
  # Params:
  #   @shop_no: Shop no
  # Output:
  #  return: Shop item
  def find_shop_by_shop_no(self, shop_no):
    with self.session_factory_read() as session:
      return session.query(Shops).filter(Shops.shop_no == shop_no, Shops.is_deleted == kbn.DeleteFlag.OFF.value).first()


  # Get data config by key
  # Params:
  #   @key: key config
  # Output:
  #  return: Data config
  def get_data_configs(self, key):
    with self.session_factory_read() as session:
      return session.query(SiteConfigs.value).filter(SiteConfigs.key == key, SiteConfigs.is_deleted == kbn.DeleteFlag.OFF.value).all()


  # Get data setting shop by shop_no
  # Params:
  #   @shop_no: shop_no of shop
  #   @key: key setting shop
  # Output:
  #  return: Data setting shop
  def find_setting_shop_by_shop_no(self, shop_no, key):
    with self.session_factory_read() as session:
      return session.query(ShopSettings).filter(
          ShopSettings.key == key,
          ShopSettings.shop_no == shop_no,
          ShopSettings.is_deleted == kbn.DeleteFlag.OFF.value).first()


  # Generate customer no
  # Params:
  #   @shop_no: Shop no
  # Output:
  #  return: Data setting shop
  def generate_customer_no(self, shop_no):
    max_customer_no = self.find_setting_shop_by_shop_no(shop_no, "customer_no")
    customer_no = ""

    # Have data customerNo max
    if max_customer_no:
      max_no = deepcopy(max_customer_no.value)
      # customerNo is less than 99999999
      if int(max_no) < env.LIMIT_CUSTOMER_NO:
        customer_no = f"{(int(max_no) + 1):08d}"
      # customerNo is equal or greater than 99999999
      else:
        customer_no = f"{int(max_no):08d}"
      # update data shop settings
      with self.session_factory() as session:
        # Update shop setting
        session.query(ShopSettings).filter(
          ShopSettings.key == "customer_no",
          ShopSettings.shop_no == shop_no,
          ShopSettings.is_deleted == kbn.DeleteFlag.OFF.value).update({
            "value": int(max_no) + 1,
            "updated_user": "system",
        })
        session.commit()
      return customer_no
    # Don't have data customerNo max will return error
    else:
      raise Exception(message=ERR_MESSAGE.ERRMSG0029)


  # Check email exist
  # Param:
  #  @email: Email account
  # Output:
  #  return: Boolean
  def check_email_exist(self, email):
    with self.session_factory_read() as session:
      account = session.query(ShopAccounts).filter(
        ShopAccounts.email == email,
        ShopAccounts.is_deleted == kbn.DeleteFlag.OFF.value).first()

      # Email not exist
      if account is None:
        return False
      return True


  # Get shop by url
  # Params:
  #   @url: URL of shop
  # Output:
  #  return: Shop item
  def get_shop_by_url(self, url):
    with self.session_factory_read() as session:
      return session.query(Shops).filter(Shops.url == url, Shops.is_deleted == kbn.DeleteFlag.OFF.value).first()


  # Get action types
  # Params: None
  # Output:
  #   return: List action type
  def get_action_types(self):
    with self.session_factory_read() as session:
      result_action_type = jsonable_encoder(session.query(ActionTypes).all())

      return result_action_type


  # Add item of batches table
  # Params:
  #   @job_id: Job id
  #   @job_type: Name of queue
  #   @job_name: Name of function
  #   @args: Data send to task
  #   @shop_no: Shop no of shop
  # Output:
  #   return: Void

  def add_batches(self, job_id, job_type, job_name, args, shop_no = None):
    with self.session_factory() as session:
      add_data = {
        "job_id": job_id,
        "job_type": job_type,
        "job_name": job_name,
        "args": args,
        "status": kbn.BatchStatus.CREATED.value,
        "queue_time": get_current_time_obj(),
        "start_time": None,
        "end_time": None,
        "payload": None,

        "shop_no": shop_no
      }

      add_data = Batches(**add_data)

      session.add(add_data)

      session.commit()


  # Update status of batches
  # Params:
  #   @job_id: Job id
  #   @type_status: Type of batch status
  # Output:
  #   return: Void
  def update_batches(self, job_id, type_status):
    with self.session_factory() as session:
      query_batch = session.query(Batches).filter(
        Batches.job_id == job_id
      )

      # Update batch status
      if type_status in [kbn.BatchStatus.RUNNING.value, kbn.BatchStatus.SUCCESS.value]:
        query_batch.update({
          Batches.status: type_status,
        })
      # Update batch status and retry_count when status is error
      elif type_status == kbn.BatchStatus.ERROR.value:
        result_batch = session.query(Batches).filter(Batches.job_id == job_id).first()

        query_batch.update({
          Batches.status: type_status,
          Batches.retry_count: result_batch.retry_count + 1,
        })

      session.commit()


  # Update shop settings
  # Params:
  #   @shop_no: Shop no
  #   @key: Name key settings
  #   @new_value: New value to updated
  #   @updater: User update
  # Output:
  #   return: Void
  def update_shop_setting(self, shop_no, key, new_value, updater):
    with self.session_factory() as session:
      session.query(ShopSettings).filter(
        ShopSettings.shop_no == shop_no,
        ShopSettings.key == key
      ).update({
        ShopSettings.value: new_value,
        ShopSettings.updated_user: updater,
      })

      session.commit()


  # Check data action
  # Params:
  #   @shop_no: Shop no
  # Output:
  #  return: Boolean
  def check_data_action(self, shop_no):
    with self.session_factory_read() as session:
      action_item = session.query(Actions).filter(
        Actions.shop_no == shop_no,
        Actions.is_deleted == kbn.DeleteFlag.OFF.value
      ).first()

      if action_item:
        return True

      return False
